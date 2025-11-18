#!/bin/bash

python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

pip install "bedrock-agentcore-starter-toolkit>=0.1.21" strands-agents strands-agents-tools boto3