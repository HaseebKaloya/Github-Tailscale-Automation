"""
Repository Creator Workflow for Github&Tailscale-Automation
Author: Haseeb Kaloya
Email: haseebkaloya@gmail.com

Main workflow that orchestrates repository creation with files, secrets, and workflows
"""

import time
from typing import Dict, Any, List, Callable, Optional
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal

from api.github_api import GitHubAPI
from api.tailscale_api import TailscaleAPI
from utils.logger import get_logger
from utils.helpers import generate_backup_filename
from core.constants import AUTO_GEN_PREFIXES
from github import GithubException
import random

class RepositoryCreator(QThread):
    """Worker thread for creating repositories"""
    
    # Error handling constants
    MAX_CONSECUTIVE_ERRORS = 5
    MAX_RETRY_ATTEMPTS = 3
    RETRY_DELAY_BASE = 2  # seconds
    REPO_READY_MAX_ATTEMPTS = 10
    REPO_READY_WAIT = 2  # seconds
    
    # Signals for progress updates
    progress_updated = pyqtSignal(int, str, str)  # overall_percent, step_name, activity
    step_completed = pyqtSignal(str)  # step_name
    step_started = pyqtSignal(str)  # step_name
    finished = pyqtSignal(bool, str, dict)  # success, message, results
    stats_updated = pyqtSignal(int, int, int, int)  # total, created, current, failed
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize repository creator
        
        Args:
            config: Configuration dictionary with all settings
        """
        super().__init__()
        self.config = config
        self.cancel_requested = False
        self.logger = get_logger()
        
        # Results tracking
        self.created_repos = []
        self.generated_keys = []
        self.errors = []
        self.failed_repos = []
        self.consecutive_errors = 0
        self.total_repos = 0
        self.current_repo_index = 0
    
    def run(self):
        """Main workflow execution"""
        try:
            self.logger.info("="*60)
            self.logger.info("Starting Repository Creation Workflow")
            self.logger.info("="*60)
            
            start_time = time.time()
            
            # Step 1: Validate configuration
            self._emit_step("Validating", 0)
            if not self._validate_config():
                self.finished.emit(False, "Configuration validation failed", {})
                return
            self._emit_progress(5, "Validating", 100, "Configuration validated")
            self._emit_complete("Validating")
            
            # Step 2: Initialize APIs
            self._emit_step("Initializing", 10)
            github_api, tailscale_api = self._initialize_apis()
            if not github_api:
                self.finished.emit(False, "Failed to initialize APIs", {})
                return
            self._emit_progress(15, "Initializing", 100, "APIs initialized")
            self._emit_complete("Initializing")
            
            # Step 3: Generate repository names
            self._emit_step("Preparing", 20)
            repo_names = self._generate_repository_names()
            self._emit_progress(25, "Preparing", 100, f"Generated {len(repo_names)} repository names")
            
            # Step 4: Generate Tailscale keys (if enabled)
            if self.config.get('auto_generate_tailscale', False) and tailscale_api:
                self._emit_step("Generating", 30)
                success = self._generate_tailscale_keys(tailscale_api, len(repo_names))
                if not success:
                    self.logger.warning("Tailscale key generation failed, continuing without keys")
                self._emit_complete("Generating")
            
            # Step 5: Create repositories
            self._emit_step("Creating", 40)
            success = self._create_repositories(github_api, repo_names)
            if not success:
                self.finished.emit(False, "Repository creation failed", {})
                return
            self._emit_complete("Creating")
            
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            
            # Prepare results
            results = {
                "created_repos": self.created_repos,
                "generated_keys": len(self.generated_keys),
                "errors": self.errors,
                "elapsed_time": elapsed_time
            }
            
            # Complete
            self._emit_progress(100, "Complete", 100, "All repositories created!")
            self._emit_complete("Finalizing")
            
            success_msg = f"Successfully created {len(self.created_repos)} repositories in {elapsed_time:.1f}s"
            self.logger.info(success_msg)
            self.finished.emit(True, success_msg, results)
            
        except Exception as e:
            error_msg = f"Fatal error in workflow: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            self.finished.emit(False, error_msg, {})
    
    def cancel(self):
        """Request cancellation of the workflow"""
        self.cancel_requested = True
        self.logger.info("Cancellation requested")
    
    def _validate_config(self) -> bool:
        """Comprehensive configuration validation with pre-flight checks"""
        try:
            self._emit_progress(1, "Validating", 10, "Checking required fields...")
            
            # Check required fields
            required_fields = ['github_username', 'github_token', 'repo_count']
            for field in required_fields:
                if not self.config.get(field):
                    self.logger.error(f"Missing required field: {field}")
                    return False
            
            # Validate repository count
            repo_count = self.config.get('repo_count', 0)
            if repo_count < 1 or repo_count > 100:
                self.logger.error(f"Invalid repo_count: {repo_count}. Must be between 1 and 100")
                return False
            
            self._emit_progress(2, "Validating", 30, "Testing GitHub API connection...")
            
            # PRE-FLIGHT: Test GitHub API connectivity
            try:
                test_api = GitHubAPI(
                    self.config['github_token'],
                    self.config['github_username']
                )
                success, message = test_api.test_connection()
                if not success:
                    self.logger.error(f"GitHub API connection failed: {message}")
                    return False
                self.logger.info(f"GitHub API connection successful: {message}")
            except Exception as e:
                self.logger.error(f"Failed to connect to GitHub API: {e}")
                return False
            
            self._emit_progress(3, "Validating", 50, "Validating file paths...")
            
            # Validate file paths if provided
            workflow_file = self.config.get('workflow_file', '')
            if workflow_file and not Path(workflow_file).exists():
                self.logger.error(f"Workflow file not found: {workflow_file}")
                return False
            
            gitignore_file = self.config.get('gitignore_file', '')
            if gitignore_file and not Path(gitignore_file).exists():
                self.logger.error(f".gitignore file not found: {gitignore_file}")
                return False
            
            # Validate project paths
            project_paths = self.config.get('project_paths', [])
            for path in project_paths:
                if not Path(path).exists():
                    self.logger.error(f"Project path not found: {path}")
                    return False
            
            # Validate Tailscale if enabled
            if self.config.get('auto_generate_tailscale'):
                self._emit_progress(4, "Validating", 70, "Testing Tailscale API...")
                
                if not self.config.get('tailscale_api') or not self.config.get('tailscale_network'):
                    self.logger.error("Tailscale credentials required for auto-generation")
                    return False
                
                # PRE-FLIGHT: Test Tailscale API connectivity
                try:
                    test_tailscale = TailscaleAPI(
                        self.config['tailscale_api'],
                        self.config['tailscale_network']
                    )
                    success, message = test_tailscale.test_connection()
                    if not success:
                        self.logger.error(f"Tailscale API connection failed: {message}")
                        return False
                    self.logger.info(f"Tailscale API connection successful: {message}")
                except Exception as e:
                    self.logger.error(f"Failed to connect to Tailscale API: {e}")
                    return False
            
            # Validate secrets configuration
            repository_secrets = self.config.get('repository_secrets', [])
            for secret in repository_secrets:
                if secret.get('source') == 'import_file':
                    file_path = secret.get('file_path', '')
                    if file_path and not Path(file_path).exists():
                        self.logger.error(f"Secret file not found: {file_path}")
                        return False
            
            self._emit_progress(5, "Validating", 100, "All validations passed!")
            self.logger.info("Configuration validation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation error: {e}", exc_info=True)
            return False
    
    def _initialize_apis(self) -> tuple:
        """Initialize GitHub and Tailscale APIs"""
        try:
            # Initialize GitHub API
            github_api = GitHubAPI(
                self.config['github_token'],
                self.config['github_username']
            )
            
            # Initialize Tailscale API if needed
            tailscale_api = None
            if self.config.get('auto_generate_tailscale'):
                tailscale_api = TailscaleAPI(
                    self.config['tailscale_api'],
                    self.config['tailscale_network']
                )
            
            return github_api, tailscale_api
            
        except Exception as e:
            self.logger.error(f"API initialization error: {e}")
            return None, None
    
    def _generate_repository_names(self) -> List[str]:
        """Generate repository names based on strategy"""
        try:
            count = self.config['repo_count']
            strategy_config = self.config.get('naming_strategy', {})
            strategy = strategy_config.get('strategy', 'AutoGenerate')
            
            names = []
            
            if strategy == 'AutoGenerate':
                # Use Greek letter prefixes
                for i in range(count):
                    prefix = AUTO_GEN_PREFIXES[i % len(AUTO_GEN_PREFIXES)]
                    names.append(f"github-{prefix}-{i+1:02d}")
            
            elif strategy == 'Custom':
                prefix = strategy_config.get('custom_prefix', 'repo')
                for i in range(count):
                    names.append(f"{prefix}-{i+1:02d}")
            
            elif strategy == 'Sequential':
                prefix = strategy_config.get('sequential_prefix', 'project')
                for i in range(count):
                    names.append(f"{prefix}-{i+1:02d}")
            
            elif strategy == 'ImportFile':
                names_file = strategy_config.get('names_file', '')
                if names_file and Path(names_file).exists():
                    with open(names_file, 'r', encoding='utf-8') as f:
                        file_names = [line.strip() for line in f if line.strip()]
                    names = file_names[:count]
                else:
                    # Fallback to auto-generate
                    self.logger.warning("Names file not found, using auto-generate")
                    for i in range(count):
                        names.append(f"repo-{i+1:02d}")
            
            else:
                # Default fallback
                for i in range(count):
                    names.append(f"repo-{i+1:02d}")
            
            self.logger.info(f"Generated {len(names)} repository names using {strategy} strategy")
            return names
            
        except Exception as e:
            self.logger.error(f"Name generation error: {e}")
            # Return default names
            return [f"repo-{i+1:02d}" for i in range(self.config['repo_count'])]
    
    def _retry_with_exponential_backoff(self, func, *args, **kwargs):
        """
        Retry function with exponential backoff on rate limit and network errors
        
        Args:
            func: Function to retry
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or raises exception after max retries
        """
        for attempt in range(self.MAX_RETRY_ATTEMPTS):
            try:
                return func(*args, **kwargs)
            except GithubException as e:
                # Handle Rate Limit (403) and Server Errors (5xx)
                if (e.status == 403 and 'rate limit' in str(e).lower()) or e.status >= 500:
                    wait_time = (self.RETRY_DELAY_BASE ** attempt) + random.uniform(0, 1)
                    self.logger.warning(f"GitHub API Error ({e.status}), waiting {wait_time:.1f}s before retry {attempt+1}/{self.MAX_RETRY_ATTEMPTS}")
                    time.sleep(wait_time)
                    if attempt == self.MAX_RETRY_ATTEMPTS - 1: raise
                else:
                    raise  # Client error, don't retry
            except Exception as e:
                # Handle network-related errors
                import requests
                if isinstance(e, (requests.exceptions.RequestException, ConnectionError, TimeoutError)):
                    wait_time = (self.RETRY_DELAY_BASE ** attempt) + random.uniform(0, 1)
                    self.logger.warning(f"Network Error ({type(e).__name__}), waiting {wait_time:.1f}s before retry {attempt+1}/{self.MAX_RETRY_ATTEMPTS}")
                    time.sleep(wait_time)
                    if attempt == self.MAX_RETRY_ATTEMPTS - 1: raise
                else:
                    raise  # Unknown error, re-raise immediately
        
        raise Exception("Max retries exceeded")
    
    def _wait_for_repository_ready(self, api: GitHubAPI, repo_name: str) -> bool:
        """
        Wait for repository to be fully initialized and ready
        
        Args:
            api: GitHub API instance
            repo_name: Repository name
            
        Returns:
            bool: True if ready, False if timeout
        """
        for attempt in range(self.REPO_READY_MAX_ATTEMPTS):
            try:
                repo = api.user.get_repo(repo_name)
                # Try to get default branch - if this works, repo is ready
                default_branch = repo.get_branch(repo.default_branch)
                self.logger.info(f"Repository {repo_name} is ready (attempt {attempt+1})")
                return True
            except GithubException as e:
                if e.status == 404:
                    # Not ready yet
                    self.logger.debug(f"Waiting for {repo_name} to be ready... (attempt {attempt+1}/{self.REPO_READY_MAX_ATTEMPTS})")
                    time.sleep(self.REPO_READY_WAIT)
                    continue
                else:
                    # Different error, log and return False
                    self.logger.warning(f"Error checking repository readiness: {e}")
                    return False
            except Exception as e:
                self.logger.warning(f"Unexpected error waiting for repository: {e}")
                return False
        
        self.logger.warning(f"Repository {repo_name} not ready after {self.REPO_READY_MAX_ATTEMPTS} attempts")
        return False
    
    def _update_statistics(self):
        """Emit statistics update signal"""
        try:
            self.stats_updated.emit(
                self.total_repos,
                len(self.created_repos),
                self.current_repo_index,
                len(self.failed_repos)
            )
        except Exception as e:
            self.logger.error(f"Error updating statistics: {e}")
    
    def _generate_tailscale_keys(self, api: TailscaleAPI, count: int) -> bool:
        """Generate Tailscale auth keys with validation"""
        try:
            self.logger.info(f"Generating {count} Tailscale auth keys...")
            
            def progress_callback(current, total, message):
                percent = int((current / total) * 100)
                self._emit_progress(30 + (percent * 0.1), "Generating", percent, message)
            
            success, keys, error = api.generate_multiple_keys(
                count=count,
                progress_callback=progress_callback
            )
            
            if success and keys:
                self.generated_keys = keys
                
                # Validate key count matches repo count
                if len(keys) < count:
                    warning_msg = f"⚠️ Generated only {len(keys)}/{count} keys. Some repositories may not receive Tailscale secrets."
                    self.logger.warning(warning_msg)
                    self.errors.append(warning_msg)
                else:
                    self.logger.info(f"✓ Successfully generated {len(keys)} Tailscale auth keys")
                
                # Save backup if enabled
                if self.config.get('auto_backup', True):
                    backup_success, filepath = api.save_keys_to_file(keys)
                    if backup_success:
                        self.logger.info(f"✓ Keys backed up to: {filepath}")
                    else:
                        self.logger.warning(f"⚠️ Failed to save backup file: {filepath}")
                else:
                    self.logger.info(f"Auto-backup disabled - keys not saved to file")
                
                return True
            else:
                error_msg = f"Tailscale key generation failed: {error}"
                self.logger.error(error_msg)
                self.errors.append(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Fatal error generating Tailscale keys: {e}"
            self.logger.error(error_msg, exc_info=True)
            self.errors.append(error_msg)
            return False
    
    def _create_repositories(self, api: GitHubAPI, names: List[str]) -> bool:
        """Create all repositories with enhanced error handling and retry logic"""
        try:
            self.total_repos = len(names)
            self.consecutive_errors = 0
            
            for i, name in enumerate(names):
                self.current_repo_index = i + 1
                
                # Check for cancellation
                if self.cancel_requested:
                    self.logger.info("Creation cancelled by user")
                    return False
                
                # Check for too many consecutive errors
                if self.consecutive_errors >= self.MAX_CONSECUTIVE_ERRORS:
                    error_msg = f"Aborting: {self.consecutive_errors} consecutive failures"
                    self.logger.error(error_msg)
                    self.errors.append(error_msg)
                    return False
                
                # Calculate progress
                overall_percent = 40 + int((i / self.total_repos) * 50)
                
                # Update progress
                self._emit_progress(
                    overall_percent,
                    "Creating",
                    0,
                    f"Creating repository {i+1}/{self.total_repos}: {name}"
                )
                
                # Update statistics
                self._update_statistics()
                
                try:
                    # Create repository with retry logic
                    success, result = self._retry_with_exponential_backoff(
                        api.create_repository,
                        name=name,
                        description=self.config.get('description', ''),
                        private=self.config.get('private', True),
                        auto_init=True,
                        has_issues=self.config.get('enable_issues', True),
                        has_wiki=self.config.get('enable_wiki', False),
                        has_projects=self.config.get('enable_projects', False)
                    )
                    
                    if not success:
                        self.consecutive_errors += 1
                        self.failed_repos.append(name)
                        self.errors.append(f"Failed to create {name}: {result}")
                        self.logger.error(f"Failed to create {name}: {result}")
                        self._update_statistics()
                        continue
                    
                    # Reset consecutive errors on success
                    self.consecutive_errors = 0
                    self.created_repos.append(name)
                    self.logger.info(f"[SUCCESS] Created repository: {name}")
                    
                    # Wait for repository to be fully ready
                    self._emit_progress(
                        overall_percent,
                        "Creating",
                        30,
                        f"Waiting for {name} to be ready..."
                    )
                    
                    if not self._wait_for_repository_ready(api, name):
                        self.logger.warning(f"Repository {name} may not be fully ready, proceeding cautiously")
                    
                    # Apply additional repository settings
                    self._emit_progress(
                        overall_percent,
                        "Creating",
                        40,
                        f"Applying settings to {name}..."
                    )
                    self._apply_repository_settings(api, name)
                    
                    # Upload workflow file if specified
                    if self.config.get('workflow_file'):
                        self._emit_progress(
                            overall_percent,
                            "Creating",
                            50,
                            f"Uploading workflow to {name}..."
                        )
                        self._upload_workflow(api, name)
                    
                    # Upload .gitignore file if specified
                    if self.config.get('gitignore_file'):
                        self._emit_progress(
                            overall_percent,
                            "Creating",
                            60,
                            f"Uploading .gitignore to {name}..."
                        )
                        self._upload_gitignore(api, name)
                    
                    # Upload project folder if specified
                    if self.config.get('project_folder') or self.config.get('project_paths'):
                        self._emit_progress(
                            overall_percent,
                            "Creating",
                            70,
                            f"Uploading files to {name}..."
                        )
                        self._upload_folder(api, name)
                    
                    # Add secrets
                    self._emit_progress(
                        overall_percent,
                        "Creating",
                        85,
                        f"Adding secrets to {name}..."
                    )
                    
                    # Add small delay to ensure repository is fully accessible
                    time.sleep(2)
                    self._add_secrets(api, name, i)
                    
                    # Start workflow if enabled
                    if self.config.get('start_workflows'):
                        self._emit_progress(
                            overall_percent,
                            "Creating",
                            95,
                            f"Starting workflow for {name}..."
                        )
                        try:
                            success, error = api.start_workflow(name)
                            if not success:
                                error_msg = f"Failed to start workflow for {name}: {error}"
                                self.logger.error(error_msg)
                                self.errors.append(error_msg)
                            else:
                                self.logger.info(f"[SUCCESS] Workflow started successfully for {name}")
                        except Exception as wf_error:
                            error_msg = f"Exception starting workflow for {name}: {str(wf_error)}"
                            self.logger.error(error_msg, exc_info=True)
                            self.errors.append(error_msg)
                    
                    self._emit_progress(
                        overall_percent,
                        "Creating",
                        100,
                        f"[COMPLETED] {name}"
                    )
                    
                    # Update statistics after successful completion
                    self._update_statistics()
                    
                except Exception as repo_error:
                    self.consecutive_errors += 1
                    self.failed_repos.append(name)
                    error_msg = f"Error processing {name}: {str(repo_error)}"
                    self.errors.append(error_msg)
                    self.logger.error(error_msg, exc_info=True)
                    self._update_statistics()
                    continue
            
            # Return True if at least one repo was created successfully
            success = len(self.created_repos) > 0
            
            if not success:
                self.logger.error("No repositories were created successfully")
            else:
                self.logger.info(f"Successfully created {len(self.created_repos)}/{self.total_repos} repositories")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Fatal error in repository creation: {e}", exc_info=True)
            return False
    
    def _apply_repository_settings(self, api: GitHubAPI, repo_name: str):
        """Apply additional repository settings (topics, branch protection, GitHub Pages)"""
        try:
            # Set repository topics
            topics = self.config.get('repo_topics', [])
            if topics:
                self.logger.info(f"Setting topics for {repo_name}: {topics}")
                api.set_repository_topics(repo_name, topics)
            
            # Enable GitHub Pages if requested
            if self.config.get('enable_github_pages', False):
                pages_source = self.config.get('pages_source', 'main branch /root')
                self.logger.info(f"Enabling GitHub Pages for {repo_name}")
                api.enable_github_pages(repo_name, pages_source)
            
            # Apply branch protection if requested
            if self.config.get('protect_main_branch', False):
                self.logger.info(f"Applying branch protection for {repo_name}")
                api.protect_branch(
                    repo_name,
                    branch="main",
                    require_reviews=self.config.get('require_pr_reviews', False),
                    require_status_checks=self.config.get('require_status_checks', False),
                    restrict_push=self.config.get('restrict_push_access', False)
                )
        except Exception as e:
            self.logger.error(f"Error applying repository settings for {repo_name}: {e}")
    
    def _upload_workflow(self, api: GitHubAPI, repo_name: str):
        """Upload workflow file to repository with validation"""
        try:
            workflow_file = self.config.get('workflow_file', '')
            if not workflow_file:
                return
            
            workflow_path = Path(workflow_file)
            if not workflow_path.exists():
                self.logger.error(f"Workflow file not found: {workflow_file}")
                self.errors.append(f"{repo_name}: Workflow file not found")
                return
            
            # Validate it's a YAML file
            if workflow_path.suffix.lower() not in ['.yml', '.yaml']:
                self.logger.warning(f"Workflow file doesn't have .yml/.yaml extension: {workflow_file}")
            
            # Check file is not empty
            if workflow_path.stat().st_size == 0:
                self.logger.error(f"Workflow file is empty: {workflow_file}")
                self.errors.append(f"{repo_name}: Workflow file is empty")
                return
            
            # Upload the file
            success, error = api.upload_file(
                repo_name,
                workflow_file,
                ".github/workflows/main.yml",
                "Add workflow file"
            )
            
            if success:
                self.logger.info(f"[SUCCESS] Uploaded workflow file to {repo_name}")
            else:
                self.logger.error(f"Failed to upload workflow to {repo_name}: {error}")
                self.errors.append(f"{repo_name}: Workflow upload failed - {error}")
                
        except Exception as e:
            self.logger.error(f"Workflow upload error for {repo_name}: {e}", exc_info=True)
            self.errors.append(f"{repo_name}: Workflow upload exception - {str(e)}")
    
    def _upload_gitignore(self, api: GitHubAPI, repo_name: str):
        """Upload .gitignore file to repository with validation"""
        try:
            gitignore_file = self.config.get('gitignore_file', '')
            if not gitignore_file:
                return
            
            gitignore_path = Path(gitignore_file)
            if not gitignore_path.exists():
                self.logger.error(f".gitignore file not found: {gitignore_file}")
                self.errors.append(f"{repo_name}: .gitignore file not found")
                return
            
            # Upload the file
            success, error = api.upload_file(
                repo_name,
                gitignore_file,
                ".gitignore",
                "Add .gitignore"
            )
            
            if success:
                self.logger.info(f"[SUCCESS] Uploaded .gitignore to {repo_name}")
            else:
                self.logger.error(f"Failed to upload .gitignore to {repo_name}: {error}")
                self.errors.append(f"{repo_name}: .gitignore upload failed - {error}")
                
        except Exception as e:
            self.logger.error(f".gitignore upload error for {repo_name}: {e}", exc_info=True)
            self.errors.append(f"{repo_name}: .gitignore upload exception - {str(e)}")
    
    def _upload_folder(self, api: GitHubAPI, repo_name: str):
        """Upload project files/folders to repository with validation (supports multiple items)"""
        try:
            # Check for new multiple paths format first
            project_paths = self.config.get('project_paths', [])
            
            # Backward compatibility: if no project_paths, try single project_folder
            if not project_paths:
                single_path = self.config.get('project_folder', '')
                if single_path:
                    project_paths = [single_path]
            
            if not project_paths:
                return  # Nothing to upload
            
            uploaded_count = 0
            failed_count = 0
            
            # Upload each item
            for path_str in project_paths:
                if not Path(path_str).exists():
                    error_msg = f"Path does not exist: {path_str}"
                    self.logger.error(error_msg)
                    self.errors.append(f"{repo_name}: {error_msg}")
                    failed_count += 1
                    continue
                
                path_obj = Path(path_str)
                item_name = path_obj.name
                
                try:
                    if path_obj.is_file():
                        # Upload single file to root with original name
                        self.logger.info(f"Uploading file: {item_name} to {repo_name}/{item_name}")
                        success, error = api.upload_file(
                            repo_name,
                            path_str,
                            item_name,
                            f"Add {item_name}"
                        )
                        
                        if success:
                            self.logger.info(f"[SUCCESS] Uploaded file {item_name} to {repo_name}")
                            uploaded_count += 1
                        else:
                            self.logger.error(f"Failed to upload file {item_name}: {error}")
                            self.errors.append(f"{repo_name}: File upload failed - {item_name}")
                            failed_count += 1
                            
                    elif path_obj.is_dir():
                        # Upload folder contents to folder with original name
                        self.logger.info(f"Uploading folder: {item_name} to {repo_name}/{item_name}/")
                        success, error = api.upload_folder(
                            repo_name,
                            path_str,
                            item_name,
                            f"Add {item_name}"
                        )
                        
                        if success:
                            self.logger.info(f"[SUCCESS] Uploaded folder {item_name} to {repo_name}")
                            uploaded_count += 1
                        else:
                            self.logger.error(f"Failed to upload folder {item_name}: {error}")
                            self.errors.append(f"{repo_name}: Folder upload failed - {item_name}")
                            failed_count += 1
                            
                except Exception as item_error:
                    self.logger.error(f"Error uploading {item_name} to {repo_name}: {item_error}")
                    self.errors.append(f"{repo_name}: Upload exception - {item_name}")
                    failed_count += 1
            
            # Log summary
            self.logger.info(f"Upload summary for {repo_name}: {uploaded_count} succeeded, {failed_count} failed")
            
        except Exception as e:
            self.logger.error(f"Fatal error in file/folder upload for {repo_name}: {e}", exc_info=True)
            self.errors.append(f"{repo_name}: File upload fatal error - {str(e)}")
    
    def _add_secrets(self, api: GitHubAPI, repo_name: str, index: int):
        """Add secrets to repository with enhanced validation (supports custom names and multiple secrets)"""
        try:
            secrets_added = 0
            secrets_failed = 0
            
            # Add custom repository secrets
            repository_secrets = self.config.get('repository_secrets', [])
            for secret in repository_secrets:
                secret_name = secret['name']
                secret_source = secret['source']
                
                try:
                    if secret_source == 'tailscale_auto':
                        # Use unique Tailscale key per repository
                        if not self.generated_keys:
                            error_msg = f"No Tailscale keys were generated for {secret_name}"
                            self.logger.error(error_msg)
                            self.errors.append(f"{repo_name}: {error_msg}")
                            secrets_failed += 1
                            continue
                        
                        if index >= len(self.generated_keys):
                            error_msg = f"Not enough Tailscale keys generated. Need {index+1}, have {len(self.generated_keys)}"
                            self.logger.error(error_msg)
                            self.errors.append(f"{repo_name}: {error_msg}")
                            secrets_failed += 1
                            continue
                        
                        secret_value = self.generated_keys[index]
                        success, error = api.add_secret(repo_name, secret_name, secret_value)
                        if success:
                            self.logger.info(f"[SUCCESS] Added {secret_name} (Tailscale key #{index+1}) to {repo_name}")
                            secrets_added += 1
                        else:
                            error_msg = f"Failed to add {secret_name}: {error}"
                            self.logger.error(error_msg)
                            self.errors.append(f"{repo_name}: {error_msg}")
                            secrets_failed += 1
                    
                    elif secret_source == 'custom_value':
                        # Use same custom value for all repositories
                        secret_value = secret['value']
                        if secret_value:
                            success, error = api.add_secret(repo_name, secret_name, secret_value)
                            if success:
                                self.logger.info(f"[SUCCESS] Added {secret_name} (custom value) to {repo_name}")
                                secrets_added += 1
                            else:
                                error_msg = f"Failed to add {secret_name}: {error}"
                                self.logger.error(error_msg)
                                self.errors.append(f"{repo_name}: {error_msg}")
                                secrets_failed += 1
                        else:
                            self.logger.warning(f"Empty custom value for secret {secret_name}")
                            secrets_failed += 1
                    
                    elif secret_source == 'import_file':
                        # Use different value per repository from file
                        file_path = secret['file_path']
                        if file_path and Path(file_path).exists():
                            from utils.helpers import read_lines_from_file
                            values = read_lines_from_file(file_path)
                            if index < len(values):
                                secret_value = values[index]
                                success, error = api.add_secret(repo_name, secret_name, secret_value)
                                if success:
                                    self.logger.info(f"[SUCCESS] Added {secret_name} (from file, line {index+1}) to {repo_name}")
                                    secrets_added += 1
                                else:
                                    error_msg = f"Failed to add {secret_name}: {error}"
                                    self.logger.error(error_msg)
                                    self.errors.append(f"{repo_name}: {error_msg}")
                                    secrets_failed += 1
                            else:
                                error_msg = f"Not enough values in file for {secret_name}. Need {index+1}, have {len(values)}"
                                self.logger.error(error_msg)
                                self.errors.append(f"{repo_name}: {error_msg}")
                                secrets_failed += 1
                        else:
                            error_msg = f"File not found for secret {secret_name}: {file_path}"
                            self.logger.error(error_msg)
                            secrets_failed += 1
                
                except Exception as e:
                    self.logger.error(f"Error adding secret {secret_name} to {repo_name}: {e}")
                    secrets_failed += 1
            
            # Add shared secrets from file (same for all repositories)
            shared_secrets_file = self.config.get('shared_secrets_file', '')
            if shared_secrets_file and Path(shared_secrets_file).exists():
                from utils.helpers import read_lines_from_file
                secrets_lines = read_lines_from_file(shared_secrets_file)
                
                for line in secrets_lines:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key and value:
                            try:
                                success, error = api.add_secret(repo_name, key, value)
                                if success:
                                    self.logger.info(f"[SUCCESS] Added shared secret {key} to {repo_name}")
                                    secrets_added += 1
                                else:
                                    error_msg = f"Failed to add shared secret {key}: {error}"
                                    self.logger.error(error_msg)
                                    self.errors.append(f"{repo_name}: {error_msg}")
                                    secrets_failed += 1
                            except Exception as e:
                                self.logger.error(f"Error adding shared secret {key} to {repo_name}: {e}")
                                secrets_failed += 1
            
            # Log summary
            if secrets_added > 0 or secrets_failed > 0:
                self.logger.info(f"Secrets summary for {repo_name}: {secrets_added} added, {secrets_failed} failed")
            
        except Exception as e:
            self.logger.error(f"Fatal error in secret addition for {repo_name}: {e}", exc_info=True)
    
    def _emit_progress(self, overall: int, step: str, step_percent: int, activity: str):
        """Emit progress signal"""
        self.progress_updated.emit(overall, step, activity)
    
    def _emit_step(self, step: str, percent: int):
        """Emit step started signal"""
        self.step_started.emit(step)
        self._emit_progress(percent, step, 0, f"Starting {step}...")
    
    def _emit_complete(self, step: str):
        """Emit step completed signal"""
        self.step_completed.emit(step)
