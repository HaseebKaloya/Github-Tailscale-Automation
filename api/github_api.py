"""
GitHub API Integration for Github&Tailscale-Automation
Author: Haseeb Kaloya
Email: haseebkaloya@gmail.com

Handles all GitHub API operations including repository creation,
file uploads, secrets management, and workflow triggers.
"""

import base64
import requests
import time
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List
from github import Github, GithubException, Repository
from nacl import encoding, public
from utils.logger import get_logger
from core.constants import API_RATE_LIMIT_DELAY

class GitHubAPI:
    """GitHub API wrapper for repository automation"""
    
    def __init__(self, token: str, username: str):
        """
        Initialize GitHub API wrapper
        
        Args:
            token: GitHub personal access token
            username: GitHub username (may be overridden by actual authenticated user)
        """
        self.token = token
        self.client = Github(token)
        self.user = self.client.get_user()
        # Use the actual authenticated user's login instead of configured username
        # This prevents "Not Found" errors when repositories are created under different username
        self.username = self.user.login
        self.logger = get_logger()
        
        if username != self.username:
            self.logger.warning(f"Configured username '{username}' differs from authenticated user '{self.username}'. Using authenticated user.")
        
        # Verify authentication
        try:
            self.user.login
            self.logger.info(f"GitHub API authenticated as: {self.user.login}")
        except Exception as e:
            self.logger.error(f"GitHub authentication failed: {e}")
            raise
    
    def create_repository(self, 
                         name: str,
                         description: str = "",
                         private: bool = True,
                         auto_init: bool = True,
                         has_issues: bool = True,
                         has_wiki: bool = False,
                         has_projects: bool = False) -> Tuple[bool, Any]:
        """
        Create a GitHub repository with customizable settings
        
        Args:
            name: Repository name
            description: Repository description
            private: Create as private repository
            auto_init: Initialize with README
            has_issues: Enable Issues
            has_wiki: Enable Wiki
            has_projects: Enable Projects
            
        Returns:
            Tuple[bool, Any]: (success, repository_object or error_message)
        """
        try:
            self.logger.info(f"Creating repository: {name} (Issues: {has_issues}, Wiki: {has_wiki}, Projects: {has_projects})")
            
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init,
                has_issues=has_issues,
                has_wiki=has_wiki,
                has_projects=has_projects
            )
            
            self.logger.info(f"Repository created successfully: {name}")
            time.sleep(API_RATE_LIMIT_DELAY)
            return True, repo
            
        except GithubException as e:
            error_msg = f"Failed to create repository {name}: {e.data.get('message', str(e))}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error creating repository {name}: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def upload_file(self,
                   repo_name: str,
                   file_path: str,
                   target_path: str,
                   commit_message: str = "Add file via automation") -> Tuple[bool, str]:
        """
        Upload a file to repository
        
        Args:
            repo_name: Repository name
            file_path: Local file path
            target_path: Target path in repository
            commit_message: Commit message
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            self.logger.info(f"Uploading file to {repo_name}: {target_path}")
            
            repo = self.user.get_repo(repo_name)
            
            # Check file size (GitHub limit is 100MB, but we'll use 50MB to be safe)
            file_size = Path(file_path).stat().st_size
            max_size = 50 * 1024 * 1024  # 50 MB
            
            if file_size > max_size:
                return False, f"File too large ({file_size / 1024 / 1024:.1f}MB). Maximum allowed: 50MB"
            
            # Read file content
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return False, f"File not found: {file_path}"
            
            with open(file_path_obj, 'rb') as f:
                content = f.read()
            
            # Upload file
            repo.create_file(
                path=target_path,
                message=commit_message,
                content=content,
                branch="main"
            )
            
            self.logger.info(f"File uploaded successfully: {target_path}")
            time.sleep(API_RATE_LIMIT_DELAY)
            return True, ""
            
        except GithubException as e:
            error_msg = f"Failed to upload file: {e.data.get('message', str(e))}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error uploading file: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def upload_folder(self,
                     repo_name: str,
                     folder_path: str,
                     target_folder: str = "",
                     commit_message: str = "Add folder via automation") -> Tuple[bool, str]:
        """
        Upload entire folder to repository
        
        Args:
            repo_name: Repository name
            folder_path: Local folder path
            target_folder: Target folder in repository
            commit_message: Commit message
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            self.logger.info(f"Uploading folder to {repo_name}: {target_folder}")
            
            folder_path_obj = Path(folder_path)
            if not folder_path_obj.exists() or not folder_path_obj.is_dir():
                return False, f"Folder not found: {folder_path}"
            
            # Get all files in folder
            files = list(folder_path_obj.rglob('*'))
            file_count = 0
            
            for file_path in files:
                if file_path.is_file():
                    # Calculate relative path
                    rel_path = file_path.relative_to(folder_path_obj)
                    
                    # Construct target path
                    if target_folder:
                        target_path = f"{target_folder}/{rel_path}".replace('\\', '/')
                    else:
                        target_path = str(rel_path).replace('\\', '/')
                    
                    # Upload file
                    success, error = self.upload_file(
                        repo_name, 
                        str(file_path), 
                        target_path,
                        f"{commit_message} - {rel_path}"
                    )
                    
                    if success:
                        file_count += 1
                    else:
                        self.logger.warning(f"Failed to upload {rel_path}: {error}")
            
            self.logger.info(f"Uploaded {file_count} files from folder")
            return True, ""
            
        except Exception as e:
            error_msg = f"Unexpected error uploading folder: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def add_secret(self,
                  repo_name: str,
                  secret_name: str,
                  secret_value: str) -> Tuple[bool, str]:
        """
        Add a secret to repository (GitHub Actions)
        
        Args:
            repo_name: Repository name
            secret_name: Secret name
            secret_value: Secret value
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            self.logger.info(f"Adding secret to {repo_name}: {secret_name}")
            
            # Get repository with error handling
            try:
                repo = self.user.get_repo(repo_name)
            except Exception as e:
                return False, f"Repository not found or inaccessible: {str(e)}"
            
            # Get repository public key for encryption
            try:
                public_key = repo.get_public_key()
            except Exception as e:
                return False, f"Cannot access repository secrets (check repository permissions): {str(e)}"
            
            # Validate secret name format
            import re
            if not re.match(r'^[A-Z0-9_]+$', secret_name):
                return False, f"Invalid secret name format: {secret_name}. Must contain only uppercase letters, numbers, and underscores."
            
            # Encrypt the secret
            try:
                encrypted = self._encrypt_secret(public_key.key, secret_value)
            except Exception as e:
                return False, f"Failed to encrypt secret: {str(e)}"
            
            # Create or update secret via REST API
            url = f"https://api.github.com/repos/{self.username}/{repo_name}/actions/secrets/{secret_name}"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "encrypted_value": encrypted,
                "key_id": public_key.key_id
            }
            
            # Log the API call for debugging
            self.logger.debug(f"Secrets API URL: {url}")
            self.logger.debug(f"Request data: key_id={public_key.key_id}, encrypted_value_length={len(encrypted)}")
            
            response = requests.put(url, json=data, headers=headers)
            
            if response.status_code in [201, 204]:
                self.logger.info(f"Secret added successfully: {secret_name}")
                time.sleep(API_RATE_LIMIT_DELAY)
                return True, ""
            else:
                try:
                    error_data = response.json()
                    error_msg = f"Failed to add secret: {error_data.get('message', 'Unknown error')}"
                except:
                    error_msg = f"Failed to add secret (HTTP {response.status_code}): {response.text}"
                
                # Enhanced error logging for debugging
                self.logger.error(f"Secrets API Error - URL: {url}")
                self.logger.error(f"Secrets API Error - Status: {response.status_code}")
                self.logger.error(f"Secrets API Error - Response: {response.text[:500]}")
                self.logger.error(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Unexpected error adding secret: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def start_workflow(self,
                      repo_name: str,
                      workflow_file: str = "main.yml") -> Tuple[bool, str]:
        """
        Trigger a GitHub Actions workflow with proper validation
        
        Args:
            repo_name: Repository name
            workflow_file: Workflow file name (e.g., "main.yml")
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            self.logger.info(f"Starting workflow in {repo_name}: {workflow_file}")
            
            # Ensure workflow_file has correct format for API
            # GitHub API expects just the filename, not the full path
            if workflow_file.startswith('.github/workflows/'):
                workflow_file = workflow_file.replace('.github/workflows/', '')
            
            # First, verify the workflow exists and has workflow_dispatch trigger
            workflows_url = f"https://api.github.com/repos/{self.username}/{repo_name}/actions/workflows"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Log the API call for debugging
            self.logger.debug(f"Workflows API URL: {workflows_url}")
            
            # Get list of workflows with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                workflows_response = requests.get(workflows_url, headers=headers)
                
                if workflows_response.status_code == 200:
                    break
                elif workflows_response.status_code == 404:
                    self.logger.error(f"Workflows API Error - URL: {workflows_url}")
                    self.logger.error(f"Workflows API Error - Status: 404")
                    self.logger.error(f"Repository '{repo_name}' not found under user '{self.username}'")
                    return False, f"Repository {repo_name} not found or no workflows exist"
                elif attempt == max_retries - 1:
                    try:
                        error_data = workflows_response.json()
                        error_msg = f"Failed to list workflows: {error_data.get('message', 'Unknown error')}"
                    except:
                        error_msg = f"Failed to list workflows (HTTP {workflows_response.status_code}): {workflows_response.text}"
                    
                    self.logger.error(f"Workflows API Error - URL: {workflows_url}")
                    self.logger.error(f"Workflows API Error - Status: {workflows_response.status_code}")
                    self.logger.error(f"Workflows API Error - Response: {workflows_response.text[:500]}")
                    self.logger.error(error_msg)
                    return False, error_msg
                else:
                    time.sleep(1)  # Wait before retry
            
            workflows_data = workflows_response.json()
            workflow_found = False
            workflow_id = None
            
            # Find the workflow by filename
            for workflow in workflows_data.get('workflows', []):
                if workflow['path'].endswith(workflow_file):
                    workflow_found = True
                    workflow_id = workflow['id']
                    
                    # Check if workflow has workflow_dispatch event
                    # Note: API doesn't always return this, so we'll try to trigger anyway
                    self.logger.debug(f"Found workflow: {workflow['name']} (ID: {workflow_id})")
                    break
            
            if not workflow_found:
                available_workflows = [w['path'] for w in workflows_data.get('workflows', [])]
                if not available_workflows:
                    error_msg = f"No workflows found in repository '{repo_name}'. Make sure you have uploaded a workflow file to .github/workflows/ folder."
                else:
                    error_msg = f"Workflow file '{workflow_file}' not found in repository. Available workflows: {available_workflows}"
                self.logger.error(error_msg)
                return False, error_msg
            
            # Trigger workflow using workflow ID (more reliable than filename)
            dispatch_url = f"https://api.github.com/repos/{self.username}/{repo_name}/actions/workflows/{workflow_id}/dispatches"
            data = {
                "ref": "main",  # Branch to run workflow on
                "inputs": {}  # Optional workflow inputs
            }
            
            # Retry workflow dispatch with exponential backoff
            max_dispatch_retries = 2
            for attempt in range(max_dispatch_retries):
                response = requests.post(dispatch_url, json=data, headers=headers)
                
                if response.status_code == 204:
                    break
                elif response.status_code == 422 and attempt < max_dispatch_retries - 1:
                    # Repository might not be ready, wait and retry
                    time.sleep(2 ** attempt)
                    continue
                elif attempt == max_dispatch_retries - 1:
                    break  # Exit retry loop, handle error below
            
            if response.status_code == 204:
                self.logger.info(f"[SUCCESS] Workflow '{workflow_file}' started successfully in {repo_name}")
                time.sleep(API_RATE_LIMIT_DELAY)
                return True, ""
            elif response.status_code == 404:
                error_msg = f"Workflow not found or doesn't have 'workflow_dispatch' trigger. Make sure your workflow file includes:\n\non:\n  workflow_dispatch:"
                self.logger.error(error_msg)
                return False, error_msg
            elif response.status_code == 422:
                try:
                    error_data = response.json()
                    if 'workflow_dispatch' in str(error_data).lower():
                        error_msg = f"Workflow doesn't support manual triggering. Add 'workflow_dispatch:' to the 'on:' section of your workflow file."
                    else:
                        error_msg = f"Workflow trigger failed: {error_data.get('message', 'Invalid workflow configuration')}"
                except:
                    error_msg = f"Cannot trigger workflow. Ensure workflow has 'workflow_dispatch' trigger in the 'on:' section"
                self.logger.error(error_msg)
                return False, error_msg
            else:
                try:
                    error_data = response.json()
                    error_msg = f"Failed to start workflow (HTTP {response.status_code}): {error_data.get('message', 'Unknown error')}"
                except:
                    error_msg = f"Failed to start workflow (HTTP {response.status_code}): {response.text}"
                
                self.logger.error(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Unexpected error starting workflow: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return False, error_msg
    
    def _encrypt_secret(self, public_key: str, secret_value: str) -> str:
        """
        Encrypt a secret using repository's public key
        
        Args:
            public_key: Repository public key (base64)
            secret_value: Value to encrypt
            
        Returns:
            str: Encrypted value (base64)
        """
        # Convert key from base64
        public_key_bytes = base64.b64decode(public_key)
        
        # Create public key object
        sealed_box = public.SealedBox(public.PublicKey(public_key_bytes))
        
        # Encrypt the secret
        encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
        
        # Return base64 encoded
        return base64.b64encode(encrypted).decode('utf-8')
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test GitHub API connection
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            user = self.client.get_user()
            username = user.login
            return True, f"Connected as: {username}"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get current rate limit information
        
        Returns:
            Dict: Rate limit information
        """
        try:
            rate_limit = self.client.get_rate_limit()
            return {
                "core": {
                    "remaining": rate_limit.core.remaining,
                    "limit": rate_limit.core.limit,
                    "reset": rate_limit.core.reset
                }
            }
        except Exception:
            return {}
    
    def set_repository_topics(self, repo_name: str, topics: List[str]) -> Tuple[bool, str]:
        """
        Set repository topics
        
        Args:
            repo_name: Repository name
            topics: List of topics to set
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            if not topics:
                return True, ""
            
            self.logger.info(f"Setting topics for {repo_name}: {topics}")
            
            repo = self.user.get_repo(repo_name)
            repo.replace_topics(topics)
            
            self.logger.info(f"Topics set successfully for {repo_name}")
            time.sleep(API_RATE_LIMIT_DELAY)
            return True, ""
            
        except Exception as e:
            error_msg = f"Failed to set topics: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def enable_github_pages(self, repo_name: str, source: str = "main branch /root") -> Tuple[bool, str]:
        """
        Enable GitHub Pages for repository
        
        Args:
            repo_name: Repository name
            source: Pages source (e.g., "main branch /root", "main branch /docs", "gh-pages branch")
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            self.logger.info(f"Enabling GitHub Pages for {repo_name} (source: {source})")
            
            # Parse source
            if "docs" in source:
                branch = "main"
                path = "/docs"
            elif "gh-pages" in source:
                branch = "gh-pages"
                path = "/"
            else:
                branch = "main"
                path = "/"
            
            # Enable Pages via REST API
            url = f"https://api.github.com/repos/{self.username}/{repo_name}/pages"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "source": {
                    "branch": branch,
                    "path": path
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code in [201, 200, 409]:  # 409 = already enabled
                self.logger.info(f"GitHub Pages enabled for {repo_name}")
                time.sleep(API_RATE_LIMIT_DELAY)
                return True, ""
            else:
                error_msg = f"Failed to enable Pages: {response.json().get('message', 'Unknown error')}"
                self.logger.warning(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Failed to enable GitHub Pages: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def protect_branch(self, repo_name: str, branch: str = "main",
                      require_reviews: bool = False,
                      require_status_checks: bool = False,
                      restrict_push: bool = False) -> Tuple[bool, str]:
        """
        Enable branch protection
        
        Args:
            repo_name: Repository name
            branch: Branch to protect
            require_reviews: Require PR reviews
            require_status_checks: Require status checks to pass
            restrict_push: Restrict who can push
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            self.logger.info(f"Protecting branch '{branch}' for {repo_name}")
            
            repo = self.user.get_repo(repo_name)
            branch_obj = repo.get_branch(branch)
            
            # Build protection rules
            protection_args = {
                "strict": require_status_checks,
                "contexts": []
            }
            
            if require_reviews:
                protection_args["required_approving_review_count"] = 1
            
            # Enable protection
            branch_obj.edit_protection(
                **protection_args
            )
            
            self.logger.info(f"Branch protection enabled for {repo_name}/{branch}")
            time.sleep(API_RATE_LIMIT_DELAY)
            return True, ""
            
        except Exception as e:
            error_msg = f"Failed to protect branch: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
