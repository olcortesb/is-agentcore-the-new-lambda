# is-agentcore-the-new-lambda ?

An investigation of how AgentCore works and whether it could become the new Lambda.

## Context

The last [AWS Community Day Spain 2025 Zaragoza](https://awscommunity.es/) was on Saturday, November 15, 2025. The keynote was given by [Álvaro Hernández Tortosa](https://www.linkedin.com/in/ahachete/). The title of the talk was "Now Go Unbuild", and it introduced a set of five challenges or out-of-the-box ideas about AWS services. One of these services was AgentCore, and the challenge was: "Is AgentCore the new Lambda?"

## Hands On

I basically accepted this challenge, and in this repository I want to test the possibility of running AgentCore as the new version of Lambda. Why? Because it seems the best way to learn — what works, what doesn't, and why.

## What is AgentCore?

Amazon Bedrock AgentCore is an AWS service that provides the foundation for building, deploying, and operating AI agents at scale (similar to AWS Lambda but with AI). It offers the necessary infrastructure for handling agent workloads, including:

- Serverless runtime
- Memory management for short and long-term context
- Tool integration via AgentCore Gateway
- Secure authentication

## Experiments

### Step 0: Run AWS Bedrock AgentCore with AI Model

**Folder:** `0_Run_default_Agentcore`

This folder contains a basic implementation of AgentCore with Titan model. I deploy a simple AgentCore and test the deployment process.

**Features:**
- Basic AgentCore setup
- Integration with Amazon Titan model
- Deployment testing

The deploy was ok and I can run the Agentcore with Amazon Titan Model

![alt text](images/image.png)

### Step 1: Run AgentCore without AI Model

**Folder:** `1_Run_AgentCore_without_AI_model`

This experiment tests AgentCore as a pure compute service without AI models, making it more similar to Lambda.

**Features:**
- AgentCore without AI dependencies
- Simple mathematical operations (addition)
- Payload processing: `{"prompt": {"a":1,"b":2}}` → `{"result": 3}`

 The first test passed , I can remove the AI model and run Agentcore as compute processing ... 

![alt text](images/image-1.png)

## Getting Started

1. Install AgentCore CLI:
   ```bash
   pip install "bedrock-agentcore-starter-toolkit>=0.1.21" strands-agents strands-agents-tools boto3
   ```
2. Navigate to the desired experiment folder
3. Run `./setup.sh` to install dependencies
4. Configure AgentCore: `agentcore configure -e my_agent.py`
5. Deploy using `agentcore deploy`
6. Test with `agentcore invoke`

## Requirements

- Python 3.10+
- AWS CLI configured
- Bedrock AgentCore CLI
- Docker (for deployment)

## References

- [AWS Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)