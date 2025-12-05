# models.py
from pydantic import BaseModel
from typing import List


class UserProfile(BaseModel):
    skills: List[str]
    experiences: List[str]


class AnalysisInput(BaseModel):
    company_name: str
    job_role: str
    user_profile: UserProfile


class SectionOutput(BaseModel):
    title: str
    content: str


class RelatedNews(BaseModel):
    title: str
    url: str
    source: str
    reason: str


class JobDeepDive(BaseModel):
    title: str
    overview: str
    main_tasks: List[str]      # 주요 업무
    required_skills: List[str] # 요구 역량
    career_path: List[str]     # 커리어 경로


class SeniorFitOutput(BaseModel):
    title: str
    strengths: str       # 강점
    key_challenges: str  # 핵심 과제


class AnalysisOutput(BaseModel):
    company_info: SectionOutput
    financial_status: SectionOutput
    trends: SectionOutput
    job_analysis: JobDeepDive
    senior_fit: SeniorFitOutput
    coach_tip: SectionOutput
    related_news: List[RelatedNews]
