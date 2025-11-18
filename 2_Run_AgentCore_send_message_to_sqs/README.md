# Step 2: AgentCore with SQS Integration

This experiment intends to demonstrate AgentCore as a serverless compute service that sends results to Amazon SQS, replicating a common Lambda + SQS pattern.

## Overview

This implementation extends the mathematical operations from Step 1 by adding SQS integration, demonstrating how AgentCore can handle asynchronous processing patterns similar to AWS Lambda.

## Files

- `my_agent.py` - Agent implementation with SQS integration
- `requirements.txt` - Python dependencies
- `setup.sh` - Environment setup script
- `sqs-policy.example.json` - IAM policy template for SQS permissions
- `.env.example` - Environment variables template
- `README.md` - This documentation

## Prerequisites

Install AgentCore CLI:
```bash
pip install "bedrock-agentcore-starter-toolkit>=0.1.21" boto3
```

## Setup

### 1. Create SQS Queue
```bash
aws sqs create-queue --queue-name agentcore-results --region us-west-2
```

### 2. Install Dependencies
```bash
./setup.sh
```

### 3. Configure Environment Variables
```bash
# Copy the example file and edit with your values
cp .env.example .env
# Edit .env file with your AWS account ID
```

Or set directly:
```bash
export SQS_QUEUE_URL="https://sqs.us-west-2.amazonaws.com/YOUR_ACCOUNT_ID/agentcore-results"
```

### 4. Setup IAM Permissions

Create IAM policy file and attach to AgentCore execution role:

```bash
# Copy example policy and edit with your account ID
cp sqs-policy.example.json sqs-policy.json
# Edit sqs-policy.json and replace YOUR_ACCOUNT_ID with your actual account ID

# Create IAM policy for SQS permissions
aws iam create-policy \
  --policy-name AgentCoreSQSPolicy \
  --policy-document file://sqs-policy.json

# Attach policy to AgentCore execution role
aws iam attach-role-policy \
  --role-name AmazonBedrockAgentCoreSDKRuntime-us-west-2-XXXXXXXXXX \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/AgentCoreSQSPolicy
```

**Note:** Replace `XXXXXXXXXX` with your actual role suffix and `YOUR_ACCOUNT_ID` with your AWS account ID.

## Configure

```bash
agentcore configure -e my_agent.py
```

## Deploy

```bash
agentcore deploy
```

## Test

```bash
agentcore invoke '{"prompt": {"a": 5, "b": 3}}'
```

## Verify SQS Message

Check that the message was sent to SQS:

```bash
aws sqs receive-message \
  --queue-url https://sqs.us-west-2.amazonaws.com/YOUR_ACCOUNT_ID/agentcore-results \
  --region us-west-2
```

## Expected Response

```json
{
  "result": 8,
  "message_sent": true,
  "message_id": "12345678-1234-1234-1234-123456789012"
}
```

## SQS Message Format

The agent sends messages to SQS with the following structure:

```json
{
  "operation": "sum",
  "input": {"a": 5, "b": 3},
  "result": 8,
  "timestamp": "2025-01-17T10:30:00.000Z",
  "source": "agentcore"
}
```

## IAM Permissions Required

The AgentCore execution role needs the following SQS permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:SendMessage"
      ],
      "Resource": "arn:aws:sqs:us-west-2:YOUR_ACCOUNT_ID:agentcore-results"
    }
  ]
}
```

## Monitoring

### Check SQS Messages
```bash
aws sqs receive-message --queue-url https://sqs.us-west-2.amazonaws.com/YOUR_ACCOUNT_ID/agentcore-results --region us-west-2
```

### CloudWatch Logs
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/AGENT_NAME-XXXXX-DEFAULT --log-stream-name-prefix "YYYY/MM/DD/[runtime-logs]" --follow
```

## Key Differences from Lambda

- **Deployment:** Container-based vs ZIP/Layer-based
- **Permissions:** AgentCore execution role vs Lambda execution role
- **Environment Variables:** Set via AgentCore configuration
- **Monitoring:** GenAI observability + standard CloudWatch

## Use Cases

- **Asynchronous Processing:** Send results for further processing
- **Audit Trail:** Log all mathematical operations
- **Fan-out Pattern:** One calculation → multiple consumers
- **Event-driven Architecture:** Trigger downstream processes

## Troubleshooting

### AccessDenied Error
If you get an `AccessDenied` error when sending to SQS:
1. Ensure the IAM policy is created: `aws iam get-policy --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/AgentCoreSQSPolicy`
2. Verify the policy is attached to the role: `aws iam list-attached-role-policies --role-name AmazonBedrockAgentCoreSDKRuntime-us-west-2-XXXXXXXXXX`
3. Check the queue exists: `aws sqs get-queue-attributes --queue-url YOUR_QUEUE_URL`

### Environment Variable Not Found
If you get `SQS_QUEUE_URL environment variable is required`:
1. Verify the variable is set in the Dockerfile
2. Redeploy with `agentcore deploy`
3. Check the container logs for environment variables

## Notes

- Uses ARM64 container architecture
- Handles SQS send failures gracefully
- Returns operation result regardless of SQS status
- Environment variable is set directly in Dockerfile for simplicity
- IAM permissions are required for SQS access

## References

- [AWS Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)
- [Amazon SQS Developer Guide](https://docs.aws.amazon.com/sqs/latest/dg/welcome.html)