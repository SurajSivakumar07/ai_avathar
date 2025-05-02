##  Lightweight AI Coach Orchestrator


**Overview**

The Lightweight AI Coach Orchestrator is a FastAPI-based prototype that enables students to interact with two AI coaches (Coach Tara and Coach Ravi) via text or audio. Users select an age group (Grade 6-8 or 9-12), mentor role, tone, and language to receive personalized coaching. The system routes conversations to the appropriate coach, manages session memory using Qdrant, and supports audio input via OpenAI Whisper. It is designed for simplicity and modularity, with optional features like text-to-speech and avatars left for future implementation.
Architecture Overview
The system comprises the following components:

 **Frontend:**

The frontend is built using Streamlit, where users can start a session by selecting their age group, mentor role, tone, and language. Users can then set goals, engage in real-time text or audio chat, and switch between different coach personas.

The **backend** is powered by a FastAPI application exposing endpoints like /start_session, /chat, /set_goal, /switch_coach, and /audio_chat. A rule-based orchestration layer assigns either Coach Tara or Coach Ravi based on the user's age and selected role. Coach Tara provides a soft, calming experience for younger students (Grades 6–8) in supportive roles, while Coach Ravi is tailored for older students (Grades 9–12) with a more energetic and exam-oriented focus. Both coaches use persona-specific prompts built on top of an LLM (model_name=gpt-3.5-turbo).

For audio input, the system integrates OpenAI Whisper for speech-to-text transcription. A memory layer using Qdrant stores session-related data—such as session ID, goals, and coach identity—to maintain conversational. The entire application, including Streamlit, FastAPI, and Qdrant, runs locally during development.
Manages
##  Installation 
```bash

Clone the Repository:
git clone https://github.com/SurajSivakumar07/ai_avathar
cd ai_avathar
 ```

## Setup
Set Up Environment Variables:Create a .env file in the project root:
OPENAI_API_KEY=your-openai-api-key

Replace your-openai-api-key with your actual OpenAI API key.

Initialize Qdrant:The application uses a local Qdrant instance (stored in ./qdrant_data). No additional setup is required, as the code initializes the session_memory collection automatically.

## Install Dependencies:
```bash

pip install -r requirements

Run the Application:
 uvicorn orchestrator.main:app --reload --port 8000
      
For streamlit:
  cd front_end
  streamlit run app.py --server.port 8501   
  
```
The API will be available at http://localhost:8000.

The Streamlit will be available at http://localhost:8501.
 
