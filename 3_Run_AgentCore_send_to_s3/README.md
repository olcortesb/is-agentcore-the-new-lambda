# Step 3: AgentCore with S3 Integration

This experiment demonstrates AgentCore as a serverless compute service that stores calculation results directly in Amazon S3, implementing a simple storage pattern for data persistence and analytics.

## Overview

This implementation extends the mathematical operations by adding S3 integration, demonstrating how AgentCore can store structured data for analytics and long-term persistence.

## Files

- `my_agent.py` - Agent implementation with S3 integration
- `requirements.txt` - Python dependencies
- `setup.sh` - Environment setup script
- `s3-policy.example.json` - IAM policy template for S3 permissions
- `.env.example` - Environment variables template
- `README.md` - This documentation

## Prerequisites

Install AgentCore CLI:
```bash
pip install "bedrock-agentcore-starter-toolkit>=0.1.21" boto3
```

## Setup

### 1. Create S3 Bucket
```bash
aws s3 mb s3://agentcore-results-is-agentcore-new-lambda --region us-west-2
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

### 4. Setup IAM Permissions

Create IAM policy file and attach to AgentCore execution role:

```bash
# Copy example policy and edit with your account ID
cp s3-policy.example.json s3-policy.json
# Edit s3-policy.json and replace YOUR_ACCOUNT_ID with your actual account ID

# Create IAM policy for S3 permissions
aws iam create-policy \
  --policy-name AgentCoreS3Policy \
  --policy-document file://s3-policy.json

# Attach policy to AgentCore execution role
aws iam attach-role-policy \
  --role-name AmazonBedrockAgentCoreSDKRuntime-us-west-2-XXXXXXXXXX \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/AgentCoreS3Policy
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

## Expected Response

```json
{
  "result": 8,
  "s3_stored": true,
  "s3_key": "agentcore-results/2025/01/17/uuid-here.json",
  "request_id": "uuid-here"
}
```

## Data Storage Format

### S3 Object Content
```json
{
  "operation": "sum",
  "input": {"a": 5, "b": 3},
  "result": 8,
  "timestamp": "2025-01-17T10:30:00.000Z",
  "source": "agentcore",
  "request_id": "uuid-here"
}
```

### S3 Storage Structure
```
agentcore-results-is-agentcore-new-lambda/
├── agentcore-results/
│   ├── 2025/
│   │   ├── 01/
│   │   │   ├── 17/
│   │   │   │   ├── uuid1.json
│   │   │   │   ├── uuid2.json
│   │   │   │   └── ...
```

## Verification

### Check SQS Messages
```bash
aws sqs receive-message \
  --queue-url https://sqs.us-west-2.amazonaws.com/YOUR_ACCOUNT_ID/agentcore-results \
  --region us-west-2
```

### Check S3 Objects
```bash
aws s3 ls s3://agentcore-results-is-agentcore-new-lambda/agentcore-results/ --recursive
```

### Download S3 Object
```bash
aws s3 cp s3://agentcore-results-is-agentcore-new-lambda/agentcore-results/2025/01/17/uuid.json ./
```

## Architecture Benefits

### Dual Storage Pattern
- **SQS:** Immediate processing and event-driven workflows
- **S3:** Long-term storage, analytics, and compliance
- **Redundancy:** Data available in multiple services
- **Flexibility:** Different access patterns for different use cases

### Use Cases
- **Real-time Processing:** SQS triggers Lambda functions for immediate action
- **Batch Analytics:** S3 enables Athena queries and data lake patterns
- **Audit Trail:** S3 provides immutable record keeping
- **Data Recovery:** S3 serves as backup for SQS message processing

## Troubleshooting

### AccessDenied Errors
1. Ensure both SQS and S3 permissions are in the IAM policy
2. Verify the policy is attached to the AgentCore execution role
3. Check that both SQS queue and S3 bucket exist

### Environment Variables Not Found
1. Verify both `SQS_QUEUE_URL` and `S3_BUCKET_NAME` are set
2. Check the Dockerfile includes both environment variables
3. Redeploy with `agentcore deploy`

### Partial Failures
The agent handles partial failures gracefully:
- If SQS fails but S3 succeeds: Returns result with SQS error
- If S3 fails but SQS succeeds: Returns result with S3 error
- If both fail: Returns result with both errors

## Notes

- Uses ARM64 container architecture
- Implements graceful error handling for both services
- Returns operation result regardless of storage status
- Uses date-based partitioning in S3 for efficient querying
- Generates unique request IDs for tracking across services

## References

- [AWS Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)
- [Amazon SQS Developer Guide](https://docs.aws.amazon.com/sqs/latest/dg/welcome.html)
- [Amazon S3 Developer Guide](https://docs.aws.amazon.com/s3/latest/userguide/Welcome.html)