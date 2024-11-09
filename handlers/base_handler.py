from helpers.configs import Settings, get_settings
from dataclasses import dataclass, field
from datetime import datetime

import os


@dataclass
class BaseHandler:
    
    app_settings: Settings = field(default_factory=get_settings)
    base_files_path: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'assets'
    )

    @staticmethod
    def generate_unique_file_name(orig_file_name: str) -> str:
        """Generate unique string to name the file"""
        now = datetime.now()
        datetime_str = now.strftime('%Y%m%d%H%M%S')
        base, ext = os.path.splitext(orig_file_name)
        unique_file_name = f'{base}-{datetime_str}{ext}'
        return unique_file_name
    