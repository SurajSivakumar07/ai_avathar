from fastapi import FastAPI, File, UploadFile
from uuid import uuid4

from coach_selection.select_coach import select_coach
from memory.session_memory import qdrant, collection_name, embed_text
from micro_coaches.coach_tara import get_tara_prompt
from micro_coaches.coach_ravi import get_ravi_prompt
from qdrant_client.models import PointStruct
import os
import hashlib
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import openai
import logging

from models.schema import StartSessionRequest, SetGoalRequest, SwitchCoachRequest, ChatRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app = FastAPI()
load_dotenv()

#open aikey
openai.api_key = os.getenv("OPENAI_API_KEY")

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/start_session")
def start_session(req: StartSessionRequest):
    print(f"Starting session with request: {req}")
    session_id = str(uuid4())

    coach = select_coach(req.age_group, req.role)

    payload = {
        "age_group": req.age_group,
        "coach": coach,
        "tone": req.tone,
        "language": req.language,
        "role": req.role,
        "goal": ""
    }

    print(f"Upserting session_id: {session_id} with payload: {payload}")
    qdrant.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=session_id, vector=embed_text(session_id), payload=payload)]
    )
    print(f"Session created: {session_id}")
    print(coach)
    return {"session_id": session_id, "message": f"Session started with {coach}"}

@app.post("/set_goal")
def set_goal(req: SetGoalRequest):
    print(f"[SET GOAL] Session ID: {req.session_id}, Goal: {req.goal}")
    try:
        result, _ = qdrant.scroll(collection_name=collection_name)
        print(f"[SET GOAL] Total sessions found in Qdrant: {len(result)}")

        for point in result:
            print(f"[SET GOAL] Checking point ID: {point.id}")
            if str(point.id) == req.session_id:
                payload = point.payload
                if not payload:
                    print(f"[SET GOAL] Payload missing for session_id: {req.session_id}")
                    return {"error": "Session found but missing data."}

                role = payload.get("role", "").strip().lower()
                coach = select_coach(role)
                payload["goal"] = req.goal
                payload["coach"] = coach  # <-- Also update coach here!

                print(f"[SET GOAL] Updating payload: {payload}")
                qdrant.upsert(
                    collection_name=collection_name,
                    points=[
                        PointStruct(
                            id=req.session_id,
                            vector=embed_text(req.session_id),
                            payload=payload
                        )
                    ]
                )
                return {"message": "Goal updated.", "coach": coach}

        print(f"[SET GOAL] No session matched for ID: {req.session_id}")
        return {"error": "Session not found"}

    except Exception as e:
        print(f"[SET GOAL ERROR] {str(e)}")
        return {"error": f"Failed to update goal: {str(e)}"}


@app.post("/switch_coach")
def switch_coach(req: SwitchCoachRequest):
    print(f"[SWITCH COACH] Requested session_id: {req.session_id}, new coach: {req.new_coach}")
    result, _ = qdrant.scroll(collection_name=collection_name)
    print(f"[SWITCH COACH] Total points found: {len(result)}")
    for point in result:
        print(f"[SWITCH COACH] Checking point.id: {point.id}")
        if str(point.id) == req.session_id:
            payload = point.payload or {}
            payload["coach"] = req.new_coach
            qdrant.upsert(
                collection_name=collection_name,
                points=[PointStruct(id=req.session_id, vector=embed_text(req.session_id), payload=payload)]
            )
            return {
                "message": f"Coach switched to {req.new_coach}",
                "coach": req.new_coach
            }
    print(f"[SWITCH COACH] No matching session found for {req.session_id}")
    return {"error": "Session not found"}


@app.post("/chat")
async def process_chat(req: ChatRequest):
    try:
        print(f"Processing chat for session_id: {req.session_id}, message: {req.message}")
        result, _ = qdrant.scroll(collection_name=collection_name)
        print(f"Qdrant sessions found: {len(result)}")
        for point in result:
            if str(point.id) == req.session_id:
                session = point.payload
                coach = session.get("coach")
                tone = session.get("tone", "")
                goal = session.get("goal", "")
                language = session.get("language", "")
                role = session.get("role", "")
                age_group = session.get("age_group", "")
                print(f"Session found: {session}")
                if coach == "tara":
                    response = response = get_tara_prompt(tone, language, goal, role, req.message)

                    print(f"Tara response: {response}")
                    return {"response": response}
                else:
                    response =  get_ravi_prompt(tone, language, goal, role, req.message)
                    print(f"Ravi response: {response}")
                    return {"response": response}
        print(f"Invalid session_id: {req.session_id}")
        return {"error": "Invalid session_id"}
    except Exception as e:
        print(f"Chat processing failed: {str(e)}")
        return {"error": f"Chat processing failed: {str(e)}"}

@app.post("/audio_chat")
async def audio_chat(session_id: str, file: UploadFile = File(...)):
    try:

        print("its inside the audio file path")
        # Save uploaded file temporarily
        audio_path = f"/tmp/{file.filename}"
        with open(audio_path, "wb") as f:
            f.write(await file.read())

        # Transcribe using Whisper via new SDK interface
        with open(audio_path, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        student_message = transcript.text

        # Look up session data from Qdrant
        result, _ = qdrant.scroll(collection_name=collection_name)
        for point in result:
            if str(point.id) == session_id:
                session = point.payload
                coach = session.get("coach")
                tone = session.get("tone", "")
                goal = session.get("goal", "")
                language = session.get("language", "")
                role = session.get("role", "")

                # Route to the appropriate coach
                if coach == "tara":
                    reply = get_tara_prompt(tone, language, goal, role, student_message)
                    print(reply)
                else:
                    reply = get_ravi_prompt(tone, language, goal, role, student_message)
                    print(reply)

                return {
                    "transcript": student_message,
                    "response": reply
                }

        return {"error": "Invalid session_id"}

    except Exception as e:
        return {"error": str(e)}

