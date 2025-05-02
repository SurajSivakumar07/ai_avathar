Lightweight AI Coach Orchestrator
Overview
The Lightweight AI Coach Orchestrator is a FastAPI-based prototype that enables students to interact with two AI coaches (Coach Tara and Coach Ravi) via text or audio. Users select an age group (Grade 6-8 or 9-12), mentor role, tone, and language to receive personalized coaching. The system routes conversations to the appropriate coach, manages session memory using Qdrant, and supports audio input via OpenAI Whisper. It is designed for simplicity and modularity, with optional features like text-to-speech and avatars left for future implementation.
Architecture Overview
The system comprises the following components:

Frontend: Basic HTML/JS/React UI (optional, not implemented) for selecting age group, mentor role, tone, and language.
FastAPI Application: Handles endpoints (/start_session, /chat, /set_goal, /switch_coach, /audio_chat) for session management, text/audio chat, and goal setting.
Orchestration Layer: Rule-based router selects Coach Tara (Grade 6-8, supportive roles) or Coach Ravi (Grade 9-12, academic/career roles) based on age group and role.
Coach Agents: Two agents (Tara: soft, calming; Ravi: energetic, exam-focused) generate responses using persona-specific prompts.
AI Processing: OpenAI Whisper for speech-to-text (audio input). LLM integration (assumed OpenAI GPT) in coach prompt functions.
Memory Layer: Qdrant stores session data (session ID, coach, goals, etc.) for continuity within a 10-minute session.
Hosting: Runs on localhost (Qdrant data stored locally).

The architecture diagram (not included here) illustrates the data flow from user input to coach responses, with Qdrant for memory and OpenAI for audio processing.
Setup Instructions
Prerequisites

Python 3.8+
pip for installing dependencies
OpenAI API key (for Whisper)
Optional: .env file for environment variables

Installation

Clone the Repository:
git clone <repository-url>
cd lightweight-ai-coach-orchestrator


Install Dependencies:
pip install fastapi uvicorn qdrant-client openai python-dotenv pydantic

Note: Additional dependencies (e.g., for micro_coaches) may be required based on get_tara_prompt and get_ravi_prompt implementations.

Set Up Environment Variables:Create a .env file in the project root:
OPENAI_API_KEY=your-openai-api-key

Replace your-openai-api-key with your actual OpenAI API key.

Initialize Qdrant:The application uses a local Qdrant instance (stored in ./qdrant_data). No additional setup is required, as the code initializes the session_memory collection automatically.

Run the Application:
uvicorn main:app --reload

The API will be available at http://localhost:8000.


Project Structure
lightweight-ai-coach-orchestrator/
├── main.py               # FastAPI application
├── micro_coaches/        # Coach prompt functions (tara.py, ravi.py)
├── qdrant_data/          # Local Qdrant storage
├── .env                  # Environment variables
└── README.md             # This file

Usage

Start a Session:Send a POST request to /start_session:
curl -X POST http://localhost:8000/start_session \
-H "Content-Type: application/json" \
-d '{"age_group": "Grade 9-12", "coach": "ravi", "role": "Career Compass", "tone": "Wise", "language": "English"}'

Response: {"session_id": "<uuid>", "message": "Session started with ravi"}

Chat:Send a POST request to /chat:
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "<session_id>", "message": "What stream should I choose?"}'

Response: {"response": "<coach_response>"}

Audio Chat:Send a POST request to /audio_chat with an audio file:
curl -X POST http://localhost:8000/audio_chat?session_id=<session_id> \
-F "file=@/path/to/audio.wav"

Response: {"transcript": "<transcribed_text>", "response": "<coach_response>"}

Set Goal:Send a POST request to /set_goal:
curl -X POST http://localhost:8000/set_goal \
-H "Content-Type: application/json" \
-d '{"session_id": "<session_id>", "goal": "Prepare for engineering exams"}'


Switch Coach:Send a POST request to /switch_coach:
curl -X POST http://localhost:8000/switch_coach \
-H "Content-Type: application/json" \
-d '{"session_id": "<session_id>", "new_coach": "tara"}'



Notes

Limitations:
Text-to-speech (TTS) and avatar integration are not implemented (marked optional in the requirements).
Recommendations (books, courses, test prep) depend on micro_coaches implementation.
Frontend UI is not included; use API calls or build a basic HTML/JS interface.


Future Improvements:
Add TTS (e.g., ElevenLabs) for audio responses.
Implement dynamic recommendations in coach prompts.
Develop a React/Streamlit frontend for user interaction.


Troubleshooting:
Ensure the OpenAI API key is valid for Whisper transcription.
Check micro_coaches for missing prompt functions.
Verify Qdrant data directory permissions.



For detailed architecture, refer to the system architecture diagram (available separately).
