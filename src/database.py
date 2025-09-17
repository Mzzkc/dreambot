import os
import json
import base64
from github import Github

class GitHubDatabase:
    """Use a private GitHub repo as free permanent storage"""
    
    def __init__(self):
        token = os.getenv('GITHUB_TOKEN')
        repo_name = os.getenv('GITHUB_REPO', 'discord-bot-data')
        
        if token:
            self.g = Github(token)
            self.user = self.g.get_user()
            
            # Create private repo if it doesn't exist
            try:
                self.repo = self.user.get_repo(repo_name)
            except:
                self.repo = self.user.create_repo(
                    repo_name, 
                    private=True,
                    description="Discord bot data storage"
                )
                # Initialize with empty files
                self.repo.create_file(
                    "reaction_roles.json", 
                    "Initialize", 
                    "{}", 
                    branch="main"
                )
                self.repo.create_file(
                    "warnings.json", 
                    "Initialize", 
                    "{}", 
                    branch="main"
                )
        else:
            print("WARNING: No GitHub token, using local JSON files")
            self.repo = None
    
    def _read_file(self, filename):
        """Read JSON file from GitHub"""
        if not self.repo:
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except:
                return {}
        
        try:
            file = self.repo.get_contents(filename)
            content = base64.b64decode(file.content).decode()
            return json.loads(content)
        except:
            return {}
    
    def _write_file(self, filename, data):
        """Write JSON file to GitHub"""
        if not self.repo:
            with open(filename, 'w') as f:
                json.dump(data, f)
            return
        
        try:
            # Try to get existing file
            try:
                file = self.repo.get_contents(filename)
                self.repo.update_file(
                    filename,
                    f"Update {filename}",
                    json.dumps(data, indent=2),
                    file.sha,
                    branch="main"
                )
            except:
                # Create new file
                self.repo.create_file(
                    filename,
                    f"Create {filename}",
                    json.dumps(data, indent=2),
                    branch="main"
                )
        except Exception as e:
            print(f"GitHub write error: {e}")
            # Fallback to local
            with open(filename, 'w') as f:
                json.dump(data, f)
    
    def load_reaction_roles(self):
        return self._read_file("reaction_roles.json")
    
    def save_reaction_roles(self, data):
        self._write_file("reaction_roles.json", data)
    
    def load_warnings(self):
        return self._read_file("warnings.json")
    
    def save_warnings(self, data):
        self._write_file("warnings.json", data)

# Create instance
db = GitHubDatabase()

# Export functions
def load_reaction_roles():
    return db.load_reaction_roles()

def save_reaction_roles(data):
    db.save_reaction_roles(data)

def load_warnings():
    return db.load_warnings()

def save_warnings(data):
    db.save_warnings(data)