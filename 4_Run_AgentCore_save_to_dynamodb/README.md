# Step 4: AgentCore with DynamoDB Integration

This experiment demonstrates AgentCore as a serverless compute service that stores calculation results in Amazon DynamoDB, implementing a NoSQL database pattern for fast queries and structured data storage.

## Overview

This implementation extends the mathematical operations by adding DynamoDB integration, demonstrating how AgentCore can store structured data in a NoSQL database for real-time queries and analytics.

## Files

- `my_agent.py` - Agent implementation with DynamoDB integration
- `requirements.txt` - Python dependencies
- `setup.sh` - Environment setup script
- `dynamodb-policy.example.json` - IAM policy template for DynamoDB permissions
- `.env.example` - Environment variables template
- `README.md` - This documentation

## Prerequisites

Install AgentCore CLI:
```bash
pip install "bedrock-agentcore-starter-toolkit>=0.1.21" boto3
```

## Setup

### 1. Create DynamoDB Table
```bash
aws dynamodb create-table \
  --table-name agentcore-calculations \
  --attribute-definitions \
    AttributeName=id,AttributeType=S \
  --key-schema \
    AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --time-to-live-specification \
    AttributeName=ttl,Enabled=true \
  --region us-west-2
```

### 2. Install Dependencies
```bash
./setup.sh
```

### 3. Configure Environment Variables
```bash
# Copy the example file and edit with your values
cp .env.example .env
```

### 4. Setup IAM Permissions

Create IAM policy file and attach to AgentCore execution role:

```bash
# Copy example policy and edit with your account ID
cp dynamodb-policy.example.json dynamodb-policy.json
# Edit dynamodb-policy.json and replace YOUR_ACCOUNT_ID with your actual account ID

# Create IAM policy for DynamoDB permissions
aws iam create-policy \
  --policy-name AgentCoreDynamoDBPolicy \
  --policy-document file://dynamodb-policy.json

# Find the correct AgentCore execution role name
cat .bedrock_agentcore.yaml | grep execution_role

# Attach policy to AgentCore execution role (use the role name from above)
aws iam attach-role-policy \
  --role-name AmazonBedrockAgentCoreSDKRuntime-us-west-2-XXXXXXXXXX \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/AgentCoreDynamoDBPolicy
```

**Note:** Replace `XXXXXXXXXX` with your actual role suffix from the grep command and `YOUR_ACCOUNT_ID` with your AWS account ID.

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
  "dynamodb_stored": true,
  "item_id": "uuid-here",
  "timestamp": "2025-11-18T10:30:00.000Z"
}
```

## Data Storage Format

### DynamoDB Item Structure
```json
{
  "id": "uuid-here",
  "timestamp": "2025-11-18T10:30:00.000Z",
  "operation": "sum",
  "input_a": 5,
  "input_b": 3,
  "result": 8,
  "source": "agentcore",
  "ttl": 1732345678
}
```

### Table Schema
- **Primary Key:** `id` (String) - Unique identifier for each calculation
- **TTL:** `ttl` (Number) - Automatic cleanup after 30 days
- **Attributes:** All calculation data stored as item attributes

## Verification

### List All Items
```bash
aws dynamodb scan --table-name agentcore-calculations --region us-west-2
```

### Get Specific Item
```bash
aws dynamodb get-item \
  --table-name agentcore-calculations \
  --key '{"id":{"S":"your-uuid-here"}}' \
  --region us-west-2
```

### Query by Timestamp (requires GSI)
```bash
aws dynamodb query \
  --table-name agentcore-calculations \
  --index-name timestamp-index \
  --key-condition-expression "timestamp = :ts" \
  --expression-attribute-values '{":ts":{"S":"2025-11-18T10:30:00.000Z"}}' \
  --region us-west-2
```

## Architecture Benefits

### DynamoDB Advantages
- **Low Latency:** Sub-millisecond response times
- **Scalability:** Automatic scaling without management
- **TTL:** Automatic data cleanup after 30 days
- **Flexible Queries:** By ID, timestamp, or other attributes
- **Cost Effective:** Pay-per-request pricing

### Use Cases
- **Real-time Analytics:** Fast queries for dashboards
- **Audit Trail:** Complete history of calculations
- **Caching:** Store frequently accessed results
- **User Sessions:** Track user calculation history

### Comparison with Previous Steps
- **Step 1:** Pure compute (no persistence)
- **Step 2:** SQS for async processing
- **Step 3:** S3 for file storage and analytics
- **Step 4:** DynamoDB for structured data and fast queries

## Troubleshooting

### AccessDenied Errors
1. Ensure DynamoDB permissions are in the IAM policy
2. Verify the policy is attached to the AgentCore execution role
3. Check that the DynamoDB table exists

### Table Not Found
1. Verify the table was created: `aws dynamodb describe-table --table-name agentcore-calculations`
2. Check the table name in environment variables
3. Ensure you're using the correct AWS region

### Environment Variables Not Found
1. Verify `DYNAMODB_TABLE_NAME` is set in the Dockerfile
2. Redeploy with `agentcore deploy`
3. Check the container logs for environment variables

## Performance Considerations

- **Item Size:** Keep items under 400KB for optimal performance
- **TTL:** Automatic cleanup prevents table growth
- **Indexes:** Consider GSI for timestamp-based queries
- **Batch Operations:** Use batch writes for high-volume scenarios

## Notes

- Uses ARM64 container architecture
- Implements graceful error handling
- Returns operation result regardless of storage status
- Uses TTL for automatic data cleanup (30 days)
- Generates unique UUIDs for each calculation

## References

- [AWS Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/Introduction.html)
- [DynamoDB TTL Documentation](https://docs.aws.amazon.com/dynamodb/latest/developerguide/TTL.html)