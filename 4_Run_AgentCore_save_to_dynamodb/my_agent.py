from bedrock_agentcore import BedrockAgentCoreApp
import boto3
import json
import os
import uuid
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = BedrockAgentCoreApp()

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

@app.entrypoint
def invoke(payload):
    """Your AI agent function that stores results in DynamoDB"""
    prompt_data = payload.get("prompt", {})
    
    # Extract numbers a and b from the prompt
    a = prompt_data.get("a", 0)
    b = prompt_data.get("b", 0)
    
    # Calculate the sum
    result = a + b
    
    # Prepare item for DynamoDB
    item_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    
    item = {
        'id': item_id,
        'timestamp': now.isoformat(),
        'operation': 'sum',
        'input_a': a,
        'input_b': b,
        'result': result,
        'source': 'agentcore',
        'ttl': int(now.timestamp() + 86400 * 30)  # 30 days TTL
    }
    
    # Store in DynamoDB
    try:
        table_name = os.environ.get('DYNAMODB_TABLE_NAME')
        if not table_name:
            raise ValueError("DYNAMODB_TABLE_NAME environment variable is required")
        
        # Get delay time from environment variable (default to 0 seconds)
        delay_seconds = int(os.environ.get('DELAY_SECONDS', '0'))
        
        # Wait before storing in DynamoDB
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        
        table = dynamodb.Table(table_name)
        table.put_item(Item=item)
        
        return {
            "result": result,
            "dynamodb_stored": True,
            "item_id": item_id,
            "timestamp": item['timestamp']
        }
        
    except Exception as e:
        return {
            "result": result,
            "dynamodb_stored": False,
            "error": str(e)
        }

if __name__ == "__main__":
    app.run()