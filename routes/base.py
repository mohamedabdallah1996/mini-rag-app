from fastapi import APIRouter, Depends
from helpers.configs import get_settings, Settings

base_router = APIRouter(
    prefix='/api/v1',
    tags=['api_v1']
)

@base_router.get('/')
def welcome(app_settings: Settings = Depends(get_settings)):
    
    app_name = app_settings.APP_NAME 
    app_version = app_settings.APP_VERSION
    
    return {
        'name': app_name,
        'version': app_version
    }