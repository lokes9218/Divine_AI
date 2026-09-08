import os
import logging
import uuid
import time
import tempfile
import base64
import threading
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Keep-alive imports
import requests

# Sarvam AI integration
from sarvamai import SarvamAI

# Commented out ElevenLabs and Google Translate imports
# from google.cloud import translate
# from elevenlabs import ElevenLabs

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_neo4j import Neo4jVector, Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "mahabharata")

CHAT_TOKEN_CUT_OFF = 10
MAX_HISTORY_MESSAGES = 4

# Optimized retrieval query
VECTOR_GRAPH_SEARCH_QUERY = """
WITH node as chunk, score
WHERE score > 0.1
OPTIONAL MATCH (chunk)-[:PART_OF]->(d:Document)
RETURN
   chunk.text as text,
   score,
   {source: COALESCE(d.fileName, d.url, 'unknown')} AS metadata
LIMIT 15
"""

CHAT_SYSTEM_TEMPLATE = """
You are an AI-powered question-answering agent specializing in the Mahabharata. Provide accurate, comprehensive, and well-structured responses.

### Response Guidelines:
1. **Clarity First**: Write naturally and clearly. Use 1-3 paragraphs as needed.
2. **Appropriate Length**: Aim for 100-150 words. Be thorough but concise.
3. **Natural Structure**: Use paragraph breaks for readability.
4. **Depth**: Provide sufficient context and explanation.
5. **Tone**: Professional, engaging, and informative.

### Context:
<context>
{context}
</context>

Using the provided context and your knowledge of the Mahabharata, answer the user's question comprehensively.
"""

# In-memory session management
class InMemorySession:
    """Fast in-memory chat session."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List = []
    
    def add_user_message(self, content: str):
        self.messages.append(HumanMessage(content=content))
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]
    
    def add_ai_message(self, content: str):
        self.messages.append(AIMessage(content=content))
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]
    
    def get_messages(self):
        return self.messages
    
    def clear(self):
        self.messages = []

memory_sessions = {}

def get_or_create_session(session_id: Optional[str] = None) -> str:
    if session_id and session_id in memory_sessions:
        return session_id
    
    new_session_id = str(uuid.uuid4())
    memory_sessions[new_session_id] = InMemorySession(new_session_id)
    return new_session_id

def format_documents_fast(documents, cutoff=CHAT_TOKEN_CUT_OFF):
    """Optimized document formatting with truncation."""
    docs_to_use = documents[:cutoff]
    
    formatted_parts = []
    sources = set()
    
    for doc in docs_to_use:
        source = doc.metadata.get('source', 'unknown')
        sources.add(source)
        
        # Truncate long documents
        content = doc.page_content
        if len(content) > 400:
            content = content[:400] + "..."
        
        formatted_parts.append(f"[{source}] {content}")
    
    context = "\n\n".join(formatted_parts)
    return context, list(sources)

def extract_text_from_ai_response(content):
    """Safely extract string content from LangChain AI response."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, str):
                text_parts.append(item)
            elif isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])
            elif hasattr(item, "text"):
                text_parts.append(item.text)
        return "".join(text_parts)
    return str(content)

def get_total_tokens_fast(ai_response):
    try:
        return ai_response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
    except:
        return 0

def process_documents_fast(docs, question, messages, llm):
    """Optimized processing with size limits."""
    start_time = time.time()
    
    try:
        # Format
        format_start = time.time()
        context, sources = format_documents_fast(docs)
        format_time = time.time() - format_start
        
        # Log sizes
        context_tokens = len(context) // 4
        history_tokens = sum(len(m.content) for m in messages) // 4
        logging.info(f"📊 Context: ~{context_tokens} tokens, History: ~{history_tokens} tokens")
        logging.info(f"⏱️  Formatting: {format_time:.3f}s")
        
        # Build prompt with history
        recent_messages = messages[-MAX_HISTORY_MESSAGES:]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", CHAT_SYSTEM_TEMPLATE),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "User question: {input}")
        ])
        
        # Generate
        gen_start = time.time()
        chain = prompt | llm
        ai_response = chain.invoke({
            "messages": recent_messages,
            "context": context,
            "input": question
        })
        gen_time = time.time() - gen_start
        logging.info(f"⏱️  LLM generation: {gen_time:.3f}s")
        
        total_time = time.time() - start_time
        response_text = extract_text_from_ai_response(ai_response.content)
        
        return {
            'message': response_text,
            'sources': sources,
            'total_tokens': get_total_tokens_fast(ai_response),
            'model': "gemini-3.6-flash",
            'time_taken': total_time
        }
        
    except Exception as e:
        logging.error(f"❌ Processing error: {e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup with optimized settings."""
    try:
        logging.info("🚀 Initializing...")
        
        # Embedding model - keep the existing Neo4j index dimensionality.
        start = time.time()
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set")
        
        embedding_model = GoogleGenerativeAIEmbeddings(
            google_api_key=gemini_api_key,
            model="models/gemini-embedding-001",
            output_dimensionality=384
        )
        app.state.embedding_model = embedding_model
        logging.info(f"✅ Embeddings initialized ({time.time()-start:.2f}s)")
        
        # LLM with optimized settings
        llm_instance = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-3.6-flash",
            temperature=0.2,
            max_tokens=1024,
            timeout=60,
            max_retries=2
        )
        app.state.llm = llm_instance
        logging.info("✅ LLM initialized")
        
        # Neo4j
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE
        )
        app.state.graph = graph
        logging.info("✅ Neo4j connected")
        
        # Retriever
        try:
            vector_store = Neo4jVector.from_existing_index(
                embedding=embedding_model,
                url=NEO4J_URI,
                username=NEO4J_USERNAME,
                password=NEO4J_PASSWORD,
                database=NEO4J_DATABASE,
                index_name="vector",
                node_label="Chunk",
                text_node_property="text",
                embedding_node_property="embedding",
                retrieval_query=VECTOR_GRAPH_SEARCH_QUERY
            )
            
            retriever = vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.1, "k": 30}
            )
            app.state.retriever = retriever
            logging.info("✅ Retriever ready")
        except Exception as ve:
            logging.warning(f"⚠️ Vector retriever init warning (will retry on query): {ve}")
            app.state.retriever = None
        
        # Start keep-alive thread for Render deployment
        if os.getenv('RENDER_EXTERNAL_URL'):
            keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
            keep_alive_thread.start()
            logging.info("✅ Keep-alive thread started for Render deployment")
        
        logging.info("🎉 Initialization complete!")
        
    except Exception as e:
        logging.error(f"❌ Startup failed: {e}")
        raise
    
    yield
    
    if hasattr(app.state, 'graph'):
        try:
            app.state.graph._driver.close()
        except:
            pass

def keep_alive():
    """Keep the server awake by calling health endpoint every 15 minutes."""
    import time
    import requests
    
    # Wait 5 minutes before starting keep-alive (let server fully start)
    time.sleep(300)
    
    while True:
        try:
            # Determine the URL - use environment variable if available
            base_url = os.getenv('RENDER_EXTERNAL_URL', 'http://localhost:8001')
            health_url = f"{base_url}/health"
            
            response = requests.get(health_url, timeout=10)
            if response.status_code == 200:
                logging.info(f"✅ Keep-alive ping successful: {health_url}")
            else:
                logging.warning(f"⚠️ Keep-alive ping returned status {response.status_code}")
        except Exception as e:
            logging.error(f"❌ Keep-alive ping failed: {e}")
        
        # Wait 15 minutes (900 seconds) before next ping
        time.sleep(900)

app = FastAPI(
    title="Mahabharata Wisdom Sage AI - Ultra Optimized",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    sources: List[str]
    total_tokens: int
    model: str
    time_taken: float

class AudioRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Mahabharata Wisdom Sage AI - Ultra Optimized"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "gpt-5.2"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """Ultra-optimized chat with in-memory sessions."""
    total_start = time.time()
    
    try:
        retriever = request.app.state.retriever
        llm = request.app.state.llm
        
        # Session (now < 0.001s)
        session_start = time.time()
        session_id = get_or_create_session(chat_request.session_id)
        session = memory_sessions[session_id]
        session.add_user_message(chat_request.message)
        messages = session.get_messages()
        session_time = time.time() - session_start
        logging.info(f"⏱️  Session setup: {session_time:.3f}s")
        
        # Retrieval
        retrieval_start = time.time()
        docs = []
        try:
            if retriever:
                docs = retriever.invoke(chat_request.message)
            else:
                logging.warning("⚠️ Retriever not initialized, proceeding with empty context")
        except Exception as re:
            logging.warning(f"⚠️ Vector retrieval error or rate limit: {re}")
            docs = []
        retrieval_time = time.time() - retrieval_start
        logging.info(f"⏱️  Retrieval: {retrieval_time:.3f}s ({len(docs)} docs)")
        
        # Process
        response = process_documents_fast(docs, chat_request.message, messages, llm)
        
        # Update session
        session.add_ai_message(response['message'])
        
        total_time = time.time() - total_start
        logging.info(f"⏱️  TOTAL TIME: {total_time:.3f}s")
        
        return ChatResponse(
            message=response['message'],
            session_id=session_id,
            sources=response['sources'],
            total_tokens=response['total_tokens'],
            model=response['model'],
            time_taken=total_time
        )
        
    except Exception as e:
        logging.error(f"❌ Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/{session_id}")
async def clear_chat_session(session_id: str):
    if session_id in memory_sessions:
        memory_sessions[session_id].clear()
        return {"message": "Session cleared"}
    raise HTTPException(status_code=404, detail="Session not found")

@app.get("/examples")
async def get_examples():
    return {
        "examples": [
            "Why did the Mahabharata war happen?",
            "Who killed Karna, and why?",
            "Why did the Pandavas have to go live in the forest for 12 years?",
            "Who was the wife of all five Pandavas, and how did that marriage come to be?",
            "What was the role of Krishna during the Kurukshetra war? Did he fight?",
            "Describe the relationship between Karna and Kunti. How did it affect the war?",
            "Who killed Ghatotakach?",
            "Who were the siblings of Karna?",
            "Why did Bhishma take a vow of celibacy, and how did that impact the throne of Hastinapur?",
            "Who killed Dronacharya and how was he tricked into giving up his weapons?"
        ]
    }

@app.post("/audio/english")
async def generate_english_audio(request: AudioRequest):
    """Audio generation endpoint for English using Sarvam AI."""
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="No text provided")
        text = request.text.split("(Model:")[0].strip() if "(Model:" in request.text else request.text
        
        SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
        if not SARVAM_API_KEY:
            raise HTTPException(status_code=500, detail="SARVAM_API_KEY not configured")
        
        client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
        tts_response = client.text_to_speech.convert(
            text=text,
            target_language_code="en-IN",
            speaker="shubh",
            pace=1.1,
            speech_sample_rate=22050,
            enable_preprocessing=True,
            model="bulbul:v3-beta"
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            if hasattr(tts_response, 'audios') and tts_response.audios:
                audio_bytes = base64.b64decode(tts_response.audios[0])
                f.write(audio_bytes)
                audio_path = f.name
                logging.info(f"Generated English audio file: {audio_path}")
            else:
                raise HTTPException(status_code=500, detail="No audio data received from TTS API")
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="english_audio.mp3"
        )
    except Exception as e:
        logging.error(f"❌ English Audio error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/tamil")
async def generate_tamil_audio(request: AudioRequest):
    """Audio generation endpoint for Tamil using Sarvam AI."""
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="No text provided")
        text = request.text.split("(Model:")[0].strip() if "(Model:" in request.text else request.text
        
        SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
        if not SARVAM_API_KEY:
            raise HTTPException(status_code=500, detail="SARVAM_API_KEY not configured")
        
        client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
        translation_response = client.text.translate(
            input=text,
            source_language_code="en-IN",
            target_language_code="ta-IN",
            speaker_gender="Male",
            mode="formal",
            model="sarvam-translate:v1",
            numerals_format="native"
        )
        translated_text = translation_response.translated_text
        
        tts_response = client.text_to_speech.convert(
            text=translated_text,
            target_language_code="ta-IN",
            speaker="shubh",
            pace=1.1,
            speech_sample_rate=22050,
            enable_preprocessing=True,
            model="bulbul:v3-beta"
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            if hasattr(tts_response, 'audios') and tts_response.audios:
                audio_bytes = base64.b64decode(tts_response.audios[0])
                f.write(audio_bytes)
                audio_path = f.name
                logging.info(f"Generated Tamil audio file: {audio_path}")
            else:
                raise HTTPException(status_code=500, detail="No audio data received from TTS API")
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="tamil_audio.mp3"
        )
    except Exception as e:
        logging.error(f"❌ Tamil Audio error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/hindi")
async def generate_hindi_audio(request: AudioRequest):
    """Audio generation endpoint using Sarvam AI."""
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        text = request.text.split("(Model:")[0].strip() if "(Model:" in request.text else request.text
        
        # # Limit text length for Sarvam AI translation (mayura:v1 has 1000 character limit)
        # MAX_TRANSLATION_LENGTH = 950  # Leave some buffer
        # if len(text) > MAX_TRANSLATION_LENGTH:
        #     text = text[:MAX_TRANSLATION_LENGTH].rsplit(' ', 1)[0]  # Truncate at word boundary
        #     logging.info(f"Text truncated to {len(text)} characters for translation")
        
        # Get Sarvam AI API key
        SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
        if not SARVAM_API_KEY:
            raise HTTPException(status_code=500, detail="SARVAM_API_KEY not configured")
        
        # Initialize Sarvam AI client
        client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
        
        # Translate text to Hindi
        translation_response = client.text.translate(
            input=text,
            source_language_code="en-IN",
            target_language_code="hi-IN",
            speaker_gender="Male",
            mode="formal",
            model="sarvam-translate:v1",
            numerals_format="native"
        )
        
        # Extract translated text from the response
        translated_text = translation_response.translated_text
        
        # Convert text to speech using bulbul:v3-beta (supports up to 2500 characters)
        tts_response = client.text_to_speech.convert(
            text=translated_text,
            target_language_code="hi-IN",
            speaker="shubh",
            pace=1.1,
            speech_sample_rate=22050,
            enable_preprocessing=True,
            model="bulbul:v3-beta"
        )
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            if hasattr(tts_response, 'audios') and tts_response.audios:
                # Decode base64 audio data and write to file
                audio_bytes = base64.b64decode(tts_response.audios[0])
                f.write(audio_bytes)
                audio_path = f.name
                logging.info(f"Generated audio file: {audio_path}")
            else:
                raise HTTPException(status_code=500, detail="No audio data received from TTS API")
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="hindi_audio.mp3"
        )
        
        # COMMENTED OUT: Original ElevenLabs + Google Translate implementation
        # project_id = os.getenv("PROJECT_ID")
        # if not project_id:
        #     raise HTTPException(status_code=500, detail="PROJECT_ID not configured")
        # 
        # client = translate.TranslationServiceClient()
        # parent = f"projects/{project_id}/locations/global"
        # 
        # response = client.translate_text(
        #     parent=parent,
        #     contents=[text],
        #     mime_type="text/plain",
        #     source_language_code="en-US",
        #     target_language_code="hi",
        # )
        # translated_text = response.translations[0].translated_text
        # 
        # ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
        # if not ELEVENLABS_API_KEY:
        #     raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY not configured")
        # 
        # elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        # audio_generator = elevenlabs_client.text_to_speech.convert(
        #     text=translated_text,
        #     voice_id="MF4J4IDTRo0AxOO4dpFR",
        #     model_id="eleven_multilingual_v2",
        #     output_format="mp3_44100_128",
        # )
        # audio_bytes = b"".join(audio_generator)
        # 
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        #     f.write(audio_bytes)
        #     audio_path = f.name
        # 
        # return FileResponse(
        #     audio_path,
        #     media_type="audio/mpeg",
        #     filename="hindi_audio.mp3"
        # )
        
    except Exception as e:
        logging.error(f"❌ Audio error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)