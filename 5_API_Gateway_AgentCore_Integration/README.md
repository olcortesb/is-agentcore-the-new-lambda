# Step 5: API Gateway + AgentCore Integration

This step creates a complete HTTP API using API Gateway that proxies requests to AgentCore, completing the serverless stack integration.

## Architecture

```
Internet → API Gateway → Lambda Proxy → AgentCore → DynamoDB
```

**✅ SUCCESS**: AgentCore successfully integrated with API Gateway, proving it can work as "the new Lambda" with HTTP endpoints!

## Manual Deployment

### 1. Prerequisites

```bash
# Install SAM CLI
pip install aws-sam-cli

# Configure AWS credentials and region
aws configure
```

### 2. Get AgentCore Agent ID

```bash
cd ../4_Run_AgentCore_save_to_dynamodb
cat .bedrock_agentcore.yaml | grep agent_id
```

### 3. Build the Application

```bash
sam build
```

### 4. Deploy to AWS

```bash
sam deploy \
    --stack-name agentcore-api-gateway-integration \
    --parameter-overrides AgentCoreAgentId=YOUR_AGENT_ID_HERE \
    --capabilities CAPABILITY_IAM \
    --resolve-s3 \
    --confirm-changeset
```

Replace `YOUR_AGENT_ID_HERE` with your actual Agent ID from step 2.

### 5. Get API Key

After deployment, get the API key value:

```bash
# Get API Key ID from CloudFormation output
API_KEY_ID=$(aws cloudformation describe-stacks \
    --stack-name agentcore-api-gateway-integration \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiKeyId`].OutputValue' \
    --output text)

# Get API Key value
API_KEY_VALUE=$(aws apigateway get-api-key \
    --api-key $API_KEY_ID \
    --include-value \
    --query 'value' \
    --output text)

echo "API Key: $API_KEY_VALUE"
```

### 6. Get API Gateway URL

```bash
API_URL=$(aws cloudformation describe-stacks \
    --stack-name agentcore-api-gateway-integration \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
    --output text)

echo "API URL: $API_URL"
```

## Testing the API

### Test the API

```bash
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"prompt": {"a": 5, "b": 3}}'
```

### Expected Response

```json
{
  "success": true,
  "data": {
    "result": 8,
    "dynamodb_stored": true,
    "item_id": "uuid-here",
    "timestamp": "2025-11-18T12:48:00.000Z"
  },
  "request_id": "lambda-request-id"
}
```

## Key Features

- **Real AgentCore Integration**: Uses `bedrock-agentcore:InvokeAgentRuntime`
- **Dynamic ARN Construction**: Gets AWS Account ID automatically
- **Streaming Response Handling**: Processes AgentCore's streaming responses
- **Error Handling**: Comprehensive validation and error responses
- **CORS Support**: Enabled for web applications

## Cleanup

```bash
aws cloudformation delete-stack --stack-name agentcore-api-gateway-integration
```

## Files

- `template.yaml`: SAM template with API Gateway and Lambda
- `lambda_proxy.py`: Lambda function that proxies to AgentCore
- `test_api.py`: Test script for API validation
- `requirements.txt`: Python dependencies (boto3 >= 1.40.75)

## Technical Implementation

**AgentCore Integration:**
- Service: `bedrock-agentcore`
- Method: `invoke_agent_runtime`
- ARN: `arn:aws:bedrock-agentcore:region:account:runtime/{agent_id}`
- Permissions: `bedrock-agentcore:InvokeAgentRuntime`

**Lambda Proxy Features:**
- Request validation and parsing
- Dynamic AWS account ID detection
- Streaming response processing
- JSON response formatting
- Comprehensive error handling