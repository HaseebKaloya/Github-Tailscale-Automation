"""
Recovery utilities for Github&Tailscale-Automation
Author: Haseeb Kaloya

Provides error recovery and resumption capabilities
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from utils.logger import get_logger

class RecoveryManager:
    """Manages error recovery and resumption"""
    
    def __init__(self):
        self.logger = get_logger()
        self.recovery_dir = Path(__file__).parent.parent / "recovery"
        self.recovery_dir.mkdir(exist_ok=True)
    
    def save_progress_state(self, session_id: str, state: Dict[str, Any]) -> bool:
        """
        Save current progress state for recovery
        
        Args:
            session_id: Unique session identifier
            state: Current state to save
            
        Returns:
            bool: Success status
        """
        try:
            state_file = self.recovery_dir / f"session_{session_id}.json"
            
            # Add timestamp
            state['timestamp'] = datetime.now().isoformat()
            state['session_id'] = session_id
            
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            self.logger.info(f"Progress state saved: {state_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save progress state: {e}")
            return False
    
    def load_progress_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load saved progress state
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict or None: Loaded state or None if not found
        """
        try:
            state_file = self.recovery_dir / f"session_{session_id}.json"
            
            if not state_file.exists():
                return None
            
            with open(state_file, 'r') as f:
                state = json.load(f)
            
            self.logger.info(f"Progress state loaded: {state_file}")
            return state
            
        except Exception as e:
            self.logger.error(f"Failed to load progress state: {e}")
            return None
    
    def get_failed_repositories(self, session_id: str) -> List[str]:
        """
        Get list of repositories that failed in previous session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of failed repository names
        """
        state = self.load_progress_state(session_id)
        if state:
            return state.get('failed_repos', [])
        return []
    
    def cleanup_old_sessions(self, days_old: int = 7) -> int:
        """
        Clean up old recovery files
        
        Args:
            days_old: Remove files older than this many days
            
        Returns:
            Number of files cleaned up
        """
        cleaned = 0
        try:
            cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            
            for file_path in self.recovery_dir.glob("session_*.json"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    cleaned += 1
            
            self.logger.info(f"Cleaned up {cleaned} old recovery files")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up recovery files: {e}")
        
        return cleaned

class RetryManager:
    """Manages retry logic for failed operations"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.logger = get_logger()
    
    def retry_with_backoff(self, func, *args, **kwargs):
        """
        Retry function with exponential backoff
        
        Args:
            func: Function to retry
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or raises last exception
        """
        import time
        import random
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries - 1:
                    # Calculate backoff delay with jitter
                    delay = (self.base_delay * (2 ** attempt)) + random.uniform(0, 1)
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                else:
                    self.logger.error(f"All retry attempts failed. Last error: {e}")
        
        raise last_exception
