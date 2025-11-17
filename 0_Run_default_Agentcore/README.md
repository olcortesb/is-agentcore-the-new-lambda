# Step 0: Basic AgentCore with Titan Model

This experiment demonstrates a basic implementation of AWS Bedrock AgentCore using the Amazon Titan text model.

## Overview

This folder contains the foundational setup for AgentCore with AI capabilities, serving as a baseline for comparison with Lambda-like implementations.

## Files

- `my_agent.py` - Main agent implementation with Titan model integration
- `requirements.txt` - Python dependencies
- `setup.sh` - Environment setup script
- `.bedrock_agentcore.yaml` - AgentCore configuration
- `Dockerfile` - Container configuration

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
agentcore invoke '{"prompt": "Hello"}'
```

## Deployment Details

- **Agent Name:** basic_titan_agentcore
- **Agent ARN:** arn:aws:bedrock-agentcore:us-west-2:YOUR_ACCOUNT_ID:runtime/basic_titan_agentcore-XXXXX
- **ECR URI:** YOUR_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-basic_titan_agentcore:latest

## Monitoring

### CloudWatch Logs
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/basic_titan_agentcore-XXXXX-DEFAULT --log-stream-name-prefix "YYYY/MM/DD/[runtime-logs]" --follow
```

### GenAI Observability Dashboard
[CloudWatch GenAI Dashboard](https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core)

## Notes

- Uses ARM64 container architecture
- Observability data may take up to 10 minutes to appear after first launch
- Includes OpenTelemetry runtime logs

## References

- [AWS Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)