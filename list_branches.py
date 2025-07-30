from git import Repo
import os
import subprocess
from utils.validators import is_command_safe, is_path_allowed

def list_branches(repo_path: str) -> dict:
    if not os.path.exists(repo_path):
        return {"error": f"Repository path does not exist: {repo_path}"}
    
    try:
        repo = Repo(repo_path)
        branches = [head.name for head in repo.heads]
        return {"branches": branches}
    except Exception as e:
        return {"error": str(e)}

def run(params):
    repo_path = params.get("repo_path")
    if not repo_path:
        return {"error": "Missing 'repo_path' parameter."}
    
    if not is_path_allowed(repo_path):
        return {"error": "Operation blocked: Repo path is not allowed."}
    
    if not is_command_safe("git branch"):
        return {"error": "Operation blocked: 'git branch' is not allowed in safe mode."}

    try:
        result = subprocess.run(
            ["git", "branch"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"branches": result.stdout.strip().split('\n')}
    except Exception as e:
        return {"error": str(e)}
