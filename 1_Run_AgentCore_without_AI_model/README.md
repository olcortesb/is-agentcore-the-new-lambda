# Step 1: AgentCore without AI Model

This experiment demonstrates AgentCore as a pure compute service, similar to AWS Lambda, without AI model dependencies.

## Overview

This implementation removes AI model dependencies and focuses on AgentCore as a serverless compute platform, processing mathematical operations instead of AI inference.

## Files

- `my_agent.py` - Agent implementation for mathematical operations
- `requirements.txt` - Minimal Python dependencies
- `setup.sh` - Environment setup script
- `.bedrock_agentcore.yaml` - AgentCore configuration
- `Dockerfile` - Container configuration

## Functionality

The agent receives a payload with two numbers and returns their sum:

**Input:**
```json
{"prompt": {"a": 1, "b": 2}}
```

**Output:**
```json
{"result": 3}
```

## Prerequisites

Install AgentCore CLI:
```bash
pip install "bedrock-agentcore-starter-toolkit>=0.1.21" strands-agents strands-agents-tools boto3
```

## Setup

```bash
./setup.sh
```

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

## Deployment Details

- **Agent Name:** agentcore_without_ai_model
- **Agent ARN:** arn:aws:bedrock-agentcore:us-west-2:YOUR_ACCOUNT_ID:runtime/agentcore_without_ai_model-XXXXX
- **ECR URI:** YOUR_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-agentcore_without_ai_model:latest

## Monitoring

### CloudWatch Logs
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/agentcore_without_ai_model-XXXXX-DEFAULT --log-stream-name-prefix "YYYY/MM/DD/[runtime-logs]" --follow
```

### GenAI Observability Dashboard
[CloudWatch GenAI Dashboard](https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core)

## Key Differences from Lambda

- **Deployment:** Container-based vs ZIP/Layer-based
- **Runtime:** AgentCore runtime vs Lambda runtime
- **Monitoring:** GenAI observability vs standard Lambda metrics
- **Scaling:** AgentCore scaling vs Lambda concurrency model

## Notes

- Uses ARM64 container architecture
- No AI model dependencies
- Demonstrates AgentCore as a general-purpose compute service
- Observability data may take up to 10 minutes to appear

## References

- [AWS Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)