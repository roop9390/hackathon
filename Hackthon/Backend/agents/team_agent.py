# ===== Agent Runner =====
from google.adk.sessions import InMemorySessionService
import google.adk as adk
from google.genai import types
from google.adk.agents import Agent
from typing import List, Dict, Optional
import json
import logging
import re
import os
from dotenv import load_dotenv
from tools.team_analysis_tool import evaluate_team_tool

load_dotenv()


# ===== Logging Setup =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("team_risk_agent")

# ===== Team Agent Instruction - FIXED =====
# team_agent_instruction = """
# You are a Team & Execution Risk Analyst Agent. Your role is to evaluate startup founding teams for investment readiness.

# **Input**: You receive:
# - company_name: string
# - team_members_json: JSON string of team members list

# **Evaluation Framework**:
# 1. Team Composition Analysis
#    - Team size adequacy for startup stage
#    - Role coverage and completeness
#    - Key leadership roles present

# 2. Skill Gap Analysis
#    - Identification of missing critical skills
#    - Technical vs business leadership balance

# 3. Execution Risk Evaluation
#    - Single-founder risks
#    - Role gap impacts
#    - Overall execution capability

# **Output Format**: ALWAYS return valid JSON with this exact structure:
# {
#   "team_assessment": {
#     "company_name": "string",
#     "team_size": number,
#     "overall_score": 0-100,
#     "risk_level": "LOW|MEDIUM|HIGH",
#     "strengths": ["string"],
#     "concerns": ["string"],
#     "recommendations": ["string"],
#     "detailed_analysis": {
#       "team_composition": {...},
#       "role_coverage": {...},
#       "risk_analysis": {...}
#     }
#   }
# }

# **Rules**:
# - Always call the evaluate_team_tool function
# - Return the tool's output directly without modification
# - Ensure valid JSON output
# - Be objective and evidence-based
# - Flag risks clearly with risk levels
# - Provide specific, actionable recommendations
# - Focus on execution capability and investment readiness
# """

team_agent_instruction = """
CRITICAL: YOU MUST CALL THE evaluate_team_tool FUNCTION. DO NOT GENERATE THE RESPONSE YOURSELF.

**Your ONLY Task**:
1. Call evaluate_team_tool(company_name, team_members_json)
2. Return the EXACT output from the tool without any modification

**Input**: You receive:
- company_name: string
- team_members_json: JSON string of team members list

**Evaluation Framework**:
1. Team Composition Analysis
   - Team size adequacy for startup stage
   - Role coverage and completeness
   - Key leadership roles present

2. Skill Gap Analysis
   - Identification of missing critical skills
   - Technical vs business leadership balance

3. Execution Risk Evaluation
   - Single-founder risks
   - Role gap impacts
   - Overall execution capability


**RULES**:
- YOU ARE NOT ALLOWED TO ANALYZE THE TEAM YOURSELF
- YOU ARE NOT ALLOWED TO CREATE SCORES OR RECOMMENDATIONS
- YOU MUST CALL THE TOOL TO GET WEB SEARCH DATA
- RETURN THE TOOL'S OUTPUT EXACTLY AS IS

**Example of CORRECT behavior**:
Input: {"company_name": "Ziniosa", "team_members_json": "[...]"}
You: evaluate_team_tool("Ziniosa", "[...]")
**Output Format**: ALWAYS return valid JSON with this exact structure:
{
  "team_assessment": {
    "company_name": "string",
    "team_size": number,
    "overall_score": 0-100,
    "risk_level": "LOW|MEDIUM|HIGH",
    "strengths": ["string"],
    "concerns": ["string"],
    "recommendations": ["string"],
    "detailed_analysis": {
      "team_composition": {...},
      "role_coverage": {...},
      "risk_analysis": {...}
    }
  }
}

**Failure to call the tool will result in missing critical web search data and inaccurate analysis.**
"""

# ===== Define the Team Agent =====
team_risk_agent = Agent(
    name="team_risk_agent",
    model="gemini-2.0-flash-exp",
    instruction=team_agent_instruction,
    tools=[evaluate_team_tool],
)

session_service = InMemorySessionService()

async def run_team_agent(agent_input: Dict) -> Dict:
    """
    Run the team evaluation agent
    """
    await session_service.create_session(
        app_name="team_evaluation_app",
        user_id="user123",
        session_id="session1"
    )
    
    runner = adk.Runner(agent=team_risk_agent, app_name="team_evaluation_app", session_service=session_service)
    
    # Prepare input for the agent
    input_text = json.dumps(agent_input)
    content = types.Content(role="user", parts=[types.Part(text=input_text)])
    
    final_output = None
    
    async for event in runner.run_async(
        user_id="user123",
        session_id="session1",
        new_message=content
    ):
        if not event.content or not event.content.parts:
            continue
            
        for part in event.content.parts:
            if part.text:
                raw_text = part.text.strip()
                # Clean JSON output
                cleaned_text = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.MULTILINE)
                logger.info(f"Team Agent Output: {cleaned_text}")
                final_output = cleaned_text
                
            elif part.function_call:
                logger.info(f"Team Agent Tool Call: {part.function_call.name}({part.function_call.args})")
    
    if not final_output:
        return {"error": "Team agent returned no output"}
    
    try:
        return json.loads(final_output)
    except json.JSONDecodeError:
        return {"error": "Failed to parse agent output as JSON", "raw_output": final_output}