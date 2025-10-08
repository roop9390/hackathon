from google.adk.sessions import InMemorySessionService
import google.adk as adk
from google.genai import types
from google.adk.agents import Agent
import json
import re
import logging
from dotenv import load_dotenv
from tools.market_analysis_tool import analyze_market_tool

load_dotenv()

# ===== Logging Setup =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("market_analyst_agent")


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
  "recommendations": ["string"],
  "timestamp": "string"
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
    try:
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
    
    except Exception as e:
        logger.error(f"Error running market agent: {e}")
        return {"error": f"Agent execution failed: {str(e)}"}