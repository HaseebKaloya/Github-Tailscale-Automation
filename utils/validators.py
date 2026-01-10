"""
Input validation utilities for Github&Tailscale-Automation
Author: Haseeb Kaloya
"""

import re
from pathlib import Path
from typing import Tuple

def validate_github_token(token: str) -> Tuple[bool, str]:
    """
    Validate GitHub personal access token format
    
    Args:
        token: GitHub token to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not token or not token.strip():
        return False, "GitHub token cannot be empty"
    
    token = token.strip()
    
    # GitHub tokens start with ghp_ (classic) or github_pat_ (fine-grained)
    if not (token.startswith('ghp_') or token.startswith('github_pat_')):
        return False, "Invalid GitHub token format"
    
    if len(token) < 20:
        return False, "GitHub token is too short"
    
    return True, ""

def validate_tailscale_key(key: str) -> Tuple[bool, str]:
    """
    Validate Tailscale API key format
    
    Args:
        key: Tailscale API key to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not key or not key.strip():
        return False, "Tailscale API key cannot be empty"
    
    key = key.strip()
    
    # Tailscale keys start with tskey-
    if not key.startswith('tskey-'):
        return False, "Invalid Tailscale API key format"
    
    if len(key) < 30:
        return False, "Tailscale API key is too short"
    
    return True, ""

def validate_repository_name(name: str) -> Tuple[bool, str]:
    """
    Validate GitHub repository name
    
    Args:
        name: Repository name to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Repository name cannot be empty"
    
    name = name.strip()
    
    # GitHub repo names can contain alphanumeric, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        return False, "Repository name can only contain letters, numbers, hyphens, and underscores"
    
    if len(name) > 100:
        return False, "Repository name is too long (max 100 characters)"
    
    if name.startswith('-') or name.startswith('_'):
        return False, "Repository name cannot start with hyphen or underscore"
    
    return True, ""

def validate_file_path(path: str, must_exist: bool = True) -> Tuple[bool, str]:
    """
    Validate file path
    
    Args:
        path: File path to validate
        must_exist: If True, check if file exists
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not path or not path.strip():
        return False, "File path cannot be empty"
    
    file_path = Path(path.strip())
    
    if must_exist and not file_path.exists():
        return False, f"File not found: {path}"
    
    if must_exist and not file_path.is_file():
        return False, f"Path is not a file: {path}"
    
    return True, ""

def validate_folder_path(path: str, must_exist: bool = True) -> Tuple[bool, str]:
    """
    Validate folder path
    
    Args:
        path: Folder path to validate
        must_exist: If True, check if folder exists
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not path or not path.strip():
        return False, "Folder path cannot be empty"
    
    folder_path = Path(path.strip())
    
    if must_exist and not folder_path.exists():
        return False, f"Folder not found: {path}"
    
    if must_exist and not folder_path.is_dir():
        return False, f"Path is not a folder: {path}"
    
    return True, ""

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not email or not email.strip():
        return False, "Email cannot be empty"
    
    email = email.strip()
    
    # Basic email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""

def validate_repo_count(count: int, min_count: int = 1, max_count: int = 100) -> Tuple[bool, str]:
    """
    Validate repository count
    
    Args:
        count: Number of repositories
        min_count: Minimum allowed count
        max_count: Maximum allowed count
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if count < min_count:
        return False, f"Repository count must be at least {min_count}"
    
    if count > max_count:
        return False, f"Repository count cannot exceed {max_count}"
    
    return True, ""
