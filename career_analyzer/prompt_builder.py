# prompt_builder.py
from models import AnalysisInput


class PromptBuilder:
    @staticmethod
    def build_prompt(input_data: AnalysisInput) -> str:
        skills_str = ", ".join(
            s.strip() for s in input_data.user_profile.skills if s.strip()
        )
        exps_str = "; ".join(
            e.strip() for e in input_data.user_profile.experiences if e.strip()
        )

        prompt = f"""
당신은 기업 및 직무 분석 전문가입니다.
아래 정보를 기반으로, 지원자가 자기소개서/면접에 바로 활용할 수 있을 정도로
**구체적이고 실무적인 기업 및 직무 분석**을 작성하세요.

[기업명]: {input_data.company_name}
[직무]: {input_data.job_role}
[보유 기술]: {skills_str}
[주요 경력]: {exps_str}

---

반드시 아래 JSON 형식으로만 응답하세요. JSON 이외의 내용, 설명, 마크다운, ```json 코드는 절대 출력하지 마세요.

{{
  "company_info": {{
    "title": "회사 정보 및 산업 분석",
    "content": "이 기업의 핵심 사업(사업부/제품/서비스), 산업 내 위치, 경쟁사 대비 특징, 최근 3~5년간의 큰 흐름(예: 메모리 사이클, 증권업 디지털 전환 등)을 4~6문장으로 설명하세요."
  }},
  "financial_status": {{
    "title": "재무 안정성 및 성장성",
    "content": "매출/영업이익/ROE/부채비율 등 재무 구조를 개괄적으로 설명하고, 안정성과 성장성을 어떻게 평가할 수 있는지, 그리고 투자/채용 측면에서 어떤 의미가 있는지 4~6문장으로 작성하세요. 구체적인 수치는 알고 있는 범위에서만 언급하고, 모르면 추측하지 말고 정성적으로만 평가하세요."
  }},
  "trends": {{
    "title": "최신 동향 및 근무 환경",
    "content": "디지털 전환, AI 도입, 리스크 관리 강화, 글로벌 진출, 조직문화(수평적 문화, 워라밸, 평가 체계 등)와 관련된 최근 동향을 정리하고, 해당 직무가 영향을 받을 만한 변화(예: 개발 조직 구조, 애자일 도입, 클라우드 전환 등)를 4~6문장으로 구체적으로 작성하세요."
  }},
  "job_analysis": {{
    "title": "직무 심층 분석",
    "overview": "해당 직무의 전체적인 역할과 포지션을 3~4문장으로 요약하세요.",
    "main_tasks": [
      "주요 업무 1",
      "주요 업무 2",
      "주요 업무 3"
    ],
    "required_skills": [
      "이 직무에서 특히 중요한 기술/역량 1",
      "이 직무에서 특히 중요한 기술/역량 2"
    ],
    "career_path": [
      "초기 커리어 단계 (예: Junior 개발자 → Senior 개발자)",
      "중기 이후 커리어 단계 (예: Tech Lead, Architect, PM, Director 등)"
    ]
  }},
  "senior_fit": {{
    "title": "5060 시니어 적합성",
    "strengths": "위에 제시된 [보유 기술]과 [주요 경력]을 근거로, 이 지원자가 해당 직무에 적합한 이유와 강점을 4~6문장으로 작성하세요. 특히 실무 경험, 프로젝트, 연구 경험이 어떻게 회사의 비즈니스(수익, 리스크 관리, 서비스 품질)에 연결되는지를 명시적으로 적어주세요.",
    "key_challenges": "지원자가 앞으로 보완해야 할 부분이나, 이 직무/업계 특성상 계속해서 공부해야 할 영역(예: 최신 AI/클라우드 트렌드, 금융 규제 이해 등)을 3~5문장으로 정리하세요. 단, 비난이 아니라 코칭 관점에서 작성하세요."
  }},
  "coach_tip": {{
    "title": "Coach's Tip",
    "content": "면접/자소서에서 반드시 강조해야 할 포인트를 3~5개 bullet point 형식으로 제시하세요. 각 포인트는 '•' 로 시작하고, 1줄에 1아이템만 작성하며, 가능한 한 '상황-행동-결과'가 드러나도록 구체적으로 작성하세요."
  }},
  "related_news": [
    {{
      "title": "기사 제목 1",
      "url": "https://www.mk.co.kr/news/...", 
      "source": "매일경제",
      "reason": "이 기사가 지원 기업/직무와 어떻게 연결되는지 한 문장으로 설명"
    }},
    {{
      "title": "기사 제목 2",
      "url": "https://www.mk.co.kr/news/...",
      "source": "매일경제",
      "reason": "이 기사가 지원자의 강점(기술/경력)과 어떻게 연결되는지 한 문장으로 설명"
    }}
  ]
}}

요구사항:
- 반드시 위 JSON 구조와 키 이름을 그대로 사용하세요.
- 존재 여부를 확신할 수 없는 구체적인 수치나 연도는 '정성적 표현'으로 대체하세요. (예: '최근 몇 년간', '업계 상위권 수준의 수익성')
- job_analysis.main_tasks / required_skills / career_path 는 반드시 문자열 배열(list)로 작성하세요.
- senior_fit.strengths / key_challenges 는 여러 문장으로 이루어진 하나의 문자열로 작성하세요.
- [related_news]는 1~3개의 매일경제 기사로만 구성하세요.
  - source는 반드시 "매일경제"로 설정하세요.
  - url은 매일경제 도메인 형식을 사용하되, 실제 기사 존재 여부를 확신할 수 없으면 '예시 URL'이라고 생각하고 자연스럽게 작성하세요.
  - reason에는 왜 이 기사가 해당 기업/직무/지원자에게 의미 있는지 구체적으로 적으세요.
- JSON 이외의 텍스트는 절대 출력하지 마세요.
"""
        return prompt.strip()
