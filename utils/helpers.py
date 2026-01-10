"""
Helper utilities for Github&Tailscale-Automation
Author: Haseeb Kaloya
"""

import time
from pathlib import Path
from datetime import datetime
from typing import List

def format_file_size(bytes_size: int) -> str:
    """
    Format byte size to human-readable format
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        str: Formatted size string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration (e.g., "2h 15m 30s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    
    return " ".join(parts)

def get_timestamp(format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get current timestamp as formatted string
    
    Args:
        format_string: strftime format string
        
    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime(format_string)

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename

def count_files_in_directory(directory: str) -> int:
    """
    Count all files in directory recursively
    
    Args:
        directory: Path to directory
        
    Returns:
        int: Total number of files
    """
    try:
        dir_path = Path(directory)
        return len(list(dir_path.rglob('*'))) if dir_path.exists() else 0
    except Exception:
        return 0

def get_directory_size(directory: str) -> int:
    """
    Calculate total size of directory in bytes
    
    Args:
        directory: Path to directory
        
    Returns:
        int: Total size in bytes
    """
    try:
        dir_path = Path(directory)
        return sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
    except Exception:
        return 0

def read_lines_from_file(filepath: str) -> List[str]:
    """
    Read all non-empty lines from a text file
    
    Args:
        filepath: Path to text file
        
    Returns:
        List[str]: List of non-empty lines
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except Exception:
        return []

def generate_backup_filename(base_name: str, extension: str = "txt") -> str:
    """
    Generate backup filename with timestamp
    
    Args:
        base_name: Base name for backup file
        extension: File extension (without dot)
        
    Returns:
        str: Backup filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}-{timestamp}.{extension}"

def sleep_with_message(seconds: float, message: str = ""):
    """
    Sleep for specified seconds with optional message
    
    Args:
        seconds: Duration to sleep
        message: Optional message to display
    """
    if message:
        print(f"{message} (waiting {seconds}s...)")
    time.sleep(seconds)
