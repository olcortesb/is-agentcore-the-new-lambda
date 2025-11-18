import json
import boto3
import logging
import os
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function that acts as a proxy between API Gateway and AgentCore
    """
    try:
        # Log the incoming event
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract the request body
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Missing request body',
                    'message': 'Please provide a JSON body with the calculation request'
                })
            }
        
        # Parse the request body
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Invalid JSON',
                    'message': 'Request body must be valid JSON'
                })
            }
        
        # Validate the request structure
        if 'prompt' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Missing prompt',
                    'message': 'Request must include a "prompt" field'
                })
            }
        
        # Get AgentCore configuration from environment variables
        agent_id = os.environ.get('AGENTCORE_AGENT_ID')
        if not agent_id:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Configuration error',
                    'message': 'AGENTCORE_AGENT_ID environment variable not set'
                })
            }
        
        # Invoke AgentCore using the correct API
        logger.info(f"Invoking AgentCore with agent_id: {agent_id}")
        
        # Initialize BedrockAgentCore client
        client = boto3.client('bedrock-agentcore', region_name='us-west-2')
        
        # Prepare payload
        payload = json.dumps(body).encode('utf-8')
        
        # Get AWS account ID dynamically
        sts = boto3.client('sts')
        account_id = sts.get_caller_identity()['Account']
        
        # Invoke AgentCore using invoke_agent_runtime
        response = client.invoke_agent_runtime(
            agentRuntimeArn=f"arn:aws:bedrock-agentcore:us-west-2:{account_id}:runtime/{agent_id}",
            payload=payload,
            contentType='application/json',
            accept='application/json',
            runtimeSessionId=context.aws_request_id
        )
        
        # Parse streaming response
        content = []
        for chunk in response['response']:
            content.append(chunk)
        
        response_text = b''.join(content).decode('utf-8')
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            result = {'message': response_text}
        
        logger.info(f"AgentCore response: {result}")
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'data': result,
                'request_id': context.aws_request_id
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e),
                'request_id': context.aws_request_id if context else 'unknown'
            })
        }