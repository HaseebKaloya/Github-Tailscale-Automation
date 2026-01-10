"""
Tailscale API Integration for Github&Tailscale-Automation
Author: Haseeb Kaloya
Email: haseebkaloya@gmail.com

Handles Tailscale auth key generation via API
"""

import requests
import time
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from utils.logger import get_logger
from utils.helpers import generate_backup_filename
from core.constants import (
    TAILSCALE_KEY_EXPIRY_DAYS,
    TAILSCALE_API_BASE_URL,
    API_RATE_LIMIT_DELAY
)

class TailscaleAPI:
    """Tailscale API wrapper for auth key generation"""
    
    def __init__(self, api_key: str, tailnet: str):
        """
        Initialize Tailscale API client
        
        Args:
            api_key: Tailscale API key
            tailnet: Tailscale network name
        """
        self.api_key = api_key
        self.tailnet = tailnet
        self.base_url = f"{TAILSCALE_API_BASE_URL}/tailnet/{tailnet}"
        self.logger = get_logger()
        
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_auth_key(self,
                         expiry_days: int = TAILSCALE_KEY_EXPIRY_DAYS,
                         reusable: bool = True,
                         ephemeral: bool = False,
                         preauthorized: bool = True,
                         tags: Optional[List[str]] = None) -> Tuple[bool, str]:
        """
        Generate a single Tailscale auth key
        
        Args:
            expiry_days: Number of days until key expires
            reusable: Allow key to be used multiple times
            ephemeral: Create ephemeral node
            preauthorized: Pre-authorize the key
            tags: List of tags to apply
            
        Returns:
            Tuple[bool, str]: (success, auth_key or error_message)
        """
        try:
            self.logger.info("Generating Tailscale auth key...")
            
            # Prepare payload
            payload = {
                "capabilities": {
                    "devices": {
                        "create": {
                            "reusable": reusable,
                            "ephemeral": ephemeral,
                            "preauthorized": preauthorized
                        }
                    }
                },
                "expirySeconds": expiry_days * 24 * 3600
            }
            
            # Add tags if provided
            if tags:
                payload["capabilities"]["devices"]["create"]["tags"] = tags
            
            # Make API request
            url = f"{self.base_url}/keys"
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                key = response.json().get('key', '')
                self.logger.info("Auth key generated successfully")
                time.sleep(API_RATE_LIMIT_DELAY)
                return True, key
            else:
                error_msg = f"API error: {response.json().get('message', 'Unknown error')}"
                self.logger.error(error_msg)
                return False, error_msg
                
        except requests.exceptions.Timeout:
            error_msg = "Request timeout - Tailscale API not responding"
            self.logger.error(error_msg)
            return False, error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def generate_multiple_keys(self,
                              count: int,
                              expiry_days: int = TAILSCALE_KEY_EXPIRY_DAYS,
                              reusable: bool = True,
                              ephemeral: bool = False,
                              progress_callback=None) -> Tuple[bool, List[str], str]:
        """
        Generate multiple Tailscale auth keys
        
        Args:
            count: Number of keys to generate
            expiry_days: Number of days until keys expire
            reusable: Allow keys to be used multiple times
            ephemeral: Create ephemeral nodes
            progress_callback: Optional callback function(current, total, message)
            
        Returns:
            Tuple[bool, List[str], str]: (success, list_of_keys, error_message)
        """
        try:
            self.logger.info(f"Generating {count} Tailscale auth keys...")
            
            keys = []
            failed_count = 0
            
            for i in range(count):
                # Update progress
                if progress_callback:
                    progress_callback(i + 1, count, f"Generating key {i + 1} of {count}")
                
                success, result = self.generate_auth_key(
                    expiry_days=expiry_days,
                    reusable=reusable,
                    ephemeral=ephemeral,
                    preauthorized=True,
                    tags=None  # Remove invalid tags that cause permission errors
                )
                
                if success:
                    keys.append(result)
                else:
                    failed_count += 1
                    self.logger.warning(f"Failed to generate key {i + 1}: {result}")
            
            if keys:
                self.logger.info(f"Generated {len(keys)} auth keys ({failed_count} failed)")
                return True, keys, ""
            else:
                error_msg = f"Failed to generate any keys (all {count} attempts failed)"
                self.logger.error(error_msg)
                return False, [], error_msg
                
        except Exception as e:
            error_msg = f"Unexpected error generating keys: {str(e)}"
            self.logger.error(error_msg)
            return False, [], error_msg
    
    def save_keys_to_file(self,
                         keys: List[str],
                         backup_dir: str = "backups") -> Tuple[bool, str]:
        """
        Save generated keys to a backup file
        
        Args:
            keys: List of auth keys
            backup_dir: Directory to save backup file
            
        Returns:
            Tuple[bool, str]: (success, filepath or error_message)
        """
        try:
            # Create backup directory
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            # Generate filename with timestamp
            filename = generate_backup_filename("tailscale-keys", "txt")
            filepath = backup_path / filename
            
            # Write keys to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Tailscale Auth Keys\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total Keys: {len(keys)}\n")
                f.write(f"# Expiry: {TAILSCALE_KEY_EXPIRY_DAYS} days\n\n")
                
                for i, key in enumerate(keys, 1):
                    f.write(f"{key}\n")
            
            self.logger.info(f"Keys saved to: {filepath}")
            return True, str(filepath)
            
        except Exception as e:
            error_msg = f"Failed to save keys: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test Tailscale API connection
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            self.logger.info("Testing Tailscale API connection...")
            
            # Try to list keys (read-only operation)
            url = f"{self.base_url}/keys"
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Connection successful"
            else:
                error_msg = f"API error: {response.json().get('message', 'Connection failed')}"
                return False, error_msg
                
        except requests.exceptions.Timeout:
            return False, "Request timeout - Tailscale API not responding"
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def list_existing_keys(self) -> Tuple[bool, List[Dict[str, Any]], str]:
        """
        List existing auth keys
        
        Returns:
            Tuple[bool, List[Dict], str]: (success, keys_list, error_message)
        """
        try:
            url = f"{self.base_url}/keys"
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                keys = response.json().get('keys', [])
                return True, keys, ""
            else:
                error_msg = f"Failed to list keys: {response.json().get('message', 'Unknown error')}"
                return False, [], error_msg
                
        except Exception as e:
            error_msg = f"Error listing keys: {str(e)}"
            return False, [], error_msg
    
    def delete_key(self, key_id: str) -> Tuple[bool, str]:
        """
        Delete an auth key
        
        Args:
            key_id: Key ID to delete
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            url = f"{self.base_url}/keys/{key_id}"
            response = requests.delete(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"Key deleted: {key_id}")
                return True, ""
            else:
                error_msg = f"Failed to delete key: {response.json().get('message', 'Unknown error')}"
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error deleting key: {str(e)}"
            return False, error_msg
