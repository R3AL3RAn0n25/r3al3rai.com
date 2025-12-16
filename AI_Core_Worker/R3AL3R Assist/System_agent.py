# AI_Core_Worker/system_agent.py
import os
import subprocess
import shutil
from pathlib import Path

class SystemAgent:
    def __init__(self):
        self.workspace = Path.cwd()

    def list_files(self, path: str = ".") -> str:
        try:
            items = os.listdir(Path(path))
            return f"Found {len(items)} items: {', '.join(items[:20])}{('...' if len(items)>20 else '')}"
        except Exception as e:
            return f"Access error: {e}"

    def read_file(self, filepath: str) -> str:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return f"--- {filepath} ---\n{content[:3000]}{'...' if len(content)>3000 else ''}"
        except Exception as e:
            return f"Cannot read {filepath}: {e}"

    def write_file(self, filepath: str, content: str) -> str:
        try:
            Path(filepath).write_text(content, encoding="utf-8")
            return f"Successfully wrote {filepath}"
        except Exception as e:
            return f"Write failed: {e}"

    def git_status(self) -> str:
        try:
            return subprocess.check_output(["git", "status", "--short"], cwd=self.workspace, text=True)
        except:
            return "Not a git repo or git not installed"

    def git_commit(self, message: str = "Auto-commit by R3AL3RAI") -> str:
        try:
            subprocess.run(["git", "add", "."], cwd=self.workspace, check=True)
            subprocess.run(["git", "commit", "-m", message], cwd=self.workspace, check=True)
            return "Committed everything"
        except Exception as e:
            return f"Commit failed: {e}"

    def execute_shell(self, cmd: str) -> str:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.workspace)
            output = result.stdout + result.stderr
            return output[:2000]
        except Exception as e:
            return str(e)