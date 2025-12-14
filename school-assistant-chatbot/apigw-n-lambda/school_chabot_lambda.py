import json
import boto3
from typing import Dict, Any

bedrock = boto3.client("bedrock-agent-runtime")

AGENT_ID = "PS6HQWI3ND"
AGENT_ALIAS_ID = "TSTALIASID"


def create_api_response(status_code: int, body: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
    if headers is None:
        headers = {"Content-Type": "application/json"}

    headers["Access-Control-Allow-Origin"] = "*"
    headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    headers["Access-Control-Allow-Headers"] = "Content-Type"

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    http_method = event.get("httpMethod")

    if http_method == "OPTIONS":
        return create_api_response(200, {})

    if http_method != "POST":
        return create_api_response(405, {"error": "Method not allowed, use POST"})

    try:
        body = json.loads(event.get("body", "{}"))
        question = body.get("question")
        if not question:
            raise ValueError("Missing 'question' field in request body")
    except Exception as e:
        return create_api_response(400, {"error": f"Invalid request body: {str(e)}"})

    # --- Call Bedrock Agent ---
    try:
        import uuid
        session_id = str(uuid.uuid4())

        response = bedrock.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=question
        )

        # --- FIXED STREAM PROCESSING ---
        answer = ""

        # The "completion" field contains a generator of events
        completion_events = response.get("completion", [])

        for event in completion_events:
            content = event.get("content", [])
            if len(content) > 0:
                text_part = content[0].get("textResponsePart")
                if text_part:
                    answer += text_part.get("text", "")

    except Exception as e:
        print(f"Bedrock Error: {e}")
        return create_api_response(500, {"error": "Bedrock agent invocation failed. Check logs."})

    return create_api_response(200, {"answer": answer})
