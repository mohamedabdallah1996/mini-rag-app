from enum import Enum 

class Message(Enum):
     
    FILE_TYPE_NOT_SUPPORTED = "File type {file_type} is not supported!"
    FILE_EXT_NOT_SUPPORTED = "File extension `{file_extension}` is not supported!"
    FILE_SIZE_EXCEEDED = "File size exceeds {default_file_size} MB limit"
    FILE_UPLOAD_SUCCESS = "File {file_name} uploaded successfully"
    FILE_UPLOAD_FAILED = "File {file_name} upload failed!"
    FILE_PROCESSING_SUCCESS = "File {file_name} processed successfully!"
    FILE_PROCESSING_FAILED = "File {file_name} processing failed!"
    FILE_NOT_EXISTS = "File {file_name} is not exists! please make sure you uploaded it successfully."
    
    def format(self, **kwargs):
        return self.value.format(**kwargs) 