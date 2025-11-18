# is-agentcore-the-new-lambda ?

An investigation of how AgentCore works and whether it could become the new Lambda.

## Context

The last [AWS Community Day Spain 2025 Zaragoza](https://awscommunity.es/) was on Saturday, November 15, 2025. The keynote was given by [Álvaro Hernández Tortosa](https://www.linkedin.com/in/ahachete/). The title of the talk was *"Now Go Unbuild"*, and it introduced a set of five challenges or out-of-the-box ideas about AWS services. One of these services was AgentCore, and the challenge was: "Is AgentCore the new Lambda?"

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

The deploy was ok and I can run the Agentcore with Amazon Titan Model ✅

![alt text](images/image.png)

### Step 1: Run AgentCore without AI Model

**Folder:** `1_Run_AgentCore_without_AI_model`

This experiment tests AgentCore as a pure compute service without AI models, making it more similar to Lambda.

**Features:**
- AgentCore without AI dependencies
- Simple mathematical operations (addition)
- Payload processing: `{"prompt": {"a":1,"b":2}}` → `{"result": 3}`

The first test passed! I can remove the AI model and run AgentCore as compute processing... ✅

![alt text](images/image-1.png)

### Step 2: Send a Message to SQS

Now things got interesting. I wanted to test if AgentCore could handle one of the most common Lambda patterns: processing data and sending results to SQS for asynchronous processing.

The implementation was straightforward - I extended the mathematical operations from Step 1 to also send the results to an SQS queue. But here's where I learned something important about AgentCore vs Lambda:

**The Challenge:** Environment variables and IAM permissions work differently than Lambda. While Lambda automatically inherits the execution role permissions, AgentCore required explicit IAM policy creation and attachment.

**The Result:** AgentCore can absolutely replicate Lambda + SQS patterns. The payload `{"prompt": {"a":5,"b":3}}` returns `{"result": 8, "message_sent": true, "message_id": "..."}` and the structured message appears in the SQS queue.

The second test passed!, I can send a message to SQS! ✅

![alt text](images/image-2.png)

### Step 3: Save JSON to S3 from AgentCore

After proving AgentCore could handle SQS integration, I wanted to test another common Lambda pattern: storing structured data in S3 for analytics and long-term persistence.

**The Implementation:** I built on the mathematical operations but this time stored the results directly in S3 with a well-structured JSON format and date-based partitioning.

**The Challenge:** Similar to Step 2, I needed to configure S3 permissions explicitly. AgentCore required its own IAM policy for S3 `PutObject` operations.

**The Process:**
1. ✅ Created S3 bucket: `agentcore-results-is-agentcore-new-lambda`
2. ✅ Implemented S3 client integration with date partitioning
3. ✅ Added environment variable `S3_BUCKET_NAME` to Dockerfile
4. ✅ Created and attached IAM policy for S3 permissions
5. 🎉 **Success!** AgentCore now stores structured JSON data in S3

**The Result:** AgentCore successfully stores calculation results in S3. The payload `{"prompt": {"a":1,"b":2}}` returns `{"result": 3, "s3_stored": true, "s3_key": "agentcore-results/2025/11/18/uuid.json", "request_id": "uuid"}` and creates a properly formatted JSON file in S3 with date partitioning.

**Key Insight:** AgentCore can handle data persistence patterns just like Lambda, but with the added benefit of container-based deployment giving you more control over the runtime environment and dependencies.

The third test passed! I can save JSON to S3 from AgentCore! ✅

The invoke to Agentcore:

![alt text](images/image-3.png)

The file in the bucket:

![alt text](images/image-3-1.png)

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
- [Amazon Bedrock AgentCore](https://aws.amazon.com/es/bedrock/agentcore/)
- [How to Deploy an AI Agent with Amazon Bedrock AgentCore](https://www.freecodecamp.org/news/deploy-an-ai-agent-with-amazon-bedrock/) 