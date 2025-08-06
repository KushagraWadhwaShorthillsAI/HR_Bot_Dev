#!/usr/bin/env python3
"""

azure_config = {
    "api_key": "",
    "api_version": "2024-08-01-preview",
    "endpoint": "https://us-tax-law-rag-demo.openai.azure.com/",
    "deployment": "gpt-4o-mini"
}
"""
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load .env file from current directory
load_dotenv()

azure_config = {
            "api_key": "",
            "api_version": "2024-08-01-preview",
            "endpoint":"https://us-tax-law-rag-demo.openai.azure.com/",
            "deployment": "gpt-4o-mini"
        }

try:
    client = AzureOpenAI(
        api_key=azure_config["api_key"],
        api_version=azure_config["api_version"],
        azure_endpoint=azure_config["endpoint"]
    )
    deployment_name = azure_config["deployment"]
    print(f"Testing Azure OpenAI connection with deployment: {deployment_name}")
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ],
        temperature=0.1,
        response_format={"type": "text"}
    )
    print("Connection successful! Response:")
    print(response.choices[0].message.content.strip())
except Exception as e:
    print(f"Connection failed: {e}")
    print("Check your endpoint, API key, and deployment name.")
