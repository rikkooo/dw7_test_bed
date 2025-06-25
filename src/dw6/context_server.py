# src/dw6/context_server.py

import uvicorn
from fastapi import FastAPI, HTTPException
from pathlib import Path
import git

from dw6.state_manager import WorkflowManager

app = FastAPI()

def get_project_root() -> Path:
    """Finds the project root by looking for the .git directory."""
    try:
        repo = git.Repo(Path.cwd(), search_parent_directories=True)
        return Path(repo.working_tree_dir)
    except git.InvalidGitRepositoryError:
        # Fallback to CWD if not in a git repo, though most features will fail.
        return Path.cwd()

PROJECT_ROOT = get_project_root()

@app.get("/context/state")
def get_workflow_state():
    """Returns the current state of the workflow."""
    try:
        manager = WorkflowManager(project_root=PROJECT_ROOT)
        return {
            "CurrentStage": manager.current_stage,
            "RequirementPointer": manager.state.get('RequirementPointer')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/context/git")
def get_git_context():
    """Returns the current Git context of the project."""
    try:
        repo = git.Repo(PROJECT_ROOT)
        latest_commit = repo.head.commit
        return {
            "branch": repo.active_branch.name,
            "latest_commit": latest_commit.hexsha[:7],
            "status": "clean" if not repo.is_dirty() else "dirty"
        }
    except git.InvalidGitRepositoryError:
        raise HTTPException(status_code=404, detail="Not a Git repository.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/context/requirements")
def get_meta_requirements():
    """Returns the meta-requirements for the project."""
    req_file = PROJECT_ROOT / "docs" / "requirements.md"
    if not req_file.exists():
        raise HTTPException(status_code=404, detail="requirements.md not found in docs/ directory.")
    
    try:
        with open(req_file, "r") as f:
            content = f.read()
        # A simple parser could be implemented here if the format is consistent.
        return {"requirements": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read requirements file: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
