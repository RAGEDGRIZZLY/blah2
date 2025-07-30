import subprocess
import os
from utils.validators import is_command_safe, is_path_allowed

def clone_repository(repo_url: str, destination: str) -> dict:
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)

        result = subprocess.run(
            ["git", "clone", repo_url, destination],
            capture_output=True,
            text=True,
            check=True
        )
        return {"status": "success", "message": result.stdout.strip()}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr.strip()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run(params):
    repo_url = params.get("repo_url")
    destination = params.get("destination")

    if not repo_url or not destination:
        return {"error": "Missing 'repo_url' or 'destination' parameter."}
    
    if not is_path_allowed(destination):
        return {"error": "Operation blocked: Destination path is not allowed."}
    
    if not is_command_safe("git clone"):
        return {"error": "Operation blocked: 'git clone' is not allowed in safe mode."}

    try:
        result = subprocess.run(
            ["git", "clone", repo_url, destination],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"success": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}
