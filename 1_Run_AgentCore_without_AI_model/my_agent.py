from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    prompt_data = payload.get("prompt", {})
    
    # Extract numbers a and b from the prompt
    a = prompt_data.get("a", 0)
    b = prompt_data.get("b", 0)
    
    # Calculate the sum
    result = a + b
    
    return {"result": result}

if __name__ == "__main__":
    app.run()