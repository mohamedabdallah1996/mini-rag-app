# mini-RAG-app

This is a minimal implementation of the RAG model for question answering.

## Requirements
- Python 3.8 or later

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run the FastAPI server

The default way to run the FastAPI app using `uvicorn` 

```bash
$ uvicorn app:app 
```

- First `app` refers to the Python module name that contains your FastAPI application. 
- Second `app` is the ASGI application instance inside the specified module. 

### (Optional) Add more details to the run

- `--reload` - To allow the app to refresh automatically with any change you made.
- `--host 0.0.0.0` - To let every one outside your server to access this API.
- `--port` - To change the port where you want to run the app, default is `8000`.