from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse 
from typing import List

from helpers.configs import Settings, get_settings
from helpers.logger import logger
from helpers.messages import Message
from handlers import DataHandler

import os
import aiofiles


data_router = APIRouter(
    prefix='/api/v1/data',
    tags=['api_v1', 'data']
)

data_handler = DataHandler()

@data_router.post('/upload/')
async def upload_file(
    file: UploadFile = Depends(data_handler.validate_file),
    app_settings: Settings = Depends(get_settings)
) -> JSONResponse:
    
    # determine file path to write
    file_name = data_handler.generate_unique_file_name(file.filename)
    file_path = os.path.join(data_handler.base_files_path, file_name)
    logger.info(f'Writing {file_path} on disk ..')
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE_BYTES):
                await f.write(chunk)
    except Exception as e:

        logger.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "result": Message.FILE_UPLOAD_FAILED.format(file_name=file.filename)
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "result": Message.FILE_UPLOAD_SUCCESS.format(file_name=file.filename)
        }
    )
        
    