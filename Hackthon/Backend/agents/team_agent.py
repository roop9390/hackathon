import os
import re
import json
import logging
import asyncio
from typing import Dict, List, Any
from google.adk.agents import Agent, SequentialAgent
import google.adk as adk
from google.adk.sessions import InMemorySessionService
from google.genai import types
from typing import List, Dict, Optional

# ===== Logging Setup =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("team_risk_agent")

# ===== Team Evaluation Tool =====
# async def evaluate_team_tool(
#                            company_name: str = None, team_members: List[Dict] = None) -> Dict:
#     """
#     Tool to evaluate startup team composition and execution risk
#     Can accept either file paths or direct team data
#     """
#     try:
#         logger.info(f"Evaluating team for {company_name or 'unknown company'}")
        
#         # If we have file paths, extract team data from documents first
#         team_data = {}
        
#         if team_members and company_name:
#             team_data = {
#                 "company_name": company_name,
#                 "team_members": team_members
#             }
#         else:
#             return {"error": "Either file_paths+bucket_name or company_name+team_members required"}
        
#         # Evaluate the team
#         evaluation = await analyze_team_composition(team_data)
#         return evaluation
        
#     except Exception as e:
#         logger.error(f"Team evaluation error: {e}")
#         return {"error": f"Team evaluation failed: {str(e)}"}

async def evaluate_team_tool(
    company_name: Optional[str] = None,
    team_members: Optional[List[Any]] = None
) -> Dict:
    """
    Tool to evaluate startup team composition and execution risk
    Can accept either file paths or direct team data
    """
    try:
        logger.info(f"Evaluating team for {company_name or 'unknown company'}")
        
        team_data = {}
        
        if team_members and company_name:
            team_data = {
                "company_name": company_name,
                "team_members": team_members
            }
        else:
            return {"error": "Either file_paths+bucket_name or company_name+team_members required"}
        
        evaluation = await analyze_team_composition(team_data)
        return evaluation
        
    except Exception as e:
        logger.error(f"Team evaluation error: {e}")
        return {"error": f"Team evaluation failed: {str(e)}"}

async def extract_team_from_documents(bucket_name: str, file_paths: List[str]) -> Dict:
    """
    Extract team information from uploaded documents using Gemini
    """
    # This would integrate with your existing document processing
    # For now, we'll simulate extraction
    logger.info(f"Extracting team data from {len(file_paths)} files in {bucket_name}")
    
    # Simulate extraction - in real implementation, you'd use Gemini to parse docs
    return {
        "company_name": "ExtractedCompany",
        "team_members": [
            {"name": "Founder One", "role": "CEO"},
            {"name": "Founder Two", "role": "CTO"}
        ]
    }

async def analyze_team_composition(team_data: Dict) -> Dict:
    """
    Analyze team composition using Google's AI services
    """
    company_name = team_data.get("company_name", "Unknown")
    team_members = team_data.get("team_members", [])
    
    logger.info(f"Analyzing {len(team_members)} team members for {company_name}")
    
    # Use Gemini to analyze team composition
    analysis = {
        "team_size_adequacy": analyze_team_size(team_members),
        "role_completeness": analyze_role_coverage(team_members),
        "founder_experience": await assess_founder_experience(company_name, team_members),
        "skill_gaps": identify_skill_gaps(team_members),
        "execution_risks": identify_execution_risks(team_members)
    }
    
    # Calculate overall scores
    analysis["scores"] = calculate_team_scores(analysis)
    analysis["recommendations"] = generate_recommendations(analysis)
    
    return analysis

def analyze_team_size(team_members: List[Dict]) -> Dict:
    """Analyze if team size is adequate for startup stage"""
    size = len(team_members)
    
    if size >= 3:
        rating = "EXCELLENT"
        rationale = "Ideal founding team size with role specialization"
    elif size == 2:
        rating = "GOOD" 
        rationale = "Standard founding team, should cover key roles"
    else:
        rating = "RISKY"
        rationale = "Single founder carries higher execution risk"
    
    return {
        "team_size": size,
        "rating": rating,
        "rationale": rationale
    }

def analyze_role_coverage(team_members: List[Dict]) -> Dict:
    """Analyze coverage of key startup roles"""
    roles = [member.get('role', '').lower() for member in team_members]
    
    key_roles = {
        "technical_lead": any(role in ['cto', 'technical founder', 'tech lead'] for role in roles),
        "business_lead": any(role in ['ceo', 'business founder', 'commercial lead'] for role in roles),
        "product_lead": any(role in ['cpO', 'product founder', 'product lead'] for role in roles),
        "operations_lead": any(role in ['coo', 'operations lead'] for role in roles)
    }
    
    coverage_percentage = (sum(key_roles.values()) / len(key_roles)) * 100
    
    missing_roles = [role for role, covered in key_roles.items() if not covered]
    
    return {
        "key_roles_present": key_roles,
        "coverage_percentage": coverage_percentage,
        "missing_roles": missing_roles,
        "rating": "STRONG" if coverage_percentage >= 75 else "MODERATE" if coverage_percentage >= 50 else "WEAK"
    }

async def assess_founder_experience(company_name: str, team_members: List[Dict]) -> Dict:
    """
    Assess founder experience using Google Search and knowledge graph
    In a real implementation, this would use Google's Enterprise Search API
    """
    experience_assessments = []
    
    for member in team_members:
        member_name = member.get('name', '')
        role = member.get('role', '')
        
        # Simulate experience assessment - real implementation would use actual APIs
        experience_score = len(member_name) * 2  # Placeholder - real logic would be more sophisticated
        experience_level = "SENIOR" if experience_score > 10 else "MID" if experience_score > 5 else "JUNIOR"
        
        experience_assessments.append({
            "name": member_name,
            "role": role,
            "experience_score": min(experience_score, 100),
            "experience_level": experience_level,
            "indicators": ["Previous startup experience", "Domain expertise"]  # Placeholder
        })
    
    return {
        "individual_assessments": experience_assessments,
        "team_experience_score": sum(member["experience_score"] for member in experience_assessments) / len(experience_assessments) if experience_assessments else 0
    }

def identify_skill_gaps(team_members: List[Dict]) -> List[str]:
    """Identify potential skill gaps in the team"""
    gaps = []
    roles = [member.get('role', '').lower() for member in team_members]
    
    # Check for common startup skill gaps
    if not any('technical' in role or 'engineer' in role or 'cto' in role for role in roles):
        gaps.append("TECHNICAL_LEADERSHIP: No clear technical founder")
    
    if not any('business' in role or 'ceo' in role or 'sales' in role for role in roles):
        gaps.append("BUSINESS_LEADERSHIP: No clear business/commercial founder")
    
    if not any('product' in role or 'design' in role for role in roles):
        gaps.append("PRODUCT_EXPERIENCE: Limited product management expertise")
    
    if len(team_members) < 2:
        gaps.append("TEAM_SIZE: Single founder may lack bandwidth for all functions")
    
    return gaps

def identify_execution_risks(team_members: List[Dict]) -> Dict:
    """Identify execution risks based on team composition"""
    risks = []
    risk_level = "LOW"
    
    # Single founder risk
    if len(team_members) == 1:
        risks.append("HIGH_RISK: Single founder - high execution burden")
        risk_level = "HIGH"
    
    # Role gap risks
    roles = [member.get('role', '').lower() for member in team_members]
    technical_present = any('technical' in role or 'engineer' in role or 'cto' in role for role in roles)
    business_present = any('business' in role or 'ceo' in role or 'sales' in role for role in roles)
    
    if not technical_present and not business_present:
        risks.append("HIGH_RISK: Missing both technical and business leadership")
        risk_level = "HIGH"
    elif not technical_present:
        risks.append("MEDIUM_RISK: Missing technical leadership")
        risk_level = "MEDIUM" if risk_level != "HIGH" else "HIGH"
    elif not business_present:
        risks.append("MEDIUM_RISK: Missing business leadership") 
        risk_level = "MEDIUM" if risk_level != "HIGH" else "HIGH"
    
    return {
        "risk_level": risk_level,
        "identified_risks": risks,
        "risk_score": {"HIGH": 75, "MEDIUM": 50, "LOW": 25}.get(risk_level, 25)
    }

def calculate_team_scores(analysis: Dict) -> Dict:
    """Calculate overall team scores"""
    size_score = {"EXCELLENT": 90, "GOOD": 70, "RISKY": 30}[analysis["team_size_adequacy"]["rating"]]
    role_score = analysis["role_completeness"]["coverage_percentage"]
    experience_score = analysis["founder_experience"]["team_experience_score"]
    risk_score = 100 - analysis["execution_risks"]["risk_score"]
    
    overall_score = (size_score * 0.2 + role_score * 0.3 + experience_score * 0.3 + risk_score * 0.2)
    
    return {
        "team_size_score": size_score,
        "role_coverage_score": role_score,
        "experience_score": experience_score,
        "risk_score": risk_score,
        "overall_score": overall_score
    }

def generate_recommendations(analysis: Dict) -> List[str]:
    """Generate actionable recommendations based on analysis"""
    recommendations = []
    
    # Team size recommendations
    if analysis["team_size_adequacy"]["team_size"] == 1:
        recommendations.append("Consider bringing on a co-founder to share execution burden")
    
    # Role gap recommendations
    missing_roles = analysis["role_completeness"]["missing_roles"]
    for role in missing_roles:
        role_name = role.replace('_', ' ').title()
        recommendations.append(f"Address {role_name} gap through hiring or advisory board")
    
    # Risk mitigation recommendations
    if analysis["execution_risks"]["risk_level"] in ["HIGH", "MEDIUM"]:
        recommendations.append("Develop clear role definitions and accountability matrix")
        recommendations.append("Consider interim executives or advisors for missing expertise")
    
    return recommendations

# ===== Team Agent Instruction =====
team_agent_instruction = """
You are a Team & Execution Risk Analyst Agent. Your role is to evaluate startup founding teams for investment readiness.

**Input**: You receive either:
1. bucket_name + file_paths: Documents to extract team data from
2. company_name + team_members: Direct team data

**Evaluation Framework**:
1. Team Composition Analysis
   - Team size adequacy for startup stage
   - Role coverage and completeness
   - Key leadership roles present

2. Founder Experience Assessment  
   - Individual founder backgrounds
   - Relevant domain expertise
   - Previous startup experience

3. Skill Gap Analysis
   - Identification of missing critical skills
   - Technical vs business leadership balance
   - Functional coverage

4. Execution Risk Evaluation
   - Single-founder risks
   - Role gap impacts
   - Overall execution capability

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
      "experience_assessment": {...},
      "risk_analysis": {...}
    }
  }
}

**Rules**:
- Be objective and evidence-based
- Flag risks clearly with risk levels
- Provide specific, actionable recommendations
- Focus on execution capability and investment readiness
"""

# ===== Define the Team Agent =====
team_risk_agent = Agent(
    name="team_risk_agent",
    model="gemini-2.0-flash-exp",
    instruction=team_agent_instruction,
    tools=[evaluate_team_tool],
)

# ===== Agent Runner =====
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

# ===== Example Usage =====
async def test_team_agent():
    """Test the team agent with sample data"""
    sample_input = {
        "company_name": "TechInnovate Inc",
        "team_members": [
            {"name": "Sarah Chen", "role": "CEO"},
            {"name": "Mike Rodriguez", "role": "CTO"},
            {"name": "David Kim", "role": "Head of Product"}
        ]
    }
    
    result = await run_team_agent(sample_input)
    print("Team Agent Test Result:")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    asyncio.run(test_team_agent())