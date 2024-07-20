from helpers.configs import Settings, get_settings
from dataclasses import dataclass, field

import os


@dataclass
class BaseHandler:
    
    app_settings: Settings = field(default_factory=get_settings)
    base_files_path: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'assets'
    )
