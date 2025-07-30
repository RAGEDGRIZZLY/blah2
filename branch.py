from git import Repo, GitCommandError

def create_branch(repo_path: str, branch_name: str) -> str:
    try:
        repo = Repo(repo_path)

        # Check if branch already exists
        if branch_name in repo.heads:
            return f"Branch '{branch_name}' already exists."

        # Create new branch
        new_branch = repo.create_head(branch_name)
        return f"Created new branch '{new_branch}'"

    except GitCommandError as e:
        return f"Git error: {str(e)}"
    except Exception as e:
        return f"Failed to create branch: {str(e)}"
