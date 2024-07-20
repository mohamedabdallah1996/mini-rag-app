from helpers.configs import get_settings, Settings
from helpers.messages import Message
from handlers.base_handler import BaseHandler

from fastapi import UploadFile, File, Depends, HTTPException, status
from datetime import datetime
from typing import List

import os


class DataHandler(BaseHandler):

    async def validate_file(
        self,
        file: UploadFile = File(...),  
    ):
        
        max_file_size = self.app_settings.FILE_MAX_SIZE_MB * 1024 * 1024  
        allowed_types = self.app_settings.FILE_ALLOWED_TYPES

        # check file size
        file_size = await file.read()
        if len(file_size) > max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, 
                # detail=f"File size exceeds {max_file_size / (1024 * 1024)} MB limit")
                detail=Message.FILE_SIZE_EXCEEDED.format(file_size=max_file_size / (1024 * 1024))
            )
        file.file.seek(0)

        # Check file type
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                # detail=f"Invalid file type: {file.content_type}"
                detail=Message.FILE_TYPE_NOT_SUPPORTED.format(file_type=file.content_type)
            )

        return file
    
    def generate_unique_file_name(
        self,
        orig_file_name: str
    ) -> str:
        
        now = datetime.now()
        datetime_str = now.strftime('%Y%m%d%H%M%S')
        base, ext = os.path.splitext(orig_file_name)
        unique_file_name = f'{base}-{datetime_str}{ext}'
        return unique_file_name