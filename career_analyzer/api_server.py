# career_analyzer/api_server.py
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from client import GeminiClient
from prompt_builder import PromptBuilder
from parser import ResponseParser
from models import AnalysisInput, UserProfile, AnalysisOutput


# ========== 1. 요청/응답 스키마 (프론트용) ==========

class AnalyzeRequest(BaseModel):
    company_name: str   # 회사명
    job_role: str       # 직무명
    skills: List[str]   # 보유 기술 배열
    experiences: List[str]  # 주요 경력 배열


# AnalysisOutput은 models.py에 이미 있으니까 그대로 응답에 사용


# ========== 2. FastAPI 앱 설정 ==========

app = FastAPI(title="Career Analyzer API", version="1.0.0")

# CORS 설정 (프론트 로컬 개발용)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ========== 3. 메인 분석 엔드포인트 ==========

@app.post("/analyze", response_model=AnalysisOutput)
async def analyze(req: AnalyzeRequest):
    """
    프론트에서:
    POST /analyze
    {
      "company_name": "삼성전자",
      "job_role": "소프트웨어 개발",
      "skills": ["Java", "Spring Boot", "AWS"],
      "experiences": ["신입사UP 서비스 1인 개발 및 운영"]
    }
    """
    # 1) 내부 모델로 변환
    user_profile = UserProfile(
        skills=req.skills,
        experiences=req.experiences,
    )
    analysis_input = AnalysisInput(
        company_name=req.company_name,
        job_role=req.job_role,
        user_profile=user_profile,
    )

    # 2) 프롬프트 생성
    prompt = PromptBuilder.build_prompt(analysis_input)

    # 3) Gemini 호출
    client = GeminiClient()
    response_text = client.request(prompt)

    # 4) JSON 파싱 → AnalysisOutput
    parsed = ResponseParser.parse(response_text)

    # 5) 그대로 반환 (FastAPI가 JSON으로 직렬화)
    return parsed


# ========== 4. 로컬에서 직접 실행할 때 ==========

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
