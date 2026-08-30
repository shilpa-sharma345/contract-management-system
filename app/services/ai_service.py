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

    IMPORTANT DATE INSTRUCTIONS:
    - Look for dates in ALL locations: tables, headers, "Effective Date", "Commencement Date", 
      "Start Date", "Expiry Date", "End Date", "Term", "Expiration Date", "Valid Until", 
      "Contract Period" fields anywhere in the document.
    - Dates may appear in formats like "1 July 2024", "01/07/2024", "July 1, 2024", "2024-07-01" — extract all of them.
    - start_date = the date the contract becomes effective / commences
    - end_date = the date the contract expires / ends
    - Always return dates in YYYY-MM-DD format.
    - If you find ANY date that could be a start or end date, return it. Do NOT return null unless absolutely no date exists anywhere in the document.

    Return ONLY a valid JSON object with exactly these fields, no extra text, no markdown:
    {{
        "supplier": "name of the supplier or vendor company, or 'Not specified' if not found",
        "value": "contract value or amount (e.g. INR 12,00,000 or £24,000/yr), or 'Not specified' if not found",
        "start_date": "contract start date in YYYY-MM-DD format, or null only if truly not found anywhere",
        "end_date": "contract end date/expiry date in YYYY-MM-DD format, or null only if truly not found anywhere",
        "notice_period": "notice period (e.g. 30 days), or 'Not specified' if not found",
        "ai_summary": "2-3 sentence plain English summary of what this contract is about",
        "risk_flag": "ALWAYS provide a risk assessment — identify the single most important risk or concern in this contract. If low risk, state 'Low risk — standard terms with no major concerns identified'.",
        "key_clauses": "comma separated list of all key clauses found in the contract"
    }}

    Contract Text:
    {contract_text[:6000]}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        result = json.loads(raw)

        # Fallback guards
        if not result.get("risk_flag"):
            result["risk_flag"] = "Low risk — no major concerns identified"
        if not result.get("supplier"):
            result["supplier"] = "Not specified"
        if not result.get("value"):
            result["value"] = "Not specified"
        if not result.get("notice_period"):
            result["notice_period"] = "Not specified"

        return result

    except json.JSONDecodeError:
        return {
            "supplier": "Not specified",
            "value": "Not specified",
            "start_date": None,
            "end_date": None,
            "notice_period": "Not specified",
            "ai_summary": "Could not analyze contract automatically.",
            "risk_flag": "Unable to assess risk — manual review required",
            "key_clauses": None
        }
    except Exception as e:
        raise Exception(f"Gemini AI error: {str(e)}")