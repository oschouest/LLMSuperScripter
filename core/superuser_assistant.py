#!/usr/bin/env python3
"""
LLM Super User Assistant - Core Engine
"""

import os
import sys
import json
import subprocess
import shutil
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

class SuperUserAssistant:
    def __init__(self):
        self.backup_dir = Path.home() / ".superuser-backups"
        self.log_file = Path.home() / ".superuser.log"
        self.setup_logging()
        self.ensure_backup_dir()
        
    def setup_logging(self):
        """Setup comprehensive logging for all operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def ensure_backup_dir(self):
        """Ensure backup directory exists"""
        self.backup_dir.mkdir(exist_ok=True)
        self.logger.info(f"Backup directory: {self.backup_dir}")
        
    def create_system_snapshot(self, operation_name: str) -> str:
        """Create a system snapshot before any operation"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"{operation_name}_{timestamp}"
        snapshot_dir = self.backup_dir / snapshot_id
        snapshot_dir.mkdir(exist_ok=True)
        
        self.logger.info(f"Creating system snapshot: {snapshot_id}")
        
        # Backup registry (Windows)
        if os.name == 'nt':
            try:
                reg_backup = snapshot_dir / "registry_backup.reg"
                subprocess.run([
                    "reg", "export", "HKEY_CURRENT_USER", str(reg_backup)
                ], check=True, capture_output=True)
                self.logger.info("Registry backup created")
            except subprocess.CalledProcessError as e:
                self.logger.warning(f"Registry backup failed: {e}")
                
        # Backup important configs
        config_files = [
            Path.home() / ".bashrc",
            Path.home() / ".ssh" / "config",
            Path("/etc/hosts") if os.path.exists("/etc/hosts") else None
        ]
        
        for config_file in config_files:
            if config_file and config_file.exists():
                try:
                    shutil.copy2(config_file, snapshot_dir / config_file.name)
                    self.logger.info(f"Backed up: {config_file}")
                except Exception as e:
                    self.logger.warning(f"Failed to backup {config_file}: {e}")
                    
        # Save snapshot metadata
        metadata = {
            "snapshot_id": snapshot_id,
            "timestamp": timestamp,
            "operation": operation_name,
            "system": os.name,
            "user": os.getenv("USER") or os.getenv("USERNAME"),
            "cwd": str(Path.cwd())
        }
        
        with open(snapshot_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
        return snapshot_id
        
    def rollback_snapshot(self, snapshot_id: str) -> bool:
        """Rollback to a previous snapshot"""
        snapshot_dir = self.backup_dir / snapshot_id
        if not snapshot_dir.exists():
            self.logger.error(f"Snapshot not found: {snapshot_id}")
            return False
            
        self.logger.info(f"Rolling back to snapshot: {snapshot_id}")
        
        # Restore registry (Windows)
        if os.name == 'nt':
            reg_backup = snapshot_dir / "registry_backup.reg"
            if reg_backup.exists():
                try:
                    subprocess.run([
                        "reg", "import", str(reg_backup)
                    ], check=True)
                    self.logger.info("Registry restored")
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Registry restore failed: {e}")
                    return False
                    
        # Restore config files
        for backup_file in snapshot_dir.glob("*"):
            if backup_file.name in ["metadata.json", "registry_backup.reg"]:
                continue
                
            # Determine original location
            if backup_file.name in [".bashrc", "config"]:
                if backup_file.name == "config":
                    original = Path.home() / ".ssh" / "config"
                else:
                    original = Path.home() / backup_file.name
            elif backup_file.name == "hosts":
                original = Path("/etc/hosts")
            else:
                continue
                
            try:
                shutil.copy2(backup_file, original)
                self.logger.info(f"Restored: {original}")
            except Exception as e:
                self.logger.error(f"Failed to restore {original}: {e}")
                
        return True
        
    def safe_execute(self, command: str, operation_name: str, 
                    require_admin: bool = False) -> Tuple[bool, str, str]:
        """Safely execute a command with backup and validation"""
        
        # Create snapshot before execution
        snapshot_id = self.create_system_snapshot(operation_name)
        
        try:
            # Ask for user confirmation
            print(f"\n🤖 LLM Super User Assistant")
            print(f"📋 Operation: {operation_name}")
            print(f"💻 Command: {command}")
            print(f"🛡️ Snapshot: {snapshot_id}")
            
            if require_admin:
                print("⚠️  This operation requires administrative privileges")
                
            response = input("\n✅ Execute this operation? (yes/no): ").lower()
            if response not in ['yes', 'y']:
                print("❌ Operation cancelled by user")
                return False, "", "Operation cancelled"
                
            # Execute command
            self.logger.info(f"Executing: {command}")
            
            if require_admin and os.name == 'nt':
                # Windows: Use powershell with admin
                ps_command = f"Start-Process powershell -Verb RunAs -ArgumentList '-Command', '{command}'"
                result = subprocess.run([
                    "powershell", "-Command", ps_command
                ], capture_output=True, text=True, timeout=300)
            else:
                # Standard execution
                result = subprocess.run(
                    command, shell=True, capture_output=True, 
                    text=True, timeout=300
                )
                
            success = result.returncode == 0
            
            if success:
                self.logger.info(f"✅ Operation completed successfully")
                print(f"\n✅ Operation completed successfully!")
                if result.stdout:
                    print(f"📤 Output:\n{result.stdout}")
            else:
                self.logger.error(f"❌ Operation failed: {result.stderr}")
                print(f"\n❌ Operation failed!")
                print(f"🔥 Error: {result.stderr}")
                
                # Ask if user wants to rollback
                rollback = input("\n🔄 Rollback changes? (yes/no): ").lower()
                if rollback in ['yes', 'y']:
                    if self.rollback_snapshot(snapshot_id):
                        print("✅ Successfully rolled back changes")
                    else:
                        print("❌ Rollback failed - check logs")
                        
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            self.logger.error("Command timed out")
            return False, "", "Command timed out"
        except Exception as e:
            self.logger.error(f"Execution failed: {e}")
            return False, "", str(e)
            
    def list_snapshots(self) -> List[Dict]:
        """List all available snapshots"""
        snapshots = []
        for snapshot_dir in self.backup_dir.iterdir():
            if snapshot_dir.is_dir():
                metadata_file = snapshot_dir / "metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            snapshots.append(metadata)
                    except Exception as e:
                        self.logger.warning(f"Failed to read metadata for {snapshot_dir}: {e}")
        return sorted(snapshots, key=lambda x: x['timestamp'], reverse=True)

def main():
    assistant = SuperUserAssistant()
    
    print("🤖 LLM Super User Assistant v1.0")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage examples:")
        print("  python superuser.py --command 'echo Hello World' --operation 'test'")
        print("  python superuser.py --snapshots")
        print("  python superuser.py --rollback <snapshot_id>")
        return
        
    if "--snapshots" in sys.argv:
        snapshots = assistant.list_snapshots()
        print(f"\n📸 Available snapshots ({len(snapshots)}):")
        for snapshot in snapshots:
            print(f"  🔹 {snapshot['snapshot_id']} - {snapshot['operation']} ({snapshot['timestamp']})")
        return
        
    if "--rollback" in sys.argv:
        idx = sys.argv.index("--rollback")
        if idx + 1 < len(sys.argv):
            snapshot_id = sys.argv[idx + 1]
            if assistant.rollback_snapshot(snapshot_id):
                print("✅ Rollback completed")
            else:
                print("❌ Rollback failed")
        return
        
    # Execute command
    command = None
    operation = "manual_command"
    require_admin = "--admin" in sys.argv
    
    if "--command" in sys.argv:
        idx = sys.argv.index("--command")
        if idx + 1 < len(sys.argv):
            command = sys.argv[idx + 1]
            
    if "--operation" in sys.argv:
        idx = sys.argv.index("--operation")
        if idx + 1 < len(sys.argv):
            operation = sys.argv[idx + 1]
            
    if command:
        assistant.safe_execute(command, operation, require_admin)
    else:
        print("❌ No command specified")

if __name__ == "__main__":
    main()
