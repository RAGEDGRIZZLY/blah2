import subprocess
from utils.validators import is_command_safe, is_path_allowed

def get_log(repo_path, max_count=10):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'--pretty=format:%h - %s', f'--max-count={max_count}'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"status": "error", "message": result.stderr.strip()}

        logs = []
        for line in result.stdout.strip().split('\n'):
            if ' - ' in line:
                commit_hash, message = line.split(' - ', 1)
                logs.append({
                    "commit": commit_hash,
                    "message": message
                })
        return {"status": "success", "commits": logs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run(params):
    repo_path = params.get("repo_path")
    if not repo_path:
        return {"error": "Missing 'repo_path' parameter."}
    
    if not is_path_allowed(repo_path):
        return {"error": "Operation blocked: Repo path is not allowed."}
    
    if not is_command_safe("git log"):
        return {"error": "Operation blocked: 'git log' is not allowed in safe mode."}

    try:
        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"log": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}
