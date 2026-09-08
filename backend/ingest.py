import os
import glob
import time
import logging
from typing import List
from dotenv import load_dotenv
from pypdf import PdfReader
from neo4j import GraphDatabase
from langchain_google_genai import GoogleGenerativeAIEmbeddings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "761a39a2")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

embedding_model = GoogleGenerativeAIEmbeddings(
    google_api_key=GEMINI_API_KEY,
    model="models/gemini-embedding-001",
    output_dimensionality=384
)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 100:
            chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def ingest():
    pdf_files = sorted(glob.glob("../dataset/*.pdf"))
    if not pdf_files:
        pdf_files = sorted(glob.glob("dataset/*.pdf"))
    
    logging.info(f"Found {len(pdf_files)} PDF files in dataset directory.")
    
    with driver.session(database=NEO4J_DATABASE) as session:
        # Create vector index if not existing
        session.run("""
        CREATE VECTOR INDEX vector IF NOT EXISTS
        FOR (c:Chunk) ON (c.embedding)
        OPTIONS {indexConfig: {
          `vector.dimensions`: 384,
          `vector.similarity_function`: 'cosine'
        }}
        """)
        logging.info("Ensured Neo4j vector index 'vector' exists.")

    total_chunks_ingested = 0
    
    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        logging.info(f"Processing {file_name}...")
        
        try:
            reader = PdfReader(pdf_path)
            full_text = ""
            # Sample pages evenly across the PDF to get good coverage
            total_pages = len(reader.pages)
            step = max(1, total_pages // 25)
            selected_pages = list(range(0, total_pages, step))[:25]
            
            for p in selected_pages:
                page_text = reader.pages[p].extract_text()
                if page_text:
                    full_text += page_text + "\n"
            
            chunks = chunk_text(full_text)
            if not chunks:
                continue
            
            # Limit per PDF for fast ingestion
            chunks = chunks[:20]
            
            logging.info(f"Generating embeddings for {len(chunks)} chunks of {file_name}...")
            embeddings = embedding_model.embed_documents(chunks)
            
            with driver.session(database=NEO4J_DATABASE) as session:
                # Merge Document node
                session.run("MERGE (d:Document {fileName: $fileName})", fileName=file_name)
                
                # Merge Chunk nodes and connect to Document
                for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                    chunk_id = f"{file_name}_chunk_{idx}"
                    session.run("""
                    MERGE (c:Chunk {id: $chunk_id})
                    SET c.text = $text, c.embedding = $embedding
                    WITH c
                    MATCH (d:Document {fileName: $fileName})
                    MERGE (c)-[:PART_OF]->(d)
                    """, chunk_id=chunk_id, text=chunk, embedding=emb, fileName=file_name)
            
            total_chunks_ingested += len(chunks)
            logging.info(f"Ingested {len(chunks)} chunks for {file_name}.")
        except Exception as e:
            logging.error(f"Error processing {file_name}: {e}")
            
    logging.info(f"🎉 Ingestion finished! Total chunks ingested: {total_chunks_ingested}")
    driver.close()

if __name__ == "__main__":
    ingest()
