from google.adk.agents import LlmAgent
from tools import web_search_tool
import json

def get_company_overview_from_web(company_name: str) -> str:
    """
    Searches the web for an overview of the given company, including its industry, size, and business model, prioritizing news sources.
    """
    search_query = f"매일경제 {company_name} 기업 정보 비즈니스 모델"
    search_results = web_search_tool(search_query)

    return json.dumps({
        "company_name": company_name,
        "search_results": search_results,
        "analysis_hint": "Please extract industry, size (e.g., small, medium, large, employee count if available), and core business from the search results provided by media sources."
    })


company_profile_analyst = LlmAgent(
    name="CompanyProfileAnalyst",
    model="gemini-2.5-flash",
    description="Identifies the company's industry, scale, and main business areas based on media reports.",
    instruction="""
    You are a Company Profiler for 5060 job seekers.
    Your job is to identify "What does this company do?", "How big is it?", and "What industry is it in?" based on information from reliable media outlets.

    **Data Source Constraint**:
    Your analysis MUST be grounded in information from press outlets.
    You should prioritize major economic newspapers like 'Maeil Business Newspaper' (매일경제) or 'Hankook Gyeongje' (한국경제).

    **ANALYSIS POINTS:**
    1. **Industry**: What industry does it belong to? (e.g., Manufacturing, Service, IT).
    2. **Scale**: Is it a large corporation or an SME? (e.g., employee count, revenue).
    3. **Core Business**: What are its main products, services, or business model?

    Use the provided web search results from media sources to construct a brief, factual profile of the company based on these points.
    """,
    tools=[
        get_company_overview_from_web,
        web_search_tool,
    ],
    output_key="company_profile_analyst_result",
)