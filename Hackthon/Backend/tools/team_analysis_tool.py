import json
import logging
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

# ===== Logging Setup =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("team_risk_tool")

# ===== Team Evaluation Tool - FIXED SIGNATURE =====
async def evaluate_team_tool(company_name: str, team_members_json: str) -> str:
    """
    Simplified tool that ADK can handle easily
    team_members_json should be a JSON string of the team members list
    """
    try:
        logger.info(f"Evaluating team for {company_name}")
        
        # Parse the JSON string
        team_members = json.loads(team_members_json)
        
        if not isinstance(team_members, list):
            return json.dumps({"error": "team_members must be a list"})
        
        # Perform the analysis
        analysis = await analyze_team_composition(company_name, team_members)
        return json.dumps(analysis)
        
    except Exception as e:
        logger.error(f"Team evaluation error: {e}")
        return json.dumps({"error": f"Team evaluation failed: {str(e)}"})

async def analyze_team_composition(company_name: str, team_members: List[Dict]) -> Dict:
    """
    Analyze team composition
    """
    logger.info(f"Analyzing {len(team_members)} team members for {company_name}")
    
    analysis = {
        "team_size_adequacy": analyze_team_size(team_members),
        "role_completeness": analyze_role_coverage(team_members),
        "skill_gaps": identify_skill_gaps(team_members),
        "execution_risks": identify_execution_risks(team_members)
    }
    
    # Calculate overall scores
    analysis["scores"] = calculate_team_scores(analysis)
    analysis["recommendations"] = generate_recommendations(analysis)
    
    return {
        "team_assessment": {
            "company_name": company_name,
            "team_size": len(team_members),
            "overall_score": analysis["scores"]["overall_score"],
            "risk_level": analysis["execution_risks"]["risk_level"],
            "strengths": extract_strengths(analysis),
            "concerns": extract_concerns(analysis),
            "recommendations": analysis["recommendations"],
            "detailed_analysis": analysis
        }
    }

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
        "technical_lead": any(keyword in ' '.join(roles) for keyword in ['cto', 'technical', 'engineer', 'developer']),
        "business_lead": any(keyword in ' '.join(roles) for keyword in ['ceo', 'business', 'commercial', 'sales', 'marketing']),
        "product_lead": any(keyword in ' '.join(roles) for keyword in ['product', 'design', 'ux', 'ui']),
        "operations_lead": any(keyword in ' '.join(roles) for keyword in ['operations', 'coo', 'delivery'])
    }
    
    coverage_percentage = (sum(key_roles.values()) / len(key_roles)) * 100
    
    missing_roles = [role for role, covered in key_roles.items() if not covered]
    
    return {
        "key_roles_present": key_roles,
        "coverage_percentage": coverage_percentage,
        "missing_roles": missing_roles,
        "rating": "STRONG" if coverage_percentage >= 75 else "MODERATE" if coverage_percentage >= 50 else "WEAK"
    }

def identify_skill_gaps(team_members: List[Dict]) -> List[str]:
    """Identify potential skill gaps in the team"""
    gaps = []
    roles = [member.get('role', '').lower() for member in team_members]
    all_roles_text = ' '.join(roles)
    
    # Check for common startup skill gaps
    if not any(keyword in all_roles_text for keyword in ['technical', 'engineer', 'cto', 'developer']):
        gaps.append("TECHNICAL_LEADERSHIP: No clear technical expertise")
    
    if not any(keyword in all_roles_text for keyword in ['business', 'ceo', 'sales', 'marketing', 'commercial']):
        gaps.append("BUSINESS_LEADERSHIP: No clear business/commercial expertise")
    
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
    roles_text = ' '.join([member.get('role', '').lower() for member in team_members])
    technical_present = any(keyword in roles_text for keyword in ['technical', 'engineer', 'cto', 'developer'])
    business_present = any(keyword in roles_text for keyword in ['business', 'ceo', 'sales', 'marketing'])
    
    if not technical_present and not business_present:
        risks.append("HIGH_RISK: Missing both technical and business leadership")
        risk_level = "HIGH"
    elif not technical_present:
        risks.append("MEDIUM_RISK: Missing technical leadership")
        risk_level = max(risk_level, "MEDIUM")
    elif not business_present:
        risks.append("MEDIUM_RISK: Missing business leadership") 
        risk_level = max(risk_level, "MEDIUM")
    
    return {
        "risk_level": risk_level,
        "identified_risks": risks,
        "risk_score": {"HIGH": 75, "MEDIUM": 50, "LOW": 25}.get(risk_level, 25)
    }

def calculate_team_scores(analysis: Dict) -> Dict:
    """Calculate overall team scores"""
    size_score = {"EXCELLENT": 90, "GOOD": 70, "RISKY": 30}[analysis["team_size_adequacy"]["rating"]]
    role_score = analysis["role_completeness"]["coverage_percentage"]
    risk_score = 100 - analysis["execution_risks"]["risk_score"]
    
    # Simple weighted average
    overall_score = (size_score * 0.3 + role_score * 0.4 + risk_score * 0.3)
    
    return {
        "team_size_score": size_score,
        "role_coverage_score": role_score,
        "risk_score": risk_score,
        "overall_score": round(overall_score, 1)
    }

def extract_strengths(analysis: Dict) -> List[str]:
    """Extract strengths from analysis"""
    strengths = []
    
    if analysis["team_size_adequacy"]["rating"] in ["EXCELLENT", "GOOD"]:
        strengths.append(f"Strong team size: {analysis['team_size_adequacy']['rationale']}")
    
    if analysis["role_completeness"]["rating"] == "STRONG":
        strengths.append("Comprehensive role coverage across key functions")
    
    if analysis["execution_risks"]["risk_level"] == "LOW":
        strengths.append("Low execution risk based on team composition")
    
    return strengths

def extract_concerns(analysis: Dict) -> List[str]:
    """Extract concerns from analysis"""
    concerns = []
    
    concerns.extend(analysis["skill_gaps"])
    concerns.extend(analysis["execution_risks"]["identified_risks"])
    
    return concerns

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
        recommendations.append(f"Consider adding {role_name} expertise through hiring or advisory board")
    
    return recommendations