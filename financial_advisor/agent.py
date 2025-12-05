from google.genai import types
from google.adk.tools import ToolContext
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.company_profile_analyst import company_profile_analyst
from .sub_agents.job_market_analyst import job_market_analyst
from .sub_agents.news_analyst import news_analyst
from .sub_agents.financial_analyst import financial_analyst
from .prompt import PROMPT

async def save_company_analysis_report(tool_context: ToolContext, summary: str, company_name: str, job_role: str):
    """
    Saves the final analysis report as a Markdown file for the user.
    """
    state = tool_context.state
    company_profile_result = state.get("company_profile_analyst_result", "데이터가 없습니다.")
    financial_stability_result = state.get("financial_analyst_result", "데이터가 없습니다.")
    news_result = state.get("news_analyst_result", "데이터가 없습니다.")
    job_market_result = state.get("job_market_analyst_result", "데이터가 없습니다.")
    
    report = f"""
# [기업 및 직무 분석] {company_name} - {job_role}

## 종합 의견
{summary}

---
### 회사 정보 및 산업 분석
{company_profile_result}

### 재무 안정성 및 성장성
{financial_stability_result}

### 최신 동향 및 근무 환경
{news_result}

### 직무 심층 분석
{job_market_result}
    """
    state["report"] = report

    filename = f"{company_name}_{job_role}_analysis_report.md"

    artifact = types.Part(
        inline_data=types.Blob(
            mime_type="text/markdown",
            data=report.encode("utf-8"),
        )
    )

    await tool_context.save_artifact(filename, artifact)

    return {
        "success": True,
        "message": f"Report saved as {filename}"
    }

career_coach = Agent(
    name="CareerCoach",
    instruction=PROMPT,
    model="gemini-2.5-flash",
    tools=[
        AgentTool(agent=company_profile_analyst),
        AgentTool(agent=financial_analyst),
        AgentTool(agent=news_analyst),
        AgentTool(agent=job_market_analyst),
        save_company_analysis_report,
    ],
)

root_agent = career_coach