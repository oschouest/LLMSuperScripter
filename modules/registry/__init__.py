"""
Registry Operations Module

Safe Windows Registry manipulation with automatic backup and rollback capabilities.
"""

import os
import sys
import json
import datetime
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Windows-specific imports (will be conditional)
if sys.platform == "win32":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None

class RegistryManager:
    """Windows Registry operations with safety features"""
    
    def __init__(self, backup_dir: str = None):
        self.logger = logging.getLogger(__name__)
        self.backup_dir = Path(backup_dir or "backups/registry")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        if sys.platform != "win32":
            self.logger.warning("Registry operations only available on Windows")
            self.available = False
        elif winreg is None:
            self.logger.error("winreg module not available")
            self.available = False
        else:
            self.available = True
    
    def create_backup(self, key_path: str) -> str:
        """Create registry backup before modifications"""
        if not self.available:
            raise RuntimeError("Registry operations not available on this platform")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"registry_backup_{timestamp}.reg"
        
        try:
            # Export registry key to .reg file
            cmd = f'reg export "{key_path}" "{backup_file}" /y'
            result = os.system(cmd)
            
            if result == 0:
                self.logger.info(f"Registry backup created: {backup_file}")
                return str(backup_file)
            else:
                raise RuntimeError(f"Failed to create registry backup: {result}")
                
        except Exception as e:
            self.logger.error(f"Backup creation failed: {e}")
            raise
    
    def restore_backup(self, backup_file: str) -> bool:
        """Restore registry from backup file"""
        if not self.available:
            raise RuntimeError("Registry operations not available on this platform")
        
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
        try:
            # Import registry from .reg file
            cmd = f'reg import "{backup_file}"'
            result = os.system(cmd)
            
            if result == 0:
                self.logger.info(f"Registry restored from: {backup_file}")
                return True
            else:
                self.logger.error(f"Failed to restore registry: {result}")
                return False
                
        except Exception as e:
            self.logger.error(f"Registry restore failed: {e}")
            return False
    
    def read_value(self, key_path: str, value_name: str) -> Any:
        """Read registry value safely"""
        if not self.available:
            raise RuntimeError("Registry operations not available on this platform")
        
        try:
            # Parse key path
            parts = key_path.split('\\', 1)
            root_key = getattr(winreg, parts[0])
            sub_key = parts[1] if len(parts) > 1 else ""
            
            with winreg.OpenKey(root_key, sub_key) as key:
                value, reg_type = winreg.QueryValueEx(key, value_name)
                self.logger.info(f"Read registry value: {key_path}\\{value_name} = {value}")
                return value
                
        except FileNotFoundError:
            self.logger.warning(f"Registry key not found: {key_path}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to read registry value: {e}")
            raise
    
    def write_value(self, key_path: str, value_name: str, value: Any, reg_type: int = winreg.REG_SZ) -> bool:
        """Write registry value with backup"""
        if not self.available:
            raise RuntimeError("Registry operations not available on this platform")
        
        # Create backup before modification
        backup_file = self.create_backup(key_path)
        
        try:
            # Parse key path
            parts = key_path.split('\\', 1)
            root_key = getattr(winreg, parts[0])
            sub_key = parts[1] if len(parts) > 1 else ""
            
            with winreg.CreateKey(root_key, sub_key) as key:
                winreg.SetValueEx(key, value_name, 0, reg_type, value)
                self.logger.info(f"Registry value written: {key_path}\\{value_name} = {value}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to write registry value: {e}")
            # Attempt to restore backup
            self.logger.info("Attempting to restore from backup...")
            self.restore_backup(backup_file)
            raise
    
    def delete_value(self, key_path: str, value_name: str) -> bool:
        """Delete registry value with backup"""
        if not self.available:
            raise RuntimeError("Registry operations not available on this platform")
        
        # Create backup before modification
        backup_file = self.create_backup(key_path)
        
        try:
            # Parse key path
            parts = key_path.split('\\', 1)
            root_key = getattr(winreg, parts[0])
            sub_key = parts[1] if len(parts) > 1 else ""
            
            with winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, value_name)
                self.logger.info(f"Registry value deleted: {key_path}\\{value_name}")
                return True
                
        except FileNotFoundError:
            self.logger.warning(f"Registry value not found: {key_path}\\{value_name}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete registry value: {e}")
            # Attempt to restore backup
            self.logger.info("Attempting to restore from backup...")
            self.restore_backup(backup_file)
            raise
    
    def list_backups(self) -> List[Dict[str, str]]:
        """List available registry backups"""
        backups = []
        
        for backup_file in self.backup_dir.glob("registry_backup_*.reg"):
            stat = backup_file.stat()
            backups.append({
                "file": str(backup_file),
                "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "size": stat.st_size
            })
        
        return sorted(backups, key=lambda x: x["created"], reverse=True)

# Common registry operations
class CommonRegistryOperations:
    """Pre-defined safe registry operations"""
    
    def __init__(self, registry_manager: RegistryManager):
        self.registry = registry_manager
        self.logger = logging.getLogger(__name__)
    
    def enable_developer_mode(self) -> bool:
        """Enable Windows Developer Mode"""
        key_path = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppModelUnlock"
        
        try:
            # Enable developer mode
            self.registry.write_value(key_path, "AllowDevelopmentWithoutDevLicense", 1, winreg.REG_DWORD)
            self.registry.write_value(key_path, "AllowAllTrustedApps", 1, winreg.REG_DWORD)
            
            self.logger.info("Developer mode enabled successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to enable developer mode: {e}")
            return False
    
    def set_power_settings(self, scheme: str = "high_performance") -> bool:
        """Configure power management settings"""
        # This would typically use powercfg commands rather than direct registry
        self.logger.info(f"Setting power scheme to: {scheme}")
        
        schemes = {
            "high_performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
            "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
            "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a"
        }
        
        if scheme not in schemes:
            raise ValueError(f"Unknown power scheme: {scheme}")
        
        try:
            cmd = f"powercfg /setactive {schemes[scheme]}"
            result = os.system(cmd)
            return result == 0
        except Exception as e:
            self.logger.error(f"Failed to set power scheme: {e}")
            return False

def create_registry_manager(backup_dir: str = None) -> RegistryManager:
    """Factory function to create registry manager"""
    return RegistryManager(backup_dir)
