None selected 

Skip to content
Using Gmail with screen readers
Conversations
Re: check once
Inbox

Girish Mukim
Attachments
12:40 PM (26 minutes ago)
to me

Lambda code and agent instructions.

On Sun, Dec 14, 2025 at 12:09 PM Ajay Pokale <cdacajay@gmail.com> wrote:
https://builder.aws.com/content/36oWAC9G4gbHqcNQFViEsUeqmo0/how-to-build-a-scalable-rag-based-chatbot-on-aws-a-school-chatbot-assistant
 2 Attachments
  •  Scanned by Gmail
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
    print("http_method:", http_method)
    if http_method == "OPTIONS":
        return create_api_response(200, {})

    if http_method != "POST":
        return create_api_response(405, {"error": "Method not allowed, use POST"})

    try:
        body = json.loads(event.get("body", "{}"))
        question = body.get("question")
        print("question:", question)
        if not question:
            raise ValueError("Missing 'question' field in request body")
    except Exception as e:
        return create_api_response(400, {"error": f"Invalid request body: {str(e)}"})

    # --- Call Bedrock Agent ---
    try:
        import uuid
        session_id = str(uuid.uuid4())
        print("session_id:", session_id)
        response = bedrock.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=question
        )

        # --- FIXED STREAM PROCESSING ---
        answer = ""

        # The "completion" field contains a generator of events
        events = response.get("completion", [])
        print("events:", events)
        for event in events:
            print("event:", event)
            chunk =event.get("chunk")
            print("chunk:", chunk)
            if chunk:
                answer += chunk.get("bytes").decode("utf-8")
                print("answer:", answer)

    except Exception as e:
        print(f"Bedrock Error: {e}")
        return create_api_response(500, {"error": "Bedrock agent invocation failed. Check logs."})

    return create_api_response(200, {"answer": answer})
Lambda.py
Displaying Agent-Instructions.txt.