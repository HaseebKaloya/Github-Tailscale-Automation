"""
Configuration Validator for Github&Tailscale-Automation
Author: Haseeb Kaloya

Validates configuration before starting operations
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Any

from utils.logger import get_logger

class ConfigValidator:
    """Validates configuration settings"""
    
    def __init__(self):
        self.logger = get_logger()
        self.errors = []
        self.warnings = []
    
    def validate_full_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Perform comprehensive configuration validation
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors.clear()
        self.warnings.clear()
        
        # Core validation
        self._validate_github_config(config)
        self._validate_repository_config(config)
        self._validate_file_paths(config)
        self._validate_secrets_config(config)
        self._validate_tailscale_config(config)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors.copy(), self.warnings.copy()
    
    def _validate_github_config(self, config: Dict[str, Any]):
        """Validate GitHub configuration"""
        # Required fields
        if not config.get('github_username'):
            self.errors.append("GitHub username is required")
        elif not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', config['github_username']):
            self.errors.append("Invalid GitHub username format")
        
        if not config.get('github_token'):
            self.errors.append("GitHub token is required")
        elif not config['github_token'].startswith(('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_')):
            self.warnings.append("GitHub token format looks unusual - ensure it's a valid personal access token")
        
        # Token permissions check
        if config.get('github_token') and len(config['github_token']) < 40:
            self.warnings.append("GitHub token seems too short - ensure it has proper permissions")
    
    def _validate_repository_config(self, config: Dict[str, Any]):
        """Validate repository configuration"""
        repo_count = config.get('repo_count', 0)
        
        if not isinstance(repo_count, int) or repo_count < 1:
            self.errors.append("Repository count must be a positive integer")
        elif repo_count > 100:
            self.warnings.append("Creating more than 100 repositories may hit rate limits")
        
        # Naming strategy validation
        naming_strategy = config.get('naming_strategy', {})
        strategy = naming_strategy.get('strategy', 'AutoGenerate')
        
        if strategy == 'ImportFile':
            names_file = naming_strategy.get('names_file', '')
            if not names_file:
                self.errors.append("Names file path is required for ImportFile strategy")
            elif not Path(names_file).exists():
                self.errors.append(f"Names file not found: {names_file}")
            else:
                # Check if file has enough names
                try:
                    with open(names_file, 'r') as f:
                        names = [line.strip() for line in f if line.strip()]
                    if len(names) < repo_count:
                        self.warnings.append(f"Names file only has {len(names)} names but need {repo_count}")
                except Exception as e:
                    self.errors.append(f"Cannot read names file: {e}")
        
        # Repository settings validation
        description = config.get('description', '')
        if len(description) > 350:
            self.warnings.append("Repository description is very long (>350 chars)")
    
    def _validate_file_paths(self, config: Dict[str, Any]):
        """Validate file paths"""
        # Workflow file
        workflow_file = config.get('workflow_file', '')
        if workflow_file:
            if not Path(workflow_file).exists():
                self.errors.append(f"Workflow file not found: {workflow_file}")
            elif not workflow_file.lower().endswith(('.yml', '.yaml')):
                self.warnings.append("Workflow file should have .yml or .yaml extension")
        
        # .gitignore file
        gitignore_file = config.get('gitignore_file', '')
        if gitignore_file and not Path(gitignore_file).exists():
            self.errors.append(f".gitignore file not found: {gitignore_file}")
        
        # Project paths
        project_paths = config.get('project_paths', [])
        for path in project_paths:
            if not Path(path).exists():
                self.errors.append(f"Project path not found: {path}")
    
    def _validate_secrets_config(self, config: Dict[str, Any]):
        """Validate secrets configuration"""
        # Shared secrets file
        shared_secrets_file = config.get('shared_secrets_file', '')
        if shared_secrets_file:
            if not Path(shared_secrets_file).exists():
                self.errors.append(f"Shared secrets file not found: {shared_secrets_file}")
            else:
                # Validate format
                try:
                    with open(shared_secrets_file, 'r') as f:
                        lines = f.readlines()
                    
                    valid_secrets = 0
                    for line_num, line in enumerate(lines, 1):
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        
                        if '=' not in line:
                            self.warnings.append(f"Invalid secret format on line {line_num}: {line}")
                        else:
                            key, value = line.split('=', 1)
                            if not re.match(r'^[A-Z0-9_]+$', key.strip()):
                                self.warnings.append(f"Invalid secret name on line {line_num}: {key.strip()}")
                            else:
                                valid_secrets += 1
                    
                    if valid_secrets == 0:
                        self.warnings.append("No valid secrets found in shared secrets file")
                        
                except Exception as e:
                    self.errors.append(f"Cannot read shared secrets file: {e}")
        
        # Repository secrets
        repository_secrets = config.get('repository_secrets', [])
        secret_names = set()
        
        for secret in repository_secrets:
            name = secret.get('name', '')
            source = secret.get('source', '')
            
            # Validate name
            if not name:
                self.errors.append("Repository secret name cannot be empty")
            elif not re.match(r'^[A-Z0-9_]+$', name):
                self.errors.append(f"Invalid secret name format: {name}")
            elif name in secret_names:
                self.errors.append(f"Duplicate secret name: {name}")
            else:
                secret_names.add(name)
            
            # Validate source-specific requirements
            if source == 'custom_value':
                if not secret.get('value'):
                    self.errors.append(f"Custom value required for secret: {name}")
            elif source == 'import_file':
                file_path = secret.get('file_path', '')
                if not file_path:
                    self.errors.append(f"File path required for secret: {name}")
                elif not Path(file_path).exists():
                    self.errors.append(f"Secret file not found for {name}: {file_path}")
    
    def _validate_tailscale_config(self, config: Dict[str, Any]):
        """Validate Tailscale configuration"""
        # Check if any secrets require Tailscale
        repository_secrets = config.get('repository_secrets', [])
        needs_tailscale = any(s.get('source') == 'tailscale_auto' for s in repository_secrets)
        
        if needs_tailscale:
            if not config.get('tailscale_api'):
                self.errors.append("Tailscale API key required for auto-generated secrets")
            elif len(config['tailscale_api']) < 20:
                self.warnings.append("Tailscale API key seems too short")
            
            if not config.get('tailscale_network'):
                self.errors.append("Tailscale network/tailnet required for auto-generated secrets")
    
    def generate_validation_report(self, config: Dict[str, Any]) -> str:
        """Generate a detailed validation report"""
        is_valid, errors, warnings = self.validate_full_config(config)
        
        report = ["🔍 Configuration Validation Report", "=" * 50]
        
        if is_valid and not warnings:
            report.append("✅ Configuration is valid - no issues found!")
        else:
            if errors:
                report.append(f"\n❌ ERRORS ({len(errors)}):")
                for i, error in enumerate(errors, 1):
                    report.append(f"  {i}. {error}")
            
            if warnings:
                report.append(f"\n⚠️  WARNINGS ({len(warnings)}):")
                for i, warning in enumerate(warnings, 1):
                    report.append(f"  {i}. {warning}")
        
        report.append(f"\n📊 Summary:")
        report.append(f"  • Repositories to create: {config.get('repo_count', 0)}")
        report.append(f"  • Repository secrets: {len(config.get('repository_secrets', []))}")
        report.append(f"  • Workflow file: {'Yes' if config.get('workflow_file') else 'No'}")
        report.append(f"  • Project files: {len(config.get('project_paths', []))}")
        
        return '\n'.join(report)
