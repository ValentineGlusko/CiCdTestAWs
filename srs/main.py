import re
from srs.app.boto_service import send_message_to_queue, receive_messages, publish_order
import os
import json
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


app = FastAPI()


@app.post("/sns/")
def post_sns_order(topic: str, order_set: dict):
    result = publish_order(topic_arn=topic, order=order_set)
    return JSONResponse(status_code=200, content=result)


@app.post("/queue/")
def post_message(queue_name: str, body: dict):
    to_str = json.dumps(body)

    result = send_message_to_queue(
        queue_name,
        message_body=to_str
    )
    if result:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    if result is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Not found")
    # return result

# @app.get("/queue/")
# def receive():


@app.get("/queue")
def get_messages(queue_name: str):
    result = receive_messages(queue_name)
    if len(result) > 0:
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Not found")


# string_json_message = {"order_id": 101, "product": "laptop", "price": 1200}
# send_message_to_queue("devops-lab-orders",  message_body=string_json_message)
