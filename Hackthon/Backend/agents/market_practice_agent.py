# import asyncio
# import aiohttp
# import json
# import re
# from typing import Dict, List, Any
# from config import Config

# class MarketAnalystAgent:
#     """
#     Market & Competitive Analyst Agent
#     Takes input: {"market": {"market_size_claim": "...", "target_market": "..."}}
#     Generates comprehensive market analysis report using free APIs
#     """
    
#     def __init__(self):
#         self.config = Config()
#         self.session = None
        
#     async def __aenter__(self):
#         self.session = aiohttp.ClientSession()
#         return self
        
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         await self.session.close()
    
#     async def analyze_market(self, startup_data: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Main method - takes startup data and returns comprehensive market analysis
#         Input format: {"market": {"market_size_claim": "...", "target_market": "..."}}
#         """
#         print("🚀 Starting Market Analysis...")
        
#         market_data = startup_data.get("market", {})
#         claimed_size = market_data.get("market_size_claim", "")
#         target_market = market_data.get("target_market", "")
        
#         # Run all analysis tools in parallel
#         tasks = {
#             "market_validation": self._validate_market_size(claimed_size, target_market),
#             "competitive_landscape": self._analyze_competitive_landscape(target_market),
#             "market_trends": self._analyze_market_trends(target_market),
#             "industry_benchmarks": self._get_industry_benchmarks(target_market),
#             "risk_assessment": self._assess_market_risks(target_market)
#         }
        
#         results = {}
#         for task_name, task in tasks.items():
#             try:
#                 results[task_name] = await task
#                 print(f"✅ {task_name.replace('_', ' ').title()} Completed")
#             except Exception as e:
#                 print(f"❌ {task_name} Failed: {e}")
#                 results[task_name] = {}
        
#         # Generate final report
#         final_report = await self._generate_comprehensive_report(
#             claimed_size, target_market, results
#         )
        
#         return final_report
    
#     # Tool 1: Market Size Validation
#     async def _validate_market_size(self, claimed_size: str, target_market: str) -> Dict:
#         """Validate market size claims using multiple data sources"""
#         print(f"🔍 Validating market size: {claimed_size}")
        
#         extracted_size = self._extract_market_size_numbers(claimed_size)
        
#         # Run validation from multiple sources
#         google_results = await self._google_market_validation(target_market, extracted_size)
#         world_bank_data = await self._world_bank_validation(target_market)
        
#         return {
#             "claimed_size": claimed_size,
#             "extracted_values": extracted_size,
#             "google_validation": google_results,
#             "world_bank_data": world_bank_data,
#             "confidence_score": self._calculate_validation_confidence(google_results, world_bank_data)
#         }
    
#     # Tool 2: Competitive Landscape Analysis
#     async def _analyze_competitive_landscape(self, target_market: str) -> Dict:
#         """Analyze competitors and market positioning"""
#         print(f"🏢 Analyzing competitive landscape for: {target_market}")
        
#         competitors = await self._find_competitors(target_market)
#         market_concentration = await self._analyze_market_concentration(competitors)
        
#         return {
#             "direct_competitors": competitors.get("direct", []),
#             "indirect_competitors": competitors.get("indirect", []),
#             "market_concentration": market_concentration,
#             "key_players": competitors.get("key_players", []),
#             "competitive_intensity": self._assess_competitive_intensity(competitors)
#         }
    
#     # Tool 3: Market Trends Analysis
#     async def _analyze_market_trends(self, target_market: str) -> Dict:
#         """Analyze current market trends and growth patterns"""
#         print(f"📈 Analyzing market trends for: {target_market}")
        
#         trends_data = await self._google_trends_analysis(target_market)
#         growth_patterns = await self._analyze_growth_patterns(target_market)
        
#         return {
#             "market_trends": trends_data,
#             "growth_patterns": growth_patterns,
#             "adoption_curve": self._estimate_adoption_curve(target_market),
#             "seasonality": self._analyze_seasonality(target_market)
#         }
    
#     # Tool 4: Industry Benchmarks
#     async def _get_industry_benchmarks(self, target_market: str) -> Dict:
#         """Get industry-specific benchmarks and KPIs"""
#         print(f"📊 Gathering industry benchmarks for: {target_market}")
        
#         benchmarks = await self._fetch_industry_benchmarks(target_market)
#         kpi_analysis = await self._analyze_standard_kpis(target_market)
        
#         return {
#             "revenue_benchmarks": benchmarks.get("revenue", {}),
#             "growth_benchmarks": benchmarks.get("growth", {}),
#             "kpi_standards": kpi_analysis,
#             "profitability_metrics": benchmarks.get("profitability", {})
#         }
    
#     # Tool 5: Risk Assessment
#     async def _assess_market_risks(self, target_market: str) -> Dict:
#         """Assess market risks and opportunities"""
#         print(f"⚠️ Assessing market risks for: {target_market}")
        
#         risks = await self._identify_market_risks(target_market)
#         opportunities = await self._identify_market_opportunities(target_market)
        
#         return {
#             "market_risks": risks,
#             "growth_opportunities": opportunities,
#             "regulatory_factors": await self._analyze_regulatory_factors(target_market),
#             "economic_sensitivity": self._assess_economic_sensitivity(target_market)
#         }
    
#     # Implementation of individual tools
#     def _extract_market_size_numbers(self, text: str) -> Dict:
#         """Extract numerical values from market size claims"""
#         patterns = {
#             'billion': r'[\$]?([\d\.]+)\s*[Bb]illion',
#             'million': r'[\$]?([\d\.]+)\s*[Mm]illion',
#             'trillion': r'[\$]?([\d\.]+)\s*[Tt]rillion',
#             'year': r'by\s*(\d{4})|in\s*(\d{4})'
#         }
        
#         extracted = {}
#         for key, pattern in patterns.items():
#             matches = re.findall(pattern, text)
#             if matches:
#                 # Handle multiple capture groups
#                 clean_matches = []
#                 for match in matches:
#                     if isinstance(match, tuple):
#                         clean_matches.extend([m for m in match if m])
#                     else:
#                         clean_matches.append(match)
#                 extracted[key] = clean_matches[0] if clean_matches else None
        
#         return extracted
    
#     async def _google_market_validation(self, target_market: str, extracted_size: Dict) -> Dict:
#         """Use Google Search to validate market claims"""
#         if not self.config.GOOGLE_SEARCH_KEY or not self.config.GOOGLE_SEARCH_Engine_Id:
#             return {"error": "Google API not configured"}
        
#         try:
#             queries = [
#                 f'"{target_market}" market size 2024',
#                 f'global {target_market} industry statistics',
#                 f'{target_market} TAM SAM SOM analysis',
#                 f'{target_market} market growth report'
#             ]
            
#             all_results = []
#             for query in queries[:2]:  # Limit to save API calls
#                 url = "https://www.googleapis.com/customsearch/v1"
#                 params = {
#                     'key': self.config.GOOGLE_SEARCH_KEY,
#                     'cx': self.config.GOOGLE_SEARCH_Engine_Id,
#                     'q': query,
#                     'num': 3
#                 }
                
#                 async with self.session.get(url, params=params) as response:
#                     if response.status == 200:
#                         data = await response.json()
#                         for item in data.get('items', []):
#                             all_results.append({
#                                 'title': item.get('title'),
#                                 'link': item.get('link'),
#                                 'snippet': item.get('snippet'),
#                                 'relevance_score': self._calculate_relevance(item.get('snippet', ''), target_market)
#                             })
            
#             return {
#                 "sources_checked": len(all_results),
#                 "relevant_sources": [r for r in all_results if r['relevance_score'] > 0.3],
#                 "validation_queries": queries[:2]
#             }
            
#         except Exception as e:
#             return {"error": str(e)}
    
#     async def _world_bank_validation(self, target_market: str) -> Dict:
#         """Use World Bank data for macroeconomic validation"""
#         try:
#             # Map common markets to World Bank indicators
#             indicator_mapping = {
#                 'retail': 'NE.CON.PRVT.CD',
#                 'technology': 'IT.NET.USER.ZS',
#                 'ecommerce': 'IT.NET.USER.ZS',
#                 'automotive': 'IS.VEH.NVEH.P3',
#                 'finance': 'FS.AST.PRVT.GD.ZS',
#                 'healthcare': 'SH.XPD.CHEX.GD.ZS'
#             }
            
#             relevant_indicator = None
#             for keyword, indicator in indicator_mapping.items():
#                 if keyword in target_market.lower():
#                     relevant_indicator = indicator
#                     break
            
#             if not relevant_indicator:
#                 return {"info": "No specific World Bank indicator found for this market"}
            
#             url = f"{self.config.WORLD_BANK_URL}country/IND/indicator/{relevant_indicator}"
#             params = {'format': 'json', 'date': '2020:2024', 'per_page': 5}
            
#             async with self.session.get(url, params=params) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     return self._process_world_bank_response(data, target_market)
#                 else:
#                     return {"error": f"World Bank API returned status {response.status}"}
                    
#         except Exception as e:
#             return {"error": str(e)}
    
#     def _process_world_bank_response(self, data: Dict, target_market: str) -> Dict:
#         """Process World Bank API response"""
#         if not data or len(data) < 2:
#             return {"info": "No data available from World Bank"}
        
#         indicators = data[1]
#         latest_data = []
        
#         for item in indicators[:3]:  # Get latest 3 data points
#             if item.get('value'):
#                 latest_data.append({
#                     'year': item.get('date'),
#                     'value': item.get('value'),
#                     'indicator': item.get('indicator', {}).get('value', '')
#                 })
        
#         return {
#             "indicator": relevant_indicator,
#             "latest_data": latest_data,
#             "trend": "growing" if len(latest_data) > 1 and latest_data[0]['value'] > latest_data[-1]['value'] else "stable/declining"
#         }
    
#     async def _find_competitors(self, target_market: str) -> Dict:
#         """Find direct and indirect competitors"""
#         # Use Google Search to find competitors
#         queries = [
#             f'"{target_market}" competitors',
#             f'"{target_market}" similar companies',
#             f'"{target_market}" market players'
#         ]
        
#         competitors = {"direct": [], "indirect": [], "key_players": []}
        
#         try:
#             for query in queries[:1]:  # Use first query only to save API calls
#                 url = "https://www.googleapis.com/customsearch/v1"
#                 params = {
#                     'key': self.config.GOOGLE_SEARCH_KEY,
#                     'cx': self.config.GOOGLE_SEARCH_Engine_Id,
#                     'q': query,
#                     'num': 5
#                 }
                
#                 async with self.session.get(url, params=params) as response:
#                     if response.status == 200:
#                         data = await response.json()
#                         competitors = self._extract_competitors_from_search(data.get('items', []), target_market)
#                         break
#         except Exception as e:
#             print(f"Competitor search error: {e}")
        
#         return competitors
    
#     def _extract_competitors_from_search(self, search_results: List, target_market: str) -> Dict:
#         """Extract competitor information from search results"""
#         competitors = {"direct": [], "indirect": [], "key_players": []}
        
#         for item in search_results:
#             snippet = item.get('snippet', '').lower()
#             title = item.get('title', '').lower()
            
#             # Simple heuristic for competitor identification
#             if any(term in snippet for term in ['competitor', 'competitive', 'vs', 'alternative']):
#                 competitors["direct"].append({
#                     'name': item.get('title'),
#                     'source': item.get('link'),
#                     'type': 'direct'
#                 })
#             elif any(term in title for term in [target_market.lower(), 'market', 'industry']):
#                 competitors["key_players"].append({
#                     'name': item.get('title'),
#                     'source': item.get('link'),
#                     'type': 'key_player'
#                 })
#             else:
#                 competitors["indirect"].append({
#                     'name': item.get('title'),
#                     'source': item.get('link'),
#                     'type': 'indirect'
#                 })
        
#         return competitors
    
#     async def _google_trends_analysis(self, target_market: str) -> Dict:
#         """Analyze market trends using Google Search data"""
#         try:
#             # Use Google Search to find trend information
#             query = f'"{target_market}" market trends 2024 growth forecast'
            
#             url = "https://www.googleapis.com/customsearch/v1"
#             params = {
#                 'key': self.config.GOOGLE_SEARCH_KEY,
#                 'cx': self.config.GOOGLE_SEARCH_Engine_Id,
#                 'q': query,
#                 'num': 3
#             }
            
#             async with self.session.get(url, params=params) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     return self._process_trends_data(data.get('items', []))
#                 else:
#                     return {"error": "Failed to fetch trends data"}
                    
#         except Exception as e:
#             return {"error": str(e)}
    
#     def _process_trends_data(self, items: List) -> Dict:
#         """Process trends data from search results"""
#         trends = []
        
#         for item in items:
#             snippet = item.get('snippet', '')
#             # Extract growth-related information
#             if any(term in snippet.lower() for term in ['growth', 'increasing', 'rising', 'forecast']):
#                 trends.append({
#                     'source': item.get('title'),
#                     'trend_indication': snippet[:200],
#                     'confidence': 'high' if 'report' in item.get('title', '').lower() else 'medium'
#                 })
        
#         return {
#             "trends_found": len(trends),
#             "trend_direction": "positive" if len(trends) > 2 else "neutral",
#             "sources": trends
#         }
    
#     # Additional helper methods for other tools
#     async def _analyze_growth_patterns(self, target_market: str) -> Dict:
#         """Analyze market growth patterns"""
#         return {
#             "estimated_cagr": "8-12%",  # This would come from actual data analysis
#             "growth_drivers": await self._identify_growth_drivers(target_market),
#             "market_maturity": self._assess_market_maturity(target_market)
#         }
    
#     async def _identify_growth_drivers(self, target_market: str) -> List:
#         """Identify key growth drivers for the market"""
#         # Simplified implementation - would use more sophisticated analysis
#         common_drivers = {
#             'technology': ['Digital adoption', 'Mobile penetration', 'IoT expansion'],
#             'retail': ['E-commerce growth', 'Consumer spending', 'Urbanization'],
#             'finance': ['Digital payments', 'Financial inclusion', 'Regulatory changes']
#         }
        
#         for sector, drivers in common_drivers.items():
#             if sector in target_market.lower():
#                 return drivers
        
#         return ['Market expansion', 'Consumer demand', 'Technological advancement']
    
#     def _assess_market_maturity(self, target_market: str) -> str:
#         """Assess market maturity level"""
#         emerging_terms = ['tech', 'digital', 'ai', 'blockchain', 'edtech', 'fintech']
#         mature_terms = ['retail', 'manufacturing', 'real estate', 'agriculture']
        
#         if any(term in target_market.lower() for term in emerging_terms):
#             return "Emerging"
#         elif any(term in target_market.lower() for term in mature_terms):
#             return "Mature"
#         else:
#             return "Growth"
    
#     async def _fetch_industry_benchmarks(self, target_market: str) -> Dict:
#         """Fetch industry-specific benchmarks"""
#         # This would integrate with more specific APIs
#         return {
#             "revenue": {
#                 "early_stage": "$1-5M ARR",
#                 "growth_stage": "$5-20M ARR",
#                 "mature": "$20M+ ARR"
#             },
#             "growth": {
#                 "early_stage": "100-200% YoY",
#                 "growth_stage": "50-100% YoY",
#                 "mature": "20-50% YoY"
#             },
#             "profitability": {
#                 "gross_margin": "60-80%",
#                 "net_margin": "10-20%",
#                 "cac_ratio": "1:3"
#             }
#         }
    
#     async def _analyze_standard_kpis(self, target_market: str) -> Dict:
#         """Analyze standard KPIs for the industry"""
#         kpi_templates = {
#             'ecommerce': ['CAC', 'LTV', 'Conversion Rate', 'AOV', 'Churn Rate'],
#             'saas': ['MRR', 'ARR', 'Churn Rate', 'LTV:CAC', 'Net Retention'],
#             'marketplace': ['GMV', 'Take Rate', 'Buyer/Seller Ratio', 'Network Effects']
#         }
        
#         for sector, kpis in kpi_templates.items():
#             if sector in target_market.lower():
#                 return kpis
        
#         return ['Revenue Growth', 'Customer Acquisition', 'Profit Margins', 'Market Share']
    
#     async def _identify_market_risks(self, target_market: str) -> List:
#         """Identify potential market risks"""
#         common_risks = {
#             'technology': ['Rapid obsolescence', 'Regulatory changes', 'Cybersecurity threats'],
#             'retail': ['Economic downturns', 'Supply chain disruptions', 'Changing consumer preferences'],
#             'finance': ['Regulatory compliance', 'Market volatility', 'Credit risks']
#         }
        
#         for sector, risks in common_risks.items():
#             if sector in target_market.lower():
#                 return risks
        
#         return ['Market competition', 'Economic factors', 'Regulatory environment']
    
#     async def _identify_market_opportunities(self, target_market: str) -> List:
#         """Identify market opportunities"""
#         return [
#             "Digital transformation initiatives",
#             "Growing consumer demand",
#             "Emerging market segments",
#             "Technology enablement"
#         ]
    
#     async def _analyze_regulatory_factors(self, target_market: str) -> Dict:
#         """Analyze regulatory factors affecting the market"""
#         return {
#             "regulatory_environment": "Moderate",  # Would come from actual analysis
#             "compliance_requirements": ["Data privacy", "Consumer protection"],
#             "licensing_needs": ["Business registration", "Industry-specific licenses"]
#         }
    
#     def _assess_economic_sensitivity(self, target_market: str) -> str:
#         """Assess how sensitive the market is to economic conditions"""
#         sensitive_sectors = ['luxury', 'real estate', 'automotive', 'travel']
#         resilient_sectors = ['healthcare', 'education', 'essential retail', 'utilities']
        
#         if any(sector in target_market.lower() for sector in sensitive_sectors):
#             return "High sensitivity to economic cycles"
#         elif any(sector in target_market.lower() for sector in resilient_sectors):
#             return "Resilient to economic cycles"
#         else:
#             return "Moderate sensitivity to economic cycles"
    
#     def _calculate_relevance(self, snippet: str, target_market: str) -> float:
#         """Calculate relevance score between snippet and target market"""
#         snippet_lower = snippet.lower()
#         market_terms = target_market.lower().split()
        
#         relevance = 0.0
#         for term in market_terms:
#             if term in snippet_lower:
#                 relevance += 0.2
        
#         # Bonus for key terms
#         key_terms = ['market', 'size', 'growth', 'industry', 'report']
#         for term in key_terms:
#             if term in snippet_lower:
#                 relevance += 0.1
        
#         return min(relevance, 1.0)
    
#     def _calculate_validation_confidence(self, google_results: Dict, world_bank_data: Dict) -> int:
#         """Calculate overall validation confidence score (0-100)"""
#         confidence = 0
        
#         # Google results contribution
#         if 'relevant_sources' in google_results:
#             confidence += min(len(google_results['relevant_sources']) * 20, 60)
        
#         # World Bank data contribution
#         if 'latest_data' in world_bank_data and world_bank_data['latest_data']:
#             confidence += 20
        
#         # Error handling
#         if 'error' in google_results or 'error' in world_bank_data:
#             confidence = max(confidence - 20, 0)
        
#         return min(confidence, 100)
    
#     def _assess_competitive_intensity(self, competitors: Dict) -> str:
#         """Assess competitive intensity based on competitor analysis"""
#         total_competitors = len(competitors.get('direct', [])) + len(competitors.get('indirect', []))
        
#         if total_competitors > 10:
#             return "High competition"
#         elif total_competitors > 5:
#             return "Moderate competition"
#         else:
#             return "Low competition"
    
#     def _estimate_adoption_curve(self, target_market: str) -> str:
#         """Estimate technology adoption curve"""
#         tech_heavy = ['ai', 'blockchain', 'iot', 'ar/vr', 'metaverse']
#         if any(tech in target_market.lower() for tech in tech_heavy):
#             return "Early Adopters"
#         else:
#             return "Early Majority"
    
#     def _analyze_seasonality(self, target_market: str) -> Dict:
#         """Analyze market seasonality patterns"""
#         seasonal_patterns = {
#             'retail': "High seasonality (Q4 peak)",
#             'travel': "Seasonal variations",
#             'education': "Academic year cycles",
#             'default': "Moderate seasonality"
#         }
        
#         for pattern, description in seasonal_patterns.items():
#             if pattern in target_market.lower():
#                 return {"pattern": description}
        
#         return {"pattern": "Moderate seasonality"}
    
#     async def _analyze_market_concentration(self, competitors: Dict) -> str:
#         """Analyze market concentration level"""
#         direct_competitors = len(competitors.get('direct', []))
        
#         if direct_competitors == 0:
#             return "Fragmented (no clear leaders)"
#         elif direct_competitors < 5:
#             return "Oligopolistic (few dominant players)"
#         else:
#             return "Competitive (many players)"
    
#     async def _generate_comprehensive_report(self, claimed_size: str, target_market: str, results: Dict) -> Dict:
#         """Generate final comprehensive market analysis report"""
        
#         validation = results.get("market_validation", {})
#         competition = results.get("competitive_landscape", {})
#         trends = results.get("market_trends", {})
#         benchmarks = results.get("industry_benchmarks", {})
#         risks = results.get("risk_assessment", {})
        
#         return {
#             "executive_summary": {
#                 "market_claim": claimed_size,
#                 "validation_confidence": validation.get("confidence_score", 0),
#                 "competitive_intensity": competition.get("competitive_intensity", "Unknown"),
#                 "market_potential": self._assess_market_potential(validation, trends),
#                 "key_risks": risks.get("market_risks", [])[:3]
#             },
#             "market_validation": validation,
#             "competitive_analysis": competition,
#             "market_trends": trends,
#             "industry_benchmarks": benchmarks,
#             "risk_assessment": risks,
#             "recommendations": await self._generate_recommendations(results),
#             "timestamp": self._get_current_timestamp()
#         }
    
#     def _assess_market_potential(self, validation: Dict, trends: Dict) -> str:
#         """Assess overall market potential"""
#         confidence = validation.get("confidence_score", 0)
#         trend_direction = trends.get("trend_direction", "neutral")
        
#         if confidence >= 70 and trend_direction == "positive":
#             return "High Potential"
#         elif confidence >= 50:
#             return "Moderate Potential"
#         else:
#             return "Needs Further Validation"
    
#     async def _generate_recommendations(self, results: Dict) -> List[str]:
#         """Generate actionable recommendations based on analysis"""
#         recommendations = []
        
#         validation = results.get("market_validation", {})
#         competition = results.get("competitive_landscape", {})
#         risks = results.get("risk_assessment", {})
        
#         # Market validation recommendations
#         if validation.get("confidence_score", 0) < 60:
#             recommendations.append("Conduct deeper market size validation with primary research")
        
#         # Competition recommendations
#         if competition.get("competitive_intensity") == "High competition":
#             recommendations.append("Focus on clear differentiation and unique value proposition")
#         elif competition.get("competitive_intensity") == "Low competition":
#             recommendations.append("Validate market demand and customer willingness to pay")
        
#         # Risk mitigation recommendations
#         if risks.get("market_risks"):
#             recommendations.append("Develop risk mitigation strategies for identified market risks")
        
#         # Always include these
#         recommendations.extend([
#             "Validate assumptions with customer interviews",
#             "Monitor key market indicators regularly",
#             "Benchmark performance against industry standards"
#         ])
        
#         return recommendations
    
#     def _get_current_timestamp(self) -> str:
#         """Get current timestamp for report"""
#         from datetime import datetime
#         return datetime.now().isoformat()

# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     # Google Custom Search
#     GOOGLE_SEARCH_KEY = os.getenv('GOOGLE_SEARCH_KEY')
#     GOOGLE_SEARCH_Engine_Id = os.getenv('GOOGLE_SEARCH_Engine_Id')
    
#     # Alpha Vantage
#     ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    
#     # Crunchbase
#     # CRUNCHBASE_API_KEY = os.getenv('CRUNCHBASE_API_KEY')
    
#     # RapidAPI
#     RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    
#     # World Bank & IMF (no keys needed)
#     WORLD_BANK_URL = "https://api.worldbank.org/v2/"
#     IMF_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"



from google.adk.sessions import InMemorySessionService
import google.adk as adk
from google.genai import types
from google.adk.agents import Agent
from typing import List, Dict, Optional
import json
import logging
import re
import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

# ===== Logging Setup =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("market_analyst_agent")

# ===== Market Analysis Tool =====
async def analyze_market_tool(market_size_claim: str, target_market: str) -> str:
    """
    Market Analysis Tool - Validates market claims and analyzes competitive landscape
    """
    try:
        logger.info(f"Analyzing market: {market_size_claim} for {target_market}")
        
        # Perform comprehensive market analysis
        analysis = await perform_market_analysis(market_size_claim, target_market)
        return json.dumps(analysis)
        
    except Exception as e:
        logger.error(f"Market analysis error: {e}")
        return json.dumps({"error": f"Market analysis failed: {str(e)}"})

async def perform_market_analysis(market_size_claim: str, target_market: str) -> Dict:
    """
    Perform comprehensive market analysis using free APIs
    """
    logger.info(f"Starting market analysis for: {target_market}")
    
    # Run all analysis components in parallel
    tasks = {
        "market_validation": validate_market_size(market_size_claim, target_market),
        "competitive_analysis": analyze_competitive_landscape(target_market),
        "market_trends": analyze_market_trends(target_market),
        "industry_benchmarks": get_industry_benchmarks(target_market),
        "risk_assessment": assess_market_risks(target_market)
    }
    
    results = {}
    for task_name, task in tasks.items():
        try:
            results[task_name] = await task
            logger.info(f"✅ {task_name} completed")
        except Exception as e:
            logger.error(f"❌ {task_name} failed: {e}")
            results[task_name] = {}
    
    # Generate final report
    return await generate_market_report(market_size_claim, target_market, results)

async def validate_market_size(claimed_size: str, target_market: str) -> Dict:
    """Validate market size claims using multiple data sources"""
    extracted_size = extract_market_size_numbers(claimed_size)
    
    # Run validation from multiple sources
    google_results = await google_market_validation(target_market, extracted_size)
    world_bank_data = await world_bank_validation(target_market)
    
    return {
        "claimed_size": claimed_size,
        "extracted_values": extracted_size,
        "google_validation": google_results,
        "world_bank_data": world_bank_data,
        "confidence_score": calculate_validation_confidence(google_results, world_bank_data)
    }

async def google_market_validation(target_market: str, extracted_size: Dict) -> Dict:
    """Use Google Search to validate market claims"""
    api_key = os.getenv('GOOGLE_API_KEY')
    cx = os.getenv('GOOGLE_CSE_ID')
    
    if not api_key or not cx:
        return {"error": "Google API not configured"}
    
    try:
        queries = [
            f'"{target_market}" market size 2024',
            f'global {target_market} industry statistics',
            f'{target_market} TAM SAM SOM analysis'
        ]
        
        all_results = []
        for query in queries[:2]:  # Limit to save API calls
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cx,
                'q': query,
                'num': 3
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        for item in data.get('items', []):
                            all_results.append({
                                'title': item.get('title'),
                                'link': item.get('link'),
                                'snippet': item.get('snippet'),
                                'relevance_score': calculate_relevance(item.get('snippet', ''), target_market)
                            })
        
        return {
            "sources_checked": len(all_results),
            "relevant_sources": [r for r in all_results if r['relevance_score'] > 0.3],
            "validation_queries": queries[:2]
        }
        
    except Exception as e:
        return {"error": str(e)}

async def world_bank_validation(target_market: str) -> Dict:
    """Use World Bank data for macroeconomic validation"""
    try:
        # Map common markets to World Bank indicators
        indicator_mapping = {
            'retail': 'NE.CON.PRVT.CD',
            'technology': 'IT.NET.USER.ZS',
            'ecommerce': 'IT.NET.USER.ZS',
            'automotive': 'IS.VEH.NVEH.P3',
            'finance': 'FS.AST.PRVT.GD.ZS'
        }
        
        relevant_indicator = None
        for keyword, indicator in indicator_mapping.items():
            if keyword in target_market.lower():
                relevant_indicator = indicator
                break
        
        if not relevant_indicator:
            return {"info": "No specific World Bank indicator found"}
        
        url = f"https://api.worldbank.org/v2/country/IND/indicator/{relevant_indicator}"
        params = {'format': 'json', 'date': '2020:2024', 'per_page': 5}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return process_world_bank_response(data, target_market)
                else:
                    return {"error": f"World Bank API returned status {response.status}"}
                    
    except Exception as e:
        return {"error": str(e)}

async def analyze_competitive_landscape(target_market: str) -> Dict:
    """Analyze competitors and market positioning"""
    competitors = await find_competitors(target_market)
    
    return {
        "direct_competitors": competitors.get("direct", []),
        "indirect_competitors": competitors.get("indirect", []),
        "market_concentration": await analyze_market_concentration(competitors),
        "competitive_intensity": assess_competitive_intensity(competitors)
    }

async def find_competitors(target_market: str) -> Dict:
    """Find direct and indirect competitors using Google Search"""
    api_key = os.getenv('GOOGLE_API_KEY')
    cx = os.getenv('GOOGLE_CSE_ID')
    
    if not api_key or not cx:
        return {"direct": [], "indirect": [], "key_players": []}
    
    try:
        query = f'"{target_market}" competitors market players'
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cx,
            'q': query,
            'num': 5
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return extract_competitors_from_search(data.get('items', []), target_market)
                    
    except Exception as e:
        logger.error(f"Competitor search error: {e}")
    
    return {"direct": [], "indirect": [], "key_players": []}

async def analyze_market_trends(target_market: str) -> Dict:
    """Analyze current market trends and growth patterns"""
    trends_data = await google_trends_analysis(target_market)
    
    return {
        "market_trends": trends_data,
        "growth_patterns": await analyze_growth_patterns(target_market),
        "market_maturity": assess_market_maturity(target_market)
    }

async def google_trends_analysis(target_market: str) -> Dict:
    """Analyze market trends using Google Search"""
    api_key = os.getenv('GOOGLE_API_KEY')
    cx = os.getenv('GOOGLE_CSE_ID')
    
    if not api_key or not cx:
        return {"error": "Google API not configured"}
    
    try:
        query = f'"{target_market}" market trends 2024 growth forecast'
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cx,
            'q': query,
            'num': 3
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return process_trends_data(data.get('items', []))
                    
    except Exception as e:
        return {"error": str(e)}

async def get_industry_benchmarks(target_market: str) -> Dict:
    """Get industry-specific benchmarks and KPIs"""
    return {
        "revenue_benchmarks": await fetch_revenue_benchmarks(target_market),
        "growth_benchmarks": await fetch_growth_benchmarks(target_market),
        "kpi_standards": analyze_standard_kpis(target_market)
    }

async def assess_market_risks(target_market: str) -> Dict:
    """Assess market risks and opportunities"""
    return {
        "market_risks": await identify_market_risks(target_market),
        "growth_opportunities": await identify_market_opportunities(target_market),
        "regulatory_factors": await analyze_regulatory_factors(target_market),
        "economic_sensitivity": assess_economic_sensitivity(target_market)
    }

async def generate_market_report(claimed_size: str, target_market: str, results: Dict) -> Dict:
    """Generate final comprehensive market analysis report"""
    
    validation = results.get("market_validation", {})
    competition = results.get("competitive_analysis", {})
    trends = results.get("market_trends", {})
    benchmarks = results.get("industry_benchmarks", {})
    risks = results.get("risk_assessment", {})
    
    return {
        "market_analysis": {
            "executive_summary": {
                "market_claim": claimed_size,
                "validation_confidence": validation.get("confidence_score", 0),
                "competitive_intensity": competition.get("competitive_intensity", "Unknown"),
                "market_potential": assess_market_potential(validation, trends),
                "key_risks": risks.get("market_risks", [])[:3]
            },
            "market_validation": validation,
            "competitive_analysis": competition,
            "market_trends": trends,
            "industry_benchmarks": benchmarks,
            "risk_assessment": risks,
            "recommendations": generate_market_recommendations(results)
        }
    }

# ===== Helper Functions =====
def extract_market_size_numbers(text: str) -> Dict:
    """Extract numerical values from market size claims"""
    patterns = {
        'billion': r'[\$]?([\d\.]+)\s*[Bb]illion',
        'million': r'[\$]?([\d\.]+)\s*[Mm]illion',
        'trillion': r'[\$]?([\d\.]+)\s*[Tt]rillion',
        'year': r'by\s*(\d{4})|in\s*(\d{4})'
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            clean_matches = []
            for match in matches:
                if isinstance(match, tuple):
                    clean_matches.extend([m for m in match if m])
                else:
                    clean_matches.append(match)
            extracted[key] = clean_matches[0] if clean_matches else None
    
    return extracted

def process_world_bank_response(data: Dict, target_market: str) -> Dict:
    """Process World Bank API response"""
    if not data or len(data) < 2:
        return {"info": "No data available from World Bank"}
    
    indicators = data[1]
    latest_data = []
    
    for item in indicators[:3]:
        if item.get('value'):
            latest_data.append({
                'year': item.get('date'),
                'value': item.get('value'),
                'indicator': item.get('indicator', {}).get('value', '')
            })
    
    return {
        "latest_data": latest_data,
        "trend": "growing" if len(latest_data) > 1 and latest_data[0]['value'] > latest_data[-1]['value'] else "stable/declining"
    }

def extract_competitors_from_search(search_results: List, target_market: str) -> Dict:
    """Extract competitor information from search results"""
    competitors = {"direct": [], "indirect": [], "key_players": []}
    
    for item in search_results:
        snippet = item.get('snippet', '').lower()
        title = item.get('title', '').lower()
        
        if any(term in snippet for term in ['competitor', 'competitive', 'vs', 'alternative']):
            competitors["direct"].append({
                'name': item.get('title'),
                'source': item.get('link'),
                'type': 'direct'
            })
        elif any(term in title for term in [target_market.lower(), 'market', 'industry']):
            competitors["key_players"].append({
                'name': item.get('title'),
                'source': item.get('link'),
                'type': 'key_player'
            })
        else:
            competitors["indirect"].append({
                'name': item.get('title'),
                'source': item.get('link'),
                'type': 'indirect'
            })
    
    return competitors

def process_trends_data(items: List) -> Dict:
    """Process trends data from search results"""
    trends = []
    
    for item in items:
        snippet = item.get('snippet', '')
        if any(term in snippet.lower() for term in ['growth', 'increasing', 'rising', 'forecast']):
            trends.append({
                'source': item.get('title'),
                'trend_indication': snippet[:200],
                'confidence': 'high' if 'report' in item.get('title', '').lower() else 'medium'
            })
    
    return {
        "trends_found": len(trends),
        "trend_direction": "positive" if len(trends) > 2 else "neutral",
        "sources": trends
    }

def calculate_relevance(snippet: str, target_market: str) -> float:
    """Calculate relevance score between snippet and target market"""
    snippet_lower = snippet.lower()
    market_terms = target_market.lower().split()
    
    relevance = 0.0
    for term in market_terms:
        if term in snippet_lower:
            relevance += 0.2
    
    key_terms = ['market', 'size', 'growth', 'industry', 'report']
    for term in key_terms:
        if term in snippet_lower:
            relevance += 0.1
    
    return min(relevance, 1.0)

def calculate_validation_confidence(google_results: Dict, world_bank_data: Dict) -> int:
    """Calculate overall validation confidence score (0-100)"""
    confidence = 0
    
    if 'relevant_sources' in google_results:
        confidence += min(len(google_results['relevant_sources']) * 20, 60)
    
    if 'latest_data' in world_bank_data and world_bank_data['latest_data']:
        confidence += 20
    
    if 'error' in google_results or 'error' in world_bank_data:
        confidence = max(confidence - 20, 0)
    
    return min(confidence, 100)

async def analyze_market_concentration(competitors: Dict) -> str:
    """Analyze market concentration level"""
    direct_competitors = len(competitors.get('direct', []))
    
    if direct_competitors == 0:
        return "Fragmented (no clear leaders)"
    elif direct_competitors < 5:
        return "Oligopolistic (few dominant players)"
    else:
        return "Competitive (many players)"

def assess_competitive_intensity(competitors: Dict) -> str:
    """Assess competitive intensity based on competitor analysis"""
    total_competitors = len(competitors.get('direct', [])) + len(competitors.get('indirect', []))
    
    if total_competitors > 10:
        return "High competition"
    elif total_competitors > 5:
        return "Moderate competition"
    else:
        return "Low competition"

async def analyze_growth_patterns(target_market: str) -> Dict:
    """Analyze market growth patterns"""
    return {
        "estimated_cagr": "8-12%",
        "growth_drivers": await identify_growth_drivers(target_market),
        "market_maturity": assess_market_maturity(target_market)
    }

async def identify_growth_drivers(target_market: str) -> List:
    """Identify key growth drivers for the market"""
    common_drivers = {
        'technology': ['Digital adoption', 'Mobile penetration', 'IoT expansion'],
        'retail': ['E-commerce growth', 'Consumer spending', 'Urbanization'],
        'finance': ['Digital payments', 'Financial inclusion', 'Regulatory changes']
    }
    
    for sector, drivers in common_drivers.items():
        if sector in target_market.lower():
            return drivers
    
    return ['Market expansion', 'Consumer demand', 'Technological advancement']

def assess_market_maturity(target_market: str) -> str:
    """Assess market maturity level"""
    emerging_terms = ['tech', 'digital', 'ai', 'blockchain', 'edtech', 'fintech']
    mature_terms = ['retail', 'manufacturing', 'real estate', 'agriculture']
    
    if any(term in target_market.lower() for term in emerging_terms):
        return "Emerging"
    elif any(term in target_market.lower() for term in mature_terms):
        return "Mature"
    else:
        return "Growth"

async def fetch_revenue_benchmarks(target_market: str) -> Dict:
    """Fetch revenue benchmarks for the industry"""
    return {
        "early_stage": "$1-5M ARR",
        "growth_stage": "$5-20M ARR",
        "mature": "$20M+ ARR"
    }

async def fetch_growth_benchmarks(target_market: str) -> Dict:
    """Fetch growth benchmarks for the industry"""
    return {
        "early_stage": "100-200% YoY",
        "growth_stage": "50-100% YoY",
        "mature": "20-50% YoY"
    }

def analyze_standard_kpis(target_market: str) -> List:
    """Analyze standard KPIs for the industry"""
    kpi_templates = {
        'ecommerce': ['CAC', 'LTV', 'Conversion Rate', 'AOV', 'Churn Rate'],
        'saas': ['MRR', 'ARR', 'Churn Rate', 'LTV:CAC', 'Net Retention'],
        'marketplace': ['GMV', 'Take Rate', 'Buyer/Seller Ratio', 'Network Effects']
    }
    
    for sector, kpis in kpi_templates.items():
        if sector in target_market.lower():
            return kpis
    
    return ['Revenue Growth', 'Customer Acquisition', 'Profit Margins', 'Market Share']

async def identify_market_risks(target_market: str) -> List:
    """Identify potential market risks"""
    common_risks = {
        'technology': ['Rapid obsolescence', 'Regulatory changes', 'Cybersecurity threats'],
        'retail': ['Economic downturns', 'Supply chain disruptions', 'Changing consumer preferences'],
        'finance': ['Regulatory compliance', 'Market volatility', 'Credit risks']
    }
    
    for sector, risks in common_risks.items():
        if sector in target_market.lower():
            return risks
    
    return ['Market competition', 'Economic factors', 'Regulatory environment']

async def identify_market_opportunities(target_market: str) -> List:
    """Identify market opportunities"""
    return [
        "Digital transformation initiatives",
        "Growing consumer demand",
        "Emerging market segments",
        "Technology enablement"
    ]

async def analyze_regulatory_factors(target_market: str) -> Dict:
    """Analyze regulatory factors affecting the market"""
    return {
        "regulatory_environment": "Moderate",
        "compliance_requirements": ["Data privacy", "Consumer protection"],
        "licensing_needs": ["Business registration", "Industry-specific licenses"]
    }

def assess_economic_sensitivity(target_market: str) -> str:
    """Assess how sensitive the market is to economic conditions"""
    sensitive_sectors = ['luxury', 'real estate', 'automotive', 'travel']
    resilient_sectors = ['healthcare', 'education', 'essential retail', 'utilities']
    
    if any(sector in target_market.lower() for sector in sensitive_sectors):
        return "High sensitivity to economic cycles"
    elif any(sector in target_market.lower() for sector in resilient_sectors):
        return "Resilient to economic cycles"
    else:
        return "Moderate sensitivity to economic cycles"

def assess_market_potential(validation: Dict, trends: Dict) -> str:
    """Assess overall market potential"""
    confidence = validation.get("confidence_score", 0)
    trend_direction = trends.get("trend_direction", "neutral")
    
    if confidence >= 70 and trend_direction == "positive":
        return "High Potential"
    elif confidence >= 50:
        return "Moderate Potential"
    else:
        return "Needs Further Validation"

def generate_market_recommendations(results: Dict) -> List[str]:
    """Generate actionable recommendations based on analysis"""
    recommendations = []
    
    validation = results.get("market_validation", {})
    competition = results.get("competitive_analysis", {})
    risks = results.get("risk_assessment", {})
    
    if validation.get("confidence_score", 0) < 60:
        recommendations.append("Conduct deeper market size validation with primary research")
    
    if competition.get("competitive_intensity") == "High competition":
        recommendations.append("Focus on clear differentiation and unique value proposition")
    elif competition.get("competitive_intensity") == "Low competition":
        recommendations.append("Validate market demand and customer willingness to pay")
    
    if risks.get("market_risks"):
        recommendations.append("Develop risk mitigation strategies for identified market risks")
    
    recommendations.extend([
        "Validate assumptions with customer interviews",
        "Monitor key market indicators regularly",
        "Benchmark performance against industry standards"
    ])
    
    return recommendations

# ===== Agent Definition =====
market_agent_instruction = """
You are the **Market Analyst Agent**.

Your task is to perform structured market analysis by calling the `analyze_market_tool` function.

---

### 🚨 CRITICAL RULES
1. **You must call** the function `analyze_market_tool(market_size_claim, target_market)`.  
2. **You must NOT** generate or summarize any text yourself.  
3. **You must NOT** invent or modify data.  
4. **Your only output** should be a **function call event**, not text or JSON you wrote.  
5. The tool's returned JSON is the final output — do not alter it.

---

### 🧩 Input
You will receive structured startup analysis JSON from the previous agent, containing:
- `market` (object) → includes `market_size_claim` and `target_market`

---

### What To Do
1. Extract the `market_size_claim` and `target_market` from the input.
2. Then immediately call: 
   - analyze_market_tool(market_size_claim=..., target_market=...)
3. The output from the tool is the **only** thing you return.

---

**Example of CORRECT behavior**:
Input from first agent: 
{
  "market": {
    "market_size_claim": "$350 B Global Secondhand Market by 2027",
    "target_market": "Women, Men, Kids"
  }
}

You create:
  market_size_claim = "$350 B Global Secondhand Market by 2027"
  target_market = "Women, Men, Kids"

Then call: analyze_market_tool("$350 B Global Secondhand Market by 2027", "Women, Men, Kids")

**Output Format**: ALWAYS return valid JSON with this exact structure:
{
  "market_analysis": {
    "executive_summary": {
      "market_claim": "string",
      "validation_confidence": 0-100,
      "competitive_intensity": "string",
      "market_potential": "string",
      "key_risks": ["string"]
    },
    "market_validation": {...},
    "competitive_analysis": {...},
    "market_trends": {...},
    "industry_benchmarks": {...},
    "risk_assessment": {...},
    "recommendations": ["string"]
  }
}

**Failure to call the tool will result in missing critical market data and inaccurate analysis.**
"""

market_analyst_agent = Agent(
    name="market_analyst_agent",
    model="gemini-2.0-flash-exp",
    instruction=market_agent_instruction,
    tools=[analyze_market_tool],
)

async def run_market_agent(agent_input: dict) -> dict:
    """
    Run the market analyst agent
    """
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name="market_analysis_app",
        user_id="user123",
        session_id="session1"
    )
    
    runner = adk.Runner(agent=market_analyst_agent, app_name="market_analysis_app", session_service=session_service)
    
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
            # When agent outputs plain text
            if part.text:
                raw_text = part.text.strip()
                cleaned_text = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.MULTILINE)
                logger.info(f"Market Agent Output: {cleaned_text}")
                final_output = cleaned_text

            # When agent calls the tool (expected behavior)
            elif part.function_call:
                logger.info(f"Market Agent Tool Call: {part.function_call.name}({part.function_call.args})")
    
    if not final_output:
        return {"error": "Market agent returned no output"}
    
    try:
        return json.loads(final_output)
    except json.JSONDecodeError:
        return {"error": "Failed to parse agent output as JSON", "raw_output": final_output}