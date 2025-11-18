from bedrock_agentcore import BedrockAgentCoreApp
import boto3
import json
import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = BedrockAgentCoreApp()

# Initialize S3 client
s3 = boto3.client('s3', region_name='us-west-2')

@app.entrypoint
def invoke(payload):
    """Your AI agent function that stores results in S3"""
    prompt_data = payload.get("prompt", {})
    
    # Extract numbers a and b from the prompt
    a = prompt_data.get("a", 0)
    b = prompt_data.get("b", 0)
    
    # Calculate the sum
    result = a + b
    
    # Prepare data for S3
    data = {
        'operation': 'sum',
        'input': {'a': a, 'b': b},
        'result': result,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'source': 'agentcore',
        'request_id': str(uuid.uuid4())
    }
    
    # Store in S3
    try:
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required")
        
        # Create S3 key with date partitioning
        now = datetime.now(timezone.utc)
        s3_key = f"agentcore-results/{now.strftime('%Y/%m/%d')}/{data['request_id']}.json"
        
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(data, indent=2),
            ContentType='application/json'
        )
        
        return {
            "result": result,
            "s3_stored": True,
            "s3_key": s3_key,
            "request_id": data['request_id']
        }
        
    except Exception as e:
        return {
            "result": result,
            "s3_stored": False,
            "error": str(e)
        }

if __name__ == "__main__":
    app.run()