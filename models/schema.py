from pydantic import BaseModel

class StartSessionRequest(BaseModel):
    age_group: str
    coach: str
    role: str
    tone: str
    language: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

class SetGoalRequest(BaseModel):
    session_id: str
    goal: str

class SwitchCoachRequest(BaseModel):
    session_id: str
    new_coach: str