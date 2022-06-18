import json
import uvicorn
import requests
import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AsyncExecute(BaseModel):
    URI: str
    RequestBody: object
    Method: str

@app.post("/destinationasync")
async def execute_TargetAPI(asynctarget: AsyncExecute):
    ut = time.time()
    base_url = asynctarget.URI
    requestbody = asynctarget.RequestBody
    wait_time = 100

    if asynctarget.Method == "GET":
        time.sleep(wait_time)
        if asynctarget.RequestBody == None:
            response = requests.get(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody != None:
            response = requests.get(base_url, json=requestbody)
            data = json.loads(response.text)
    elif asynctarget.Method == "POST":
        time.sleep(wait_time)
        if asynctarget.RequestBody == None:
            response = requests.post(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody != None:
            response = requests.post(base_url, json=requestbody)
            data = json.loads(response.text)
    elif asynctarget.Method == "PUT":
        time.sleep(wait_time)
        if asynctarget.RequestBody == None:
            response = requests.put(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody != None:
            response = requests.put(base_url, json=requestbody)
            data = json.loads(response.text)
    elif asynctarget.Method == "DELETE":
        time.sleep(wait_time)
        if asynctarget.RequestBody == None:
            response = requests.delete(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody != None:
            response = requests.delete(base_url, json=requestbody)
            data = json.loads(response.text)

    async_Return = {
        "status": "ok",
        "message": "Accepted",
        "RequestURI": base_url,
        "RequestBody": requestbody,
        "Method": asynctarget.Method,
        "timestamp": ut
    }
    return async_Return

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)