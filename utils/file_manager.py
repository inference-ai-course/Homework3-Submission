"""
File Management Utilities
"""
import os
import uuid
import asyncio
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
from config.settings import settings
from utils.logger import logger


class FileManager:
    """Manage temporary audio files"""
    
    def __init__(self):
        self.temp_dir = settings.get_temp_dir_path()
        self.cleanup_interval = 3600  # 1 hour
        self.file_ttl = 7200  # 2 hours
    
    def generate_unique_filename(self, extension: str = ".mp3") -> str:
        """
        Generate a unique filename
        
        Args:
            extension: File extension (e.g., '.mp3', '.wav')
            
        Returns:
            Unique filename
        """
        unique_id = uuid.uuid4().hex[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{unique_id}{extension}"
    
    def get_temp_filepath(self, filename: str) -> Path:
        """
        Get full path for a temp file
        
        Args:
            filename: Name of the file
            
        Returns:
            Full path to the file
        """
        return self.temp_dir / filename
    
    async def save_uploaded_file(self, file_bytes: bytes, filename: Optional[str] = None) -> Path:
        """
        Save uploaded file to temp directory
        
        Args:
            file_bytes: File content
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = self.generate_unique_filename(".wav")
        
        filepath = self.get_temp_filepath(filename)
        
        # Write file asynchronously
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._write_file,
            filepath,
            file_bytes
        )
        
        logger.info(f"Saved file: {filepath}")
        return filepath
    
    def _write_file(self, filepath: Path, content: bytes):
        """Synchronous file write"""
        with open(filepath, "wb") as f:
            f.write(content)
    
    def delete_file(self, filepath: Path) -> bool:
        """
        Delete a file
        
        Args:
            filepath: Path to file
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            if filepath.exists():
                filepath.unlink()
                logger.debug(f"Deleted file: {filepath}")
                return True
        except Exception as e:
            logger.error(f"Failed to delete file {filepath}: {e}")
        return False
    
    def cleanup_old_files(self):
        """Remove files older than TTL"""
        try:
            cutoff_time = datetime.now() - timedelta(seconds=self.file_ttl)
            deleted_count = 0
            
            for file_path in self.temp_dir.glob("*"):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_time:
                        if self.delete_file(file_path):
                            deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old temp files")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    async def start_cleanup_task(self):
        """Start background cleanup task"""
        while True:
            await asyncio.sleep(self.cleanup_interval)
            self.cleanup_old_files()


# Global file manager instance
file_manager = FileManager()
