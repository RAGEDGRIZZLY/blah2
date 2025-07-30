from git import Repo, GitCommandError
import os
import subprocess
from utils.validators import is_command_safe, is_path_allowed

def commit_changes(repo_path: str, message: str) -> dict:
    try:
        if not os.path.exists(repo_path):
            return {"status": "error", "message": f"Repository path does not exist: {repo_path}"}

        repo = Repo(repo_path)

        # Check if repo is dirty before committing
        if not repo.is_dirty(untracked_files=True):
            return {"status": "info", "message": "No changes to commit."}

        repo.git.add(A=True)
        repo.index.commit(message)
        return {"status": "success", "message": f"Committed changes with message: '{message}'"}

    except GitCommandError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

def run(params):
    repo_path = params.get("repo_path")
    message = params.get("message")

    if not repo_path or not message:
        return {"error": "Missing 'repo_path' or 'message' parameter."}

    if not is_path_allowed(repo_path):
        return {"error": "Operation blocked: Repo path is not allowed."}

    if not is_command_safe("git commit"):
        return {"error": "Operation blocked: 'git commit' is not allowed in safe mode."}

    try:
        subprocess.run(["git", "add", "."], cwd=repo_path)
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"success": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}        
