from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

# Use Amazon Titan model (available by default, no approval needed)
titan_model = BedrockModel(model_id="amazon.titan-text-express-v1", region="us-west-2")

# Create an agent with Titan model
agent = Agent(model=titan_model)


@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent(user_message)
    return {"result": result.message}
    # return {"result": payload.get("prompt", result)}


if __name__ == "__main__":
    app.run()