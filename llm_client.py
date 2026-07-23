"""
LLM Integration Client using boto3 for AWS Bedrock.
----------------------------------------------------
Handles direct interaction with Amazon Bedrock endpoints via Converse API.
"""

import json
import logging
from typing import Dict, Any
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, MODEL_ID
from prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def get_bedrock_client():
    """Helper function to instantiate a reusable boto3 Bedrock Runtime client."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


# Reusable Bedrock client instance
bedrock = get_bedrock_client()


def generate_summary(meeting_notes_text: str) -> Dict[str, Any]:
    """
    Sends meeting notes to Claude via Bedrock Converse API and returns 
    a structured summary dictionary.

    Args:
        meeting_notes_text: The raw meeting notes string.

    Returns:
        A dictionary structured with summary, action items, key decisions, 
        and open questions.
    """
    try:
        response = bedrock.converse(
            modelId=MODEL_ID,
            system=[{"text": SYSTEM_PROMPT}],
            messages=[
                {
                    "role": "user",
                    "content": [{"text": f"Here are the meeting notes:\n\n{meeting_notes_text}"}]
                }
            ],
            inferenceConfig={
                "maxTokens": 2000,
                "temperature": 0.2
            }
        )

        # Parse output from Bedrock Converse API
        output_text = response["output"]["message"]["content"][0]["text"].strip()
        
        # Clean potential markdown code fences if Claude wraps the JSON in ```json
        if output_text.startswith("```"):
            output_text = output_text.split("```")[1]
            if output_text.startswith("json"):
                output_text = output_text[4:]
            output_text = output_text.strip()

        # Parse JSON output into Python dictionary
        result = json.loads(output_text)
        
        # Inject token usage stats if available
        if "usage" in response:
            result["token_usage"] = {
                "input": response["usage"].get("inputTokens", 0),
                "output": response["usage"].get("outputTokens", 0),
                "total": response["usage"].get("totalTokens", 0)
            }

        return result

    except (BotoCoreError, ClientError, json.JSONDecodeError, Exception) as e:
        logger.warning(f"Bedrock invocation error, using fallback contract: {str(e)}")
        # Fallback response matching API schema if model call or parsing fails
        return {
            "summary": "This is a fallback summary generated due to an API processing error.",
            "action_items": [
                "Verify API configuration and model JSON schema output."
            ],
            "key_decisions": [],
            "open_questions": [],
            "token_usage": {
                "input": 0,
                "output": 0,
                "total": 0
            }
        }