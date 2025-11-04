from openai import AsyncOpenAI
from typing import List, Dict, Optional
import json
import os
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass


class OpportunityDetector:
    """Service for detecting opportunities using OpenAI"""

    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_key_here":
            raise AIServiceError(
                "OPENAI_API_KEY not configured. Please set a valid OpenAI API key in .env file"
            )
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"

    def _get_system_prompt(self) -> str:
        """System prompt for OpenAI"""
        return """You are an AI assistant for a law firm that identifies business opportunities in client communications.

Your task is to analyze communications and extract potential legal service opportunities.

Focus on these practice areas:
1. Real Estate (office leases, property transactions, zoning)
2. Employment Law (hiring, terminations, HR issues, contracts)
3. Mergers & Acquisitions (acquisitions, sales, due diligence)
4. Intellectual Property (trademarks, patents, copyright)
5. Litigation (lawsuits, disputes, arbitration)

For each opportunity:
- Be specific about what the client needs
- Base confidence on clarity and urgency
- Extract the exact text that indicates the need
- Estimate value if enough information is provided

Return ONLY valid JSON, no additional text."""

    def _build_prompt(self, content: str, client_name: str) -> str:
        """Build user prompt"""
        return f"""Client: {client_name}

Communication:
{content}

Analyze this communication and identify any legal service opportunities.

Return a JSON object with this exact structure:
{{
  "opportunities": [
    {{
      "title": "Brief title (max 60 chars)",
      "description": "What the client needs",
      "type": "real_estate|employment_law|m&a|ip|litigation",
      "confidence": 85,
      "extracted_text": "Exact quote from communication",
      "estimated_value": "$20k-50k" (optional, only if you can estimate)
    }}
  ]
}}

Rules:
- Only include opportunities with confidence >= 40%
- Maximum 5 opportunities per communication
- Be conservative with confidence scores
- If no opportunities found, return empty array
"""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def analyze_communication(
        self,
        content: str,
        client_name: str
    ) -> List[Dict]:
        """
        Analyze communication and extract opportunities.

        Returns:
            List of opportunity dicts with keys:
            - title, description, type, confidence, extracted_text, estimated_value
        """
        try:
            logger.info(f"Analyzing communication for client: {client_name}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._build_prompt(content, client_name)}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=1500
            )

            result_text = response.choices[0].message.content
            logger.debug(f"OpenAI response: {result_text}")

            result = json.loads(result_text)
            opportunities = result.get("opportunities", [])

            # Validate and clean opportunities
            validated = self._validate_opportunities(opportunities)

            logger.info(f"Found {len(validated)} opportunities")
            return validated

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response: {e}")
            raise AIServiceError("Failed to parse AI response")

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AIServiceError(f"AI service error: {str(e)}")

    def _validate_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Validate and normalize opportunity data"""
        validated = []

        valid_types = {"real_estate", "employment_law", "m&a", "ip", "litigation"}

        for opp in opportunities:
            try:
                # Normalize type
                opp_type = opp.get("type", "").lower().replace("&", "").replace(" ", "_")
                if opp_type == "ma":
                    opp_type = "m&a"

                if opp_type not in valid_types:
                    logger.warning(f"Invalid opportunity type: {opp.get('type')}")
                    continue

                # Validate confidence
                confidence = float(opp.get("confidence", 0))
                if confidence < 40 or confidence > 100:
                    logger.warning(f"Invalid confidence: {confidence}")
                    continue

                # Validate required fields
                if not opp.get("title") or not opp.get("description"):
                    logger.warning("Missing required fields")
                    continue

                # Normalize and validate
                validated_opp = {
                    "title": opp["title"][:200],  # Truncate to max length
                    "description": opp["description"],
                    "type": opp_type,
                    "confidence": confidence,
                    "extracted_text": opp.get("extracted_text", opp["description"]),
                    "estimated_value": opp.get("estimated_value"),
                }

                validated.append(validated_opp)

            except (ValueError, KeyError) as e:
                logger.warning(f"Invalid opportunity data: {e}")
                continue

        return validated
