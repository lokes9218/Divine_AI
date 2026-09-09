# 🕉️ Mahabharata Wisdom Mentor

> Explore the timeless wisdom of the Mahabharata through AI-powered conversations, character relationships, and knowledge from a graph database.

Mahabharata Wisdom Mentor is an AI-powered application that makes the vast knowledge of the Mahabharata accessible through an interactive chatbot. Users can ask questions, explore characters, understand relationships, unravel mysteries, and gain insights from the epic in **Tamil and English**.

The application combines **Google Gemini, Neo4j GraphRAG, and a modern Nuxt.js interface** to provide contextual and engaging answers.

![Mahabharata Wisdom Mentor](https://github.com/user-attachments/assets/7d9da36c-dfff-46cd-8dce-2c11fbebcaf8)

## 🌟 Features

- **🤖 Google Gemini Powered**: AI-powered responses using Google Gemini models.
- **🗄️ Graph Database**: Neo4j-powered knowledge graph for rich contextual information.
- **🎨 Modern UI**: Beautiful Nuxt.js frontend with responsive design.
- **🚀 FastAPI Backend**: High-performance API with automatic documentation.
- **🌐 Tamil & English**: Ask questions and explore the Mahabharata in Tamil and English.
- **🔊 Tamil Audio**: Listen to responses in Tamil using Sarvam AI TTS.
- **📱 Responsive**: Works on desktop and mobile devices.
- **🔍 Source Attribution**: See exactly where information comes from.
- **💬 Session Management**: Maintains conversation context with automatic summarization.
- **🧠 Contextual Knowledge**: Uses graph-based retrieval to connect characters, events, and relationships.
- **🚀 Cloud Deployment**: Supports separate frontend, backend, and database deployment.

## 🏗️ Architecture

This project follows a modern, scalable architecture with separate frontend and backend services.

```text
┌──────────────────────────────────────────────┐
│              Mahabharata Wisdom Mentor       │
└──────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              Nuxt.js Frontend                │
│         TypeScript + Tailwind CSS            │
│          Chat Interface + Audio              │
└──────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              FastAPI Backend                 │
│       API Routes + Session Management        │
│       Gemini Integration + GraphRAG          │
└──────────────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐
│    Google Gemini     │  │    Neo4j Database    │
│   AI Responses       │  │  Mahabharata Graph   │
└──────────────────────┘  └──────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────┐
│              Sarvam AI                       │
│          Tamil Translation & TTS             │
└──────────────────────────────────────────────┘
```

## 📂 Project Structure

```text
mahabharata-genai/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   ├── example.backend.env
│   ├── mahabharata-db-setup.cypher
│   └── ...
│
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── assets/
│   ├── public/
│   ├── nuxt.config.ts
│   ├── package.json
│   ├── .env
│   ├── example.frontend.env
│   └── ...
│
├── DEPLOYMENT.md
└── README.md
```

## 🏗️ Backend

The backend is built using **FastAPI** and provides the API services required by the frontend.

### Backend Technologies

- **FastAPI** – High-performance backend framework.
- **Python** – Backend programming language.
- **Google Gemini** – AI-powered language processing.
- **Neo4j GraphRAG** – Graph-based retrieval augmented generation.
- **Neo4j** – Knowledge graph database.
- **Sarvam AI** – Tamil translation and text-to-speech.
- **Session Management** – Maintains conversation context.
- **CORS** – Enables frontend integration.
- **Automatic API Documentation** – FastAPI documentation support.

### Backend Responsibilities

- Receives user questions from the frontend.
- Retrieves relevant information from the Neo4j knowledge graph.
- Uses Google Gemini to generate contextual responses.
- Maintains conversation sessions.
- Summarizes conversations automatically when required.
- Supports Tamil translation and audio generation.
- Provides API endpoints for frontend communication.

## 🎨 Frontend

The frontend is built using **Nuxt.js 3** with TypeScript and Tailwind CSS.

### Frontend Technologies

- **Nuxt.js 3**
- **Vue.js**
- **TypeScript**
- **Tailwind CSS**
- **Responsive UI**
- **Custom Chat Interface**
- **Audio Playback**

### Frontend Responsibilities

- Provides the user interface for asking questions.
- Displays AI-generated responses.
- Supports Tamil and English interactions.
- Displays source attribution.
- Provides audio playback for Tamil responses.
- Maintains a responsive experience across devices.

## 🗄️ Database

The project uses **Neo4j** as its graph database.

The knowledge graph stores Mahabharata-related information such as:

- Characters
- Relationships
- Events
- Battles
- Locations
- Connections between characters and events

This graph-based structure helps the application retrieve relevant contextual information before generating answers.

### Database Setup

The project includes a Cypher script for loading the Mahabharata data:

```text
backend/mahabharata-db-setup.cypher
```

## 🤖 AI Integration

### Google Gemini

Google Gemini is used for advanced language processing and AI-generated responses.

The application uses Gemini to:

- Understand user questions.
- Generate contextual answers.
- Explain Mahabharata characters and events.
- Answer questions using retrieved graph information.
- Maintain conversational context.

### Neo4j GraphRAG

Neo4j GraphRAG combines graph-based retrieval with generative AI.

```text
User Question
      │
      ▼
Retrieve Relevant Graph Information
      │
      ▼
Neo4j Knowledge Graph
      │
      ▼
Google Gemini
      │
      ▼
Contextual AI Response
```

### Sarvam AI

Sarvam AI is used for Tamil language support.

The application supports:

- Tamil translation.
- Tamil text-to-speech.
- Audio playback of Tamil responses.

## 🌐 Supported Languages

Mahabharata Wisdom Mentor supports:

- **English**
- **Tamil**

Users can explore the Mahabharata in both languages through the chatbot.

## 🚀 Live Demo

🎯 **Live Demo:** (https://divine-ai-frontend.onrender.com/)

## 💻 Local Development

### Prerequisites

Before running the project locally, make sure you have:

- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database**
- **Mahabharata data loaded into Neo4j**
- **Google Gemini API Key**
- **Sarvam AI API Key** *(for Tamil translation and audio)*

## 📥 Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/lokes9218/Divine_AI.git
cd mahabharata-genai/backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

**Windows:**

```powershell
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp example.backend.env .env
```

Then edit the `.env` file with your API keys and database credentials.

### 5. Start the Backend Server

```bash
uvicorn main:app --reload --port 8001
```

The backend will run at:

```text
http://localhost:8001
```

FastAPI documentation will be available at:

```text
http://localhost:8001/docs
```

## 🎨 Frontend Setup

### 1. Navigate to the Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Copy the example frontend environment file:

```bash
cp example.frontend.env .env
```

Then configure the backend URL.

### 4. Start the Development Server

```bash
npm run dev
```

The frontend will be available at the URL shown by Nuxt.

## 🗄️ Database Setup

### 1. Install Neo4j

Follow the official Neo4j installation guide:

https://neo4j.com/docs/operations-manual/current/installation/

### 2. Load Mahabharata Data

Use the provided Cypher script:

```text
backend/mahabharata-db-setup.cypher
```

### 3. Configure the Database Connection

Update the Neo4j credentials in your backend `.env` file.

## 🔐 Environment Configuration

### Backend Environment

Create a `.env` file inside the `backend/` directory.

```env
# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=neo4j

# Sarvam AI (for Tamil features)
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional: Google Cloud Project ID
PROJECT_ID=your_google_cloud_project_id
```

### Frontend Environment

Create a `.env` file inside the `frontend/` directory.

```env
# Backend API URL
API_BASE_URL=http://localhost:8001
```

> **Note:** Keep your API keys private. Do not commit your `.env` files to GitHub.

## 🌍 Background & Story

This journey evolved from exploring the Mahabharata through graph theory to creating an innovative Neo4j-powered chatbot that makes the epic's complex relationships accessible to everyone.

The project combines the timeless knowledge of the Mahabharata with modern AI and graph database technologies to create an interactive learning experience.

Users can ask questions, explore characters, understand relationships, and gain insights from the epic through a conversational interface.

## 📖 Blog Series

This project is part of a learning journey exploring the Mahabharata through **graph theory, knowledge graphs, and generative AI**.

### Blog Series

- Coming soon.

## 🚀 Deployment

This application supports modern cloud deployment with separate frontend and backend services.

### Backend

Compatible with:

- **Render**
- **Railway**
- Other FastAPI-supporting platforms

### Frontend

Deployable on:

- **Netlify**
- **Vercel**
- Similar static hosting platforms

### Database

The application can use:

- **Neo4j AuraDB** for managed cloud database hosting.

### Deployment Architecture

```text
┌──────────────────────┐
│   Frontend Hosting   │
│   Netlify / Vercel   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Backend Hosting    │
│  Render / Railway    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Neo4j AuraDB     │
│   Managed Database   │
└──────────────────────┘
```

For complete deployment instructions, see:

```text
DEPLOYMENT.md
```

## 🧪 Development Workflow

```text
1. Clone the repository
        ↓
2. Set up the backend
        ↓
3. Configure Google Gemini API
        ↓
4. Configure Neo4j database
        ↓
5. Load Mahabharata data
        ↓
6. Set up the frontend
        ↓
7. Configure backend API URL
        ↓
8. Run the application
        ↓
9. Ask questions in Tamil or English
```

## 🤝 Contributing

We welcome contributions to make **Mahabharata Wisdom Mentor** a better resource for exploring the Mahabharata.

### Contributing Guidelines

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/YourFeature
```

3. Make your changes.
4. Commit your changes:

```bash
git commit -m "Add some feature"
```

5. Push to your branch:

```bash
git push origin feature/YourFeature
```

6. Create a pull request.

## 📄 License

This project is licensed under the **Apache License 2.0**.

See the `LICENSE` file for more information.

## 🙏 Acknowledgements

Special thanks to the technologies and tools that made this project possible:

- **Google Gemini** – AI-powered language processing.
- **Neo4j** – Graph database and knowledge graph.
- **FastAPI** – Backend API framework.
- **Nuxt.js** – Frontend framework.
- **Tailwind CSS** – UI styling.
- **Sarvam AI** – Tamil translation and text-to-speech.

## ⭐ Support

If you find **Mahabharata Wisdom Mentor** helpful, please give the repository a star!

---

**Mahabharata Wisdom Mentor**  
*Explore the epic. Understand the relationships. Discover the wisdom.*
**DONE BY LOKESWARAN S**
