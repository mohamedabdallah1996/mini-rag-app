from enum import Enum 

class Message(Enum):
     
    FILE_TYPE_NOT_SUPPORTED = "File type {file_type} is not supported"
    FILE_SIZE_EXCEEDED = "File size exceeds {default_file_size} MB limit"
    FILE_UPLOAD_SUCCESS = "File {file_name} uploaded successfully"
    FILE_UPLOAD_FAILED = "File {file_name} upload failed!"
    
    def format(self, **kwargs):
        return self.value.format(**kwargs) 