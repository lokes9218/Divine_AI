Dive into the timeless wisdom of an ancient Indian epic! Ask questions, explore characters, unravel mysteries, and gain insights from the vast knowledge powered by AI and graph databases.

## 🌟 Features

- **🤖 OpenAI Powered**: Advanced AI responses using OpenAI's GPT models
- **🗄️ Graph Database**: Neo4j-powered knowledge graph for rich contextual information
- **🎨 Modern UI**: Beautiful Nuxt.js frontend with responsive design
- **🚀 FastAPI Backend**: High-performance API with automatic documentation
- **🇮🇳 Hindi Audio**: Listen to responses in Hindi using Sarvam AI TTS
- **📱 Responsive**: Works perfectly on desktop and mobile devices
- **🔍 Source Attribution**: See exactly where information comes from
- **💬 Session Management**: Maintains conversation context with automatic summarization
- **🌐 Live Demo**: Ready-to-use deployment on Netlify

## 🏗️ Architecture

This project follows a modern, scalable architecture with separate frontend and backend services:

### Backend (`backend/`)
- **FastAPI** server with automatic API documentation
- **OpenAI integration** for advanced language processing
- **Neo4j GraphRAG** for graph-based retrieval augmented generation
- **Session management** with automatic conversation summarization
- **Sarvam AI integration** for Hindi translation and text-to-speech
- **CORS enabled** for frontend integration

### Frontend (`frontend/`)
- **Nuxt.js 3** application with TypeScript support
- **Tailwind CSS** for modern, responsive styling
- **Custom chat interface** with real-time interactions
- **Audio playback** for Hindi responses
- **Mobile-first responsive design**

## 🚀 Live Demo

🎯 

## 💻 Local Development

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database** (with Mahabharata data loaded)
- **OpenAI API Key**
- **Sarvam AI API Key** (for Hindi translation and audio)

## Background

## 🚀 Deployment

This application supports modern cloud deployment with separate backend and frontend services:
- **Backend**: Compatible with Render, Railway, or any FastAPI-supporting platform
- **Frontend**: Deployable on Netlify, Vercel, or similar static hosting services
- **Database**: Neo4j AuraDB for managed cloud database

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 💻 Local Development

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database** (with your Mahabharata data loaded)
- **OpenAI API Key**
- **Sarvam AI API Key** (for Hindi translation and audio)

### Backend Setup

1. **Clone and navigate to the project**:
```bash
git clone https://github.com/lokes9218/Divine_AI.git
cd mahabharata-genai/backend
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp example.backend.env .env
# Edit .env with your API keys and database credentials
```

5. **Start the backend server**:
```bash
uvicorn main:app --reload --port 8001
```

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment**:
```bash
cp example.frontend.env .env
# Edit .env with your backend URL
```

4. **Start development server**:
```bash
npm run dev
```

### Database Setup

1. **Install Neo4j**: Follow the official [Neo4j installation guide](https://neo4j.com/docs/operations-manual/current/installation/)
2. **Load Mahabharata data**: Use the provided [mahabharata-db-setup.cypher](backend/mahabharata-db-setup.cypher) script
3. **Configure connection**: Update your `.env` file with Neo4j credentials

### Environment Configuration

**Backend Environment (`backend/.env`)**:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=neo4j

# Sarvam AI (for Hindi features)
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional: Google Cloud Project ID
PROJECT_ID=your_google_cloud_project_id
```

**Frontend Environment (`frontend/.env`)**:
```env
# Backend API URL
API_BASE_URL=http://localhost:8001
```

## 🌍 Background & Story



This journey evolved from exploring the Mahabharata through graph theory to creating an innovative Neo4j-powered chatbot that makes the epic's complex relationships accessible to everyone.

### 📖 Blog Series



## 🚀 Deployment

This application supports modern cloud deployment with separate backend and frontend services:

- **Backend**: Compatible with Render, Railway, or any FastAPI-supporting platform
- **Frontend**: Deployable on Netlify, Vercel, or similar static hosting services
- **Database**: Neo4j AuraDB for managed cloud database

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🤝 Contributing

We welcome contributions to make the Mahabharata chatbot the best resource for exploring this epic tale! 



**Contributing Guidelines**:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to your branch: `git push origin feature/YourFeature`
5. Create a pull request

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

## 🙏 Acknowledgements

Special thanks to:


---

⭐ **If you find this project helpful, please give it a star!** ⭐
