# client.py
import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv


# 프로젝트 루트(.env 있는 곳) 기준으로 로드
# 현재 파일: financial-agent/career_analyzer/client.py
# 부모 폴더: financial-agent  -> 여기에 .env 있다고 가정
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)


class GeminiClient:
    def __init__(self, api_key: str | None = None, model: str = "gemini-2.0-flash"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError("환경변수 GOOGLE_API_KEY가 설정되어 있지 않습니다.")

        self.model = model
        self.base_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

    def request(self, prompt: str) -> str:
        """프롬프트를 Gemini에 보내고, 응답 텍스트 전체를 문자열로 반환."""
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        resp = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        # candidates[0].content.parts[*].text 이어붙이기
        try:
            candidates = data["candidates"]
            parts = candidates[0]["content"]["parts"]
            texts = [p.get("text", "") for p in parts]
            return "".join(texts).strip()
        except Exception as e:
            raise RuntimeError(f"Gemini 응답 파싱 중 오류: {e}\n원본 응답: {data}")
