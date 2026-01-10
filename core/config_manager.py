"""
Configuration Manager for Github&Tailscale-Automation
Author: Haseeb Kaloya
Email: haseebkaloya@gmail.com

Handles saving and loading application configuration
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from utils.logger import get_logger

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_dir: str = "configs"):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Directory to store configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.logger = get_logger()
        
        # Default configuration template
        self.default_config = {
            # Accounts
            "github_username": "",
            "github_token": "",
            "tailscale_api": "",
            "tailscale_network": "",
            
            # Files
            "workflow_file": "",
            "project_folder": "",  # Backward compatibility
            "project_paths": [],  # New: multiple files/folders support
            "gitignore_file": "",
            
            # Repositories
            "repo_count": 10,
            "naming_strategy": {
                "strategy": "AutoGenerate",  # AutoGenerate, Custom, Sequential, ImportFile
                "custom_prefix": "",
                "sequential_prefix": "",
                "names_file": ""
            },
            "description": "",
            "private": True,
            
            # Secrets
            "shared_secrets_file": "",
            "repository_secrets": [],  # New: custom repository secrets with names
            "auto_generate_tailscale": True,  # Backward compatibility
            "tailscale_keys_file": "",  # Backward compatibility
            "skip_tailscale": False,  # Backward compatibility
            
            # Actions - Workflow Options
            "start_workflows": True,
            "wait_workflow_completion": False,
            "retry_failed_workflows": False,
            "workflow_timeout": 30,
            
            # Actions - Repository Settings
            "enable_issues": True,
            "enable_wiki": False,
            "enable_projects": False,
            "repo_topics": [],
            
            # Actions - Branch Protection
            "protect_main_branch": False,
            "require_pr_reviews": False,
            "require_status_checks": False,
            "restrict_push_access": False,
            
            # Actions - GitHub Pages
            "enable_github_pages": False,
            "pages_source": "main branch /root",
            
            # Actions - Backup & Logging
            "auto_backup": True,
            "detailed_logging": True
        }
    
    def save_config(self, filename: str, config: Dict[str, Any]) -> bool:
        """
        Save configuration to JSON file
        
        Args:
            filename: Full path or name of the configuration file
            config: Configuration dictionary to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if filename is already a full path
            filepath = Path(filename)
            if not filepath.is_absolute():
                # Relative path, join with config_dir
                filepath = self.config_dir / filename
            
            # Ensure .json extension
            if not filepath.suffix == '.json':
                filepath = filepath.with_suffix('.json')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Configuration saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def load_config(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load configuration from JSON file
        
        Args:
            filename: Full path or name of the configuration file
            
        Returns:
            Dict or None: Configuration dictionary if successful, None otherwise
        """
        try:
            # Check if filename is already a full path
            filepath = Path(filename)
            if not filepath.is_absolute():
                # Relative path, join with config_dir
                filepath = self.config_dir / filename
            
            # Ensure .json extension
            if not filepath.suffix == '.json':
                filepath = filepath.with_suffix('.json')
            
            if not filepath.exists():
                self.logger.warning(f"Configuration file not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Merge with default config for backward compatibility
            merged_config = self.default_config.copy()
            merged_config.update(config)
            
            self.logger.info(f"Configuration loaded from {filepath}")
            return merged_config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return None
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration
        
        Returns:
            Dict: Default configuration dictionary
        """
        return self.default_config.copy()
    
    def list_configs(self) -> list:
        """
        List all saved configuration files
        
        Returns:
            list: List of configuration file names
        """
        try:
            configs = [f.stem for f in self.config_dir.glob('*.json')]
            return sorted(configs)
        except Exception as e:
            self.logger.error(f"Failed to list configurations: {e}")
            return []
    
    def delete_config(self, filename: str) -> bool:
        """
        Delete a configuration file
        
        Args:
            filename: Name of the configuration file to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            filepath = self.config_dir / filename
            
            # Ensure .json extension
            if not filepath.suffix == '.json':
                filepath = filepath.with_suffix('.json')
            
            if filepath.exists():
                filepath.unlink()
                self.logger.info(f"Configuration deleted: {filepath}")
                return True
            else:
                self.logger.warning(f"Configuration not found: {filepath}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to delete configuration: {e}")
            return False
