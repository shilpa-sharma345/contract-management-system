from google import genai
from app.constants.environ import GEMINI_API_KEY
import json

# -------------------------
# CONFIGURE GEMINI
# -------------------------
client = genai.Client(api_key=GEMINI_API_KEY)


# -------------------------
# ANALYZE CONTRACT
# -------------------------
async def analyze_contract(contract_text: str) -> dict:
    prompt = f"""
    You are a contract analysis expert. Analyze the following contract text and extract key information.

    Return ONLY a JSON object with exactly these fields, nothing else:
    {{
        "supplier": "name of the supplier or vendor company",
        "value": "contract value or amount (e.g. £24,000/yr)",
        "start_date": "contract start date in YYYY-MM-DD format or null",
        "end_date": "contract end date in YYYY-MM-DD format or null",
        "notice_period": "notice period (e.g. 30 days) or null",
        "ai_summary": "2-3 sentence plain English summary of the contract",
        "risk_flag": "any critical risk or urgent action needed, or null",
        "key_clauses": "comma separated list of key clauses found"
    }}

    Contract Text:
    {contract_text[:5000]}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError:
        return {
            "supplier": None,
            "value": None,
            "start_date": None,
            "end_date": None,
            "notice_period": None,
            "ai_summary": "Could not analyze contract automatically.",
            "risk_flag": None,
            "key_clauses": None
        }
    except Exception as e:
        raise Exception(f"Gemini AI error: {str(e)}")