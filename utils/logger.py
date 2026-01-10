"""
Logging utility for Github&Tailscale-Automation
Author: Haseeb Kaloya
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from utils.paths import LOGS_DIR

def setup_logger(name="GithubTailscaleAutomation"):
    """
    Setup application logger
    
    Args:
        name: Logger name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Use centralized logs directory
    log_path = LOGS_DIR
    log_path.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    log_file = log_path / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def get_logger():
    """Get the application logger"""
    return logging.getLogger("GithubTailscaleAutomation")
