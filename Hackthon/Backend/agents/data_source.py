# import requests
# import json
# import logging
# from bs4 import BeautifulSoup
# from typing import Dict, List, Optional
# from config import Config

# logger = logging.getLogger(__name__)

# class NewsAPIClient:
#     """Client for NewsAPI to get company/founder news"""
    
#     def __init__(self):
#         self.api_key = Config.NEWSAPI_KEY
#         self.base_url = "https://newsapi.org/v2"
    
#     def get_company_news(self, company_name: str) -> List[Dict]:
#         """Get recent news articles about the company"""
#         try:
#             url = f"{self.base_url}/everything"
#             params = {
#                 'q': f'"{company_name}"',
#                 'sortBy': 'relevancy',
#                 'pageSize': 10,
#                 'apiKey': self.api_key
#             }
            
#             response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
#             response.raise_for_status()
            
#             data = response.json()
#             return data.get('articles', [])
            
#         except Exception as e:
#             logger.error(f"NewsAPI error for {company_name}: {e}")
#             return []
    
#     def get_person_news(self, person_name: str, company_name: str) -> List[Dict]:
#         """Get news articles about a specific person"""
#         try:
#             url = f"{self.base_url}/everything"
#             params = {
#                 'q': f'"{person_name}" "{company_name}"',
#                 'sortBy': 'relevancy',
#                 'pageSize': 5,
#                 'apiKey': self.api_key
#             }
            
#             response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
#             response.raise_for_status()
            
#             data = response.json()
#             return data.get('articles', [])
            
#         except Exception as e:
#             logger.error(f"NewsAPI error for {person_name}: {e}")
#             return []

# class GoogleSearchClient:
#     """Client for Google Custom Search API"""
    
#     def __init__(self):
#         self.api_key = Config.GOOGLE_SEARCH_KEY
#         self.cx = Config.GOOGLE_CX
    
#     def search_person(self, person_name: str, company_name: str) -> List[Dict]:
#         """Search for information about a person"""
#         try:
#             url = "https://www.googleapis.com/customsearch/v1"
#             params = {
#                 'q': f'{person_name} {company_name} founder',
#                 'key': self.api_key,
#                 'cx': self.cx,
#                 'num': 5
#             }
            
#             response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
#             response.raise_for_status()
            
#             data = response.json()
#             return data.get('items', [])
            
#         except Exception as e:
#             logger.error(f"Google Search error for {person_name}: {e}")
#             return []

# class WebsiteScraper:
#     """Scrape company website for team information"""
    
#     @staticmethod
#     def extract_team_info(html_content: str) -> Dict:
#         """Extract team information from company website HTML"""
#         try:
#             soup = BeautifulSoup(html_content, 'html.parser')
            
#             # Look for common team section patterns
#             team_data = {
#                 'bios_found': False,
#                 'team_section': False,
#                 'about_page': False
#             }
            
#             # Check for common team-related elements
#             team_keywords = ['team', 'about', 'founder', 'leadership', 'crew']
#             for keyword in team_keywords:
#                 if soup.find(text=lambda t: t and keyword in t.lower()):
#                     team_data['team_section'] = True
            
#             # Look for person bios
#             bios = soup.find_all(['div', 'section'], class_=lambda x: x and any(
#                 kw in str(x).lower() for kw in ['bio', 'team', 'member', 'founder']
#             ))
            
#             if bios:
#                 team_data['bios_found'] = True
            
#             return team_data
            
#         except Exception as e:
#             logger.error(f"Website scraping error: {e}")
#             return {}