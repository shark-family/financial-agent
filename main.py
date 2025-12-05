import os
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# main.py가 있는 폴더 경로 (여기 안에 financial_advisor 패키지가 있음)
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 세션 저장용 DB (간단하게 SQLite)
SESSION_DB_URL = "sqlite:///./sessions.db"

# CORS 허용 도메인 (나중에 프론트 붙이면 여기 조정)
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]

# ADK 웹 UI를 같이 띄울지 여부 (True면 /dev-ui 열림)
SERVE_WEB_INTERFACE = True

# ADK에서 FastAPI 앱 만들어주는 헬퍼
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# Render health check
@app.get("/")
def root():
    return {"status": "ok", "message": "CareerCoach API running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
