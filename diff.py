from utils.validators import is_command_safe, is_path_allowed
import subprocess

def run(params):
    repo_path = params.get("repo_path")
    if not repo_path:
        return {"error": "Missing 'repo_path' parameter."}

    try:
        result = subprocess.run(
            ["git", "diff"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        
        return {"diff": result.stdout.strip()}

    except Exception as e:
        return {"error": str(e)}

def run(params):
    repo_path = params.get("repo_path")
    if not repo_path:
        return {"error": "Missing 'repo_path' parameter."}

    if not is_path_allowed(repo_path):
        return {"error": "Operation blocked: Repo path is not allowed."}
    
    if not is_command_safe("git diff"):
        return {"error": "Operation blocked: 'git diff' is not allowed in safe mode."}

    try:
        result = subprocess.run(
            ["git", "diff"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"diff": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}
