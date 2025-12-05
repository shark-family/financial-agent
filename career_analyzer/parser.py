# parser.py
import json
from typing import Any, List

from models import (
    AnalysisOutput,
    SectionOutput,
    RelatedNews,
    JobDeepDive,
    SeniorFitOutput,
)


class ResponseParser:
    @staticmethod
    def _strip_code_fence(text: str) -> str:
        s = text.strip()
        if s.startswith("```"):
            s = s.strip("`")
            if s.lower().startswith("json"):
                s = s[4:].lstrip()
        return s

    @staticmethod
    def _normalize_section(data: dict) -> SectionOutput:
        content = data.get("content", "")
        if isinstance(content, list):
            content = "\n".join(str(c) for c in content)
        elif not isinstance(content, str):
            content = str(content)

        return SectionOutput(
            title=data.get("title", ""),
            content=content,
        )

    @staticmethod
    def _normalize_list(value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(v) for v in value if str(v).strip()]
        if isinstance(value, str):
            # 줄바꿈으로 나눠서 리스트로 만들 수도 있음
            return [line.strip() for line in value.split("\n") if line.strip()]
        if value is None:
            return []
        return [str(value)]

    @staticmethod
    def parse(response_text: str) -> AnalysisOutput:
        cleaned = ResponseParser._strip_code_fence(response_text)

        try:
            data = json.loads(cleaned)
        except Exception as e:
            raise ValueError(f"JSON 파싱 실패: {e}\n원본 응답 일부: {cleaned[:300]}")

        try:
            # 공통 섹션
            company_info = ResponseParser._normalize_section(data["company_info"])
            financial_status = ResponseParser._normalize_section(data["financial_status"])
            trends = ResponseParser._normalize_section(data["trends"])
            coach_tip = ResponseParser._normalize_section(data["coach_tip"])

            # 직무 심층 분석
            ja = data["job_analysis"]
            job_analysis = JobDeepDive(
                title=ja.get("title", "직무 심층 분석"),
                overview=str(ja.get("overview", "")),
                main_tasks=ResponseParser._normalize_list(ja.get("main_tasks", [])),
                required_skills=ResponseParser._normalize_list(
                    ja.get("required_skills", [])
                ),
                career_path=ResponseParser._normalize_list(ja.get("career_path", [])),
            )

            # 시니어/지원자 적합성
            sf = data["senior_fit"]
            strengths = sf.get("strengths", "")
            key_challenges = sf.get("key_challenges", "")

            if isinstance(strengths, list):
                strengths = "\n".join(str(s) for s in strengths)
            if isinstance(key_challenges, list):
                key_challenges = "\n".join(str(s) for s in key_challenges)

            senior_fit = SeniorFitOutput(
                title=sf.get("title", "지원자 강점 및 핵심 과제"),
                strengths=str(strengths),
                key_challenges=str(key_challenges),
            )

            # 관련 뉴스
            related_news = [
                RelatedNews(**item) for item in data.get("related_news", [])
            ]

            return AnalysisOutput(
                company_info=company_info,
                financial_status=financial_status,
                trends=trends,
                job_analysis=job_analysis,
                senior_fit=senior_fit,
                coach_tip=coach_tip,
                related_news=related_news,
            )
        except KeyError as e:
            raise ValueError(f"필수 키 누락: {e} / keys={list(data.keys())}")
