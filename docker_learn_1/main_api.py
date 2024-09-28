import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import logging
from weaviate_query_add import VectorMain

my_app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager to initialize application state during startup.
    This context manager loads the ML model and initializes the `RoutingMain` instance.
    """

    config_file= "/mnt/e/win_python/vector_api/config_file.json"
    
    my_app_state["WeaviateAPI"] = VectorMain(collection_name="API_test_2", 
                                             model_name= "/mnt/gte-large-en-v1.5")
    
    yield

app = FastAPI(lifespan=lifespan)

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


#############################Insert API ############################################
class RequestInputDataPayload(BaseModel):
    """
    Model to define the structure of the input payload for process_query endpoint.
    """
    input_json: list
    session_id: str

class ResponseInputDataPayload(BaseModel):
    """
    Model to define the structure of the input payload for process_query endpoint.
    """
    Counter_value: str
    session_id : str

@app.post("/input_query")
async def process_query(payload: RequestInputDataPayload):
    input_json = payload.input_json
    session_id = payload.session_id
    value = my_app_state["WeaviateAPI"].insert_data(input_json)
    return ResponseInputDataPayload(Counter_value=value, session_id=session_id)


#############################Vector Query API ############################################
class RequestSearchPayload(BaseModel):
    """
    Model to define the structure of the input payload for process_query endpoint.
    """
    query : str
    session_id: str

class OutputQueryPayload(BaseModel):
    """
    Model to define the structure of the input payload for process_query endpoint.
    """
    response : list
   

@app.post("/search_query")
async def process_query(payload: RequestSearchPayload):
    query = payload.query
    session_id = payload.session_id
    query_response = my_app_state["WeaviateAPI"].db_query_data(query=query)
    return OutputQueryPayload(response=query_response,session_id=session_id)



if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    uvicorn.run("main_api:app", host="0.0.0.0", port=8050, reload=False)


