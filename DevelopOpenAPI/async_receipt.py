import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse

app = FastAPI()

response_items = {"status": "", "message": "", "time": ""}

class ReceiptBody(BaseModel):
    userid: str
    password: str


class ReceiptItem(BaseModel):
    TargetURI: str
    TargetJSONBody: ReceiptBody


@app.get("/")
def root_response():
    return {"What": "are you looking at?"}


@app.post("/acceptcall")
def accept_call(Item: ReceiptItem):
    response_items["status"] = "S202"
    response_items["message"] = "ACCEPTED"
    # time = datetime.now().isoformat(timespec="seconds")
    response_items["time"] = datetime.now().isoformat()
    # ToDo: Implement trigger of proxy execution API

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response_items)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8080)
