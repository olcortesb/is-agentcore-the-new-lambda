from bedrock_agentcore import BedrockAgentCoreApp
import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = BedrockAgentCoreApp()

# Initialize SQS client
sqs = boto3.client('sqs', region_name='us-west-2')

@app.entrypoint
def invoke(payload):
    """Your AI agent function that sends results to SQS"""
    prompt_data = payload.get("prompt", {})
    
    # Extract numbers a and b from the prompt
    a = prompt_data.get("a", 0)
    b = prompt_data.get("b", 0)
    
    # Calculate the sum
    result = a + b
    
    # Send result to SQS
    try:
        queue_url = os.environ.get('SQS_QUEUE_URL')
        
        if not queue_url:
            raise ValueError("SQS_QUEUE_URL environment variable is required")
        
        message = {
            'operation': 'sum',
            'input': {'a': a, 'b': b},
            'result': result,
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'agentcore'
        }
        
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        
        return {
            "result": result,
            "message_sent": True,
            "message_id": response.get('MessageId')
        }
        
    except Exception as e:
        return {
            "result": result,
            "message_sent": False,
            "error": str(e)
        }

if __name__ == "__main__":
    app.run()