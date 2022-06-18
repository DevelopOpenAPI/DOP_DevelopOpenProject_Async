import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse
import time
import json
import requests

app = FastAPI()

response_items = {"status": "", "message": "", "time": ""}


class ReceiptBody(BaseModel):
    userid: str
    password: str


class ReceiptItem(BaseModel):
    TargetURI: str
    TargetJSONBody: ReceiptBody
    Method: str


class AsyncExecute(BaseModel):
    URI: str
    RequestBody: ReceiptBody
    Method: str


@app.get("/")
async def root_response():
    return {"What": "are you looking at?"}


@app.post("/acceptcall")
async def accept_call(Item: ReceiptItem):
    response_items["status"] = "S202"
    response_items["message"] = "ACCEPTED"
    response_items["time"] = datetime.now().isoformat()
    # implement type 1: await function
    target_body = AsyncExecute(
        URI=Item.TargetURI,
        RequestBody = Item.TargetJSONBody,
        Method = Item.Method,
    )
    await execute_targetapi(target_body)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response_items)


@app.post("/destinationasync")
async def execute_targetapi(asynctarget: AsyncExecute):
    ut = time.time()
    base_url = asynctarget.URI
    requestbody = asynctarget.RequestBody
    wait_time = 100

    if asynctarget.Method == "GET":
        time.sleep(wait_time)
        if asynctarget.RequestBody is None:
            response = requests.get(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody is not None:
            response = requests.get(base_url, json=requestbody)
            data = json.loads(response.text)
    elif asynctarget.Method == "POST":
        time.sleep(wait_time)
        if asynctarget.RequestBody is None:
            response = requests.post(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody is not None:
            response = requests.post(base_url, json=requestbody)
            data = json.loads(response.text)
    elif asynctarget.Method == "PUT":
        time.sleep(wait_time)
        if asynctarget.RequestBody == None:
            response = requests.put(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody is not None:
            response = requests.put(base_url, json=requestbody)
            data = json.loads(response.text)
    elif asynctarget.Method == "DELETE":
        time.sleep(wait_time)
        if asynctarget.RequestBody is None:
            response = requests.delete(base_url)
            data = json.loads(response.text)
        elif asynctarget.RequestBody is not None:
            response = requests.delete(base_url, json=requestbody)
            data = json.loads(response.text)

    async_return = {
        "status": "ok",
        "message": "Accepted",
        "RequestURI": base_url,
        "RequestBody": requestbody,
        "Method": asynctarget.Method,
        "timestamp": ut
    }
    return async_return


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8080)
