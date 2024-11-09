from helpers.configs import get_settings, Settings
from helpers.messages import Message
from handlers.base_handler import BaseHandler

from fastapi import UploadFile, File, Depends, HTTPException, status
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel
from dataclasses import dataclass
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.text_splitter import TextSplitter
from langchain.docstore.document import Document

import os


@dataclass
class FileMetadata:
    file_name: str
    chunk_size: Optional[int] = 200
    overlap_size: Optional[int] = 20


class FileHandler(BaseHandler):

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
                detail=Message.FILE_SIZE_EXCEEDED.format(file_size=max_file_size / (1024 * 1024))
            )
        file.file.seek(0)

        # Check file type
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                detail=Message.FILE_TYPE_NOT_SUPPORTED.format(file_type=file.content_type)
            )

        return file
    
    
    def load_file(self, file_name: str) -> List:   # were FileLoader
        """Get file loader based on the file extension"""
        file_ext = os.path.splitext(file_name)[1]
        file_path = os.path.join(self.base_files_path, file_name)
        
        # check path exists
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Message.FILE_NOT_EXISTS.format(file_name=file_metadata.file_name)
                }
            )
        
        if file_ext == '.txt':
            return TextLoader(file_path).load()
        elif file_ext == '.pdf':
            return PyMuPDFLoader(file_path).load()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=Message.FILE_EXT_NOT_SUPPORTED.format(file_extension=file_ext))
            
    
    def split_text_to_chunks(self, file_content: List[Dict], chunk_size: int, overlap_size: int):
        """Split the extracted text into chunks for storing and processing"""
        
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )
        
        chunks_serialized = [{
            "page_content": chunk.page_content, 
            "metadata": chunk.metadata
        } for chunk in chunks]

        return chunks_serialized