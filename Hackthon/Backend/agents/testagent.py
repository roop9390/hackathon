# # import asyncio
# # import json
# # from market_practice_agent import run_market_agent

# # agent_input = {
# #     "market": {
# #         "market_size_claim": "$350 B Global Secondhand Market by 2027",
# #         "target_market": "Women, Men, Kids"
# #     }
# # }

# # async def main():
# #     result = await run_market_agent(agent_input)
# #     print(json.dumps(result, indent=2))

# # if __name__ == "__main__":
# #     asyncio.run(main())
# # testagent.py
# import asyncio
# import json
# import time
# from market_agent import run_market_agent

# async def main():
#     agent_input = {
#         "market": {
#             "market_size_claim": "$350 B Global Secondhand Market by 2027", 
#             "target_market": "Women, Men, Kids"
#         }
#     }
    
#     # Add delay to avoid quota issues
#     print("🔄 Starting market analysis...")
#     await asyncio.sleep(1)
    
#     result = await run_market_agent(agent_input)
#     print("✅ Market Analysis Completed!")
#     print("Market Analysis Result:", json.dumps(result, indent=2))

# if __name__ == "__main__":
#     asyncio.run(main())