import requests
import json
import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test():
    return {"msg": "CLI is working"}

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MCP_SERVER_URL = "http://localhost:8000"

def query_llm(natural_text: str):
    prompt = f"""
You are an assistant that translates natural language Git instructions into a strict JSON format.

The JSON must have the structure:

{{"tool": "<tool_name>", "params": {{ ... }} }}

Where <tool_name> is exactly one of: clone, branch, commit, diff, list_branches, log, merge, pull, push.

Tool-specific rules:
- clone → tool: "clone", params: "url" and "destination"
- branch → tool: "branch", params: "repo_path" and "branch_name"
- commit → tool: "commit", params: "repo_path" and "message"
- pull → tool: "pull", params: "repo_path"
- push → tool: "push", params: "repo_path"
- merge → tool: "merge", params: "repo_path" and "source_branch" and "target_branch"
- log → tool: "log", params: "repo_path"
- diff → tool: "diff", params: "repo_path"
- list_branches → tool: "list_branches", params: "repo_path"

Respond with a valid JSON. No explanations. No markdown.

Here is the request:

{natural_text}
"""


    response = requests.post(OLLAMA_API_URL, json={
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    })

    llm_text = response.json().get("response", "").strip()

    # Remove markdown code fences if any
    if llm_text.startswith("```"):
        lines = llm_text.splitlines()
        if len(lines) > 2:
            llm_text = "\n".join(lines[1:-1]).strip()

    return llm_text

def perform_git_operation(tool: str, params: dict):
    # Fix endpoint name difference for branch
    endpoint = "create-branch" if tool == "branch" else tool

    url = f"{MCP_SERVER_URL}/{endpoint}"

    # POST method for these tools, else GET
    post_tools = {"clone", "commit", "push", "pull", "merge", "branch", "diff", "create-branch"}
    try:
        if tool in post_tools:
            response = requests.post(url, json=params)
        else:
            response = requests.get(url, params=params)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to perform Git operation: {str(e)}"}

def main():
    print("Welcome to MCP Git CLI powered by LLM!")
    print("Type your Git command in plain English. Type 'exit' to quit.")

    while True:
        user_input = input("\nEnter Git command: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        llm_response = query_llm(user_input)

        try:
            parsed = json.loads(llm_response)
            tool = parsed["tool"]
            params = parsed["params"]
        except Exception as e:
            print(f"Failed to parse LLM response:\n{llm_response}")
            continue

        print(f"Detected tool: {tool}")
        print(f"Parameters: {params}")

        # Optional repo_path existence check before sending request
        if "repo_path" in params and not os.path.exists(params["repo_path"]):
            print(f"Error: repo_path does not exist: {params['repo_path']}")
            continue

        result = perform_git_operation(tool, params)
        print("Operation result:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
