from pathlib import Path
import os
import shutil
from datetime import datetime
from typing import Optional, List
import json

class FileManager:
    """Utility class for managing output files in the website builder."""
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the FileManager.
        
        Args:
            output_dir (Optional[str]): Directory to store output files. If None, uses 'output' in current directory.
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / 'output'
        self.backup_dir = self.output_dir / 'backups'
        self.version_dir = self.output_dir / 'versions'
        self._ensure_directories()
        self._load_version_history()
    
    def _ensure_directories(self) -> None:
        """Ensure all necessary directories exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.version_dir.mkdir(parents=True, exist_ok=True)
        # Create subdirectories for different file types
        (self.output_dir / 'html').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'css').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'js').mkdir(parents=True, exist_ok=True)
    
    def _load_version_history(self) -> None:
        """Load version history from JSON file."""
        self.version_file = self.version_dir / 'version_history.json'
        if self.version_file.exists():
            with open(self.version_file, 'r') as f:
                self.version_history = json.load(f)
        else:
            self.version_history = {}
    
    def _save_version_history(self) -> None:
        """Save version history to JSON file."""
        with open(self.version_file, 'w') as f:
            json.dump(self.version_history, f, indent=2)
    
    def get_file_path(self, filename: str) -> Path:
        """
        Get the full path for an output file.
        
        Args:
            filename (str): Name of the file
            
        Returns:
            Path: Full path to the file
        """
        file_path = self.output_dir / filename
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path
    
    def write_file(self, filename: str, content: str, create_backup: bool = True) -> Path:
        """
        Write content to a file in the output directory.
        
        Args:
            filename (str): Name of the file
            content (str): Content to write
            create_backup (bool): Whether to create a backup before writing
            
        Returns:
            Path: Path to the written file
            
        Raises:
            IOError: If there's an error writing the file
        """
        file_path = self.get_file_path(filename)
        
        if create_backup and file_path.exists():
            self.create_backup(filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self._update_version_history(filename, content)
            
            return file_path
        except IOError as e:
            raise IOError(f"Error writing file {filename}: {str(e)}")
    
    def read_file(self, filename: str) -> str:
        """
        Read content from a file in the output directory.
        
        Args:
            filename (str): Name of the file
            
        Returns:
            str: Content of the file
            
        Raises:
            IOError: If there's an error reading the file
        """
        file_path = self.get_file_path(filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Error reading file {filename}: {str(e)}")
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists in the output directory.
        
        Args:
            filename (str): Name of the file
            
        Returns:
            bool: True if file exists, False otherwise
        """
        return self.get_file_path(filename).exists()
    
    def create_backup(self, filename: str) -> Path:
        """
        Create a backup of a file.
        
        Args:
            filename (str): Name of the file to backup
            
        Returns:
            Path: Path to the backup file
            
        Raises:
            IOError: If there's an error creating the backup
        """
        if not self.file_exists(filename):
            return None
            
        source_path = self.get_file_path(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{filename}.{timestamp}.bak"
        backup_path = self.backup_dir / backup_filename
        
        try:
            shutil.copy2(source_path, backup_path)
            return backup_path
        except IOError as e:
            raise IOError(f"Error creating backup for {filename}: {str(e)}")
    
    def restore_backup(self, backup_filename: str) -> Path:
        """
        Restore a file from a backup.
        
        Args:
            backup_filename (str): Name of the backup file
            
        Returns:
            Path: Path to the restored file
            
        Raises:
            IOError: If there's an error restoring the backup
        """
        backup_path = self.backup_dir / backup_filename
        if not backup_path.exists():
            raise IOError(f"Backup file {backup_filename} not found")
            
        original_filename = backup_filename.split('.')[0]
        target_path = self.get_file_path(original_filename)
        
        try:
            shutil.copy2(backup_path, target_path)
            return target_path
        except IOError as e:
            raise IOError(f"Error restoring backup {backup_filename}: {str(e)}")
    
    def list_backups(self, filename: Optional[str] = None) -> List[str]:
        """
        List all backup files or backups for a specific file.
        
        Args:
            filename (Optional[str]): Name of the file to list backups for
            
        Returns:
            List[str]: List of backup filenames
        """
        if filename:
            return [f for f in os.listdir(self.backup_dir) if f.startswith(f"{filename}.")]
        return os.listdir(self.backup_dir)
    
    def _update_version_history(self, filename: str, content: str) -> None:
        """
        Update version history for a file.
        
        Args:
            filename (str): Name of the file
            content (str): Content of the file
        """
        if filename not in self.version_history:
            self.version_history[filename] = []
            
        version = {
            'timestamp': datetime.now().isoformat(),
            'content': content
        }
        self.version_history[filename].append(version)
        self._save_version_history()
    
    def get_file_versions(self, filename: str) -> List[dict]:
        """
        Get version history for a file.
        
        Args:
            filename (str): Name of the file
            
        Returns:
            List[dict]: List of version information
        """
        return self.version_history.get(filename, [])
    
    def restore_version(self, filename: str, version_index: int) -> Path:
        """
        Restore a specific version of a file.
        
        Args:
            filename (str): Name of the file
            version_index (int): Index of the version to restore
            
        Returns:
            Path: Path to the restored file
            
        Raises:
            ValueError: If version index is invalid
        """
        if filename not in self.version_history:
            raise ValueError(f"No version history found for {filename}")
            
        versions = self.version_history[filename]
        if not 0 <= version_index < len(versions):
            raise ValueError(f"Invalid version index: {version_index}")
            
        version = versions[version_index]
        return self.write_file(filename, version['content'], create_backup=False) 