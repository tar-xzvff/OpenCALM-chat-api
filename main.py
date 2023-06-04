import secrets
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

BASIC_AUTH_USERNAME = b"user"
BASIC_AUTH_PASSWORD = b"P@assW0rd"

RUNNING_ON_GPU = True

if RUNNING_ON_GPU:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model = AutoModelForCausalLM.from_pretrained(
        "/home/ubuntu/model/cyberagent/open-calm-7",
        device_map="auto",
        torch_dtype=torch.float16
    )
    tokenizer = AutoTokenizer.from_pretrained("/home/ubuntu/model/cyberagent/open-calm-7")


def talk(message):
    inputs = tokenizer(message, return_tensors="pt").to(model.device)
    with torch.no_grad():
        tokens = model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.05,
            pad_token_id=tokenizer.pad_token_id,
        )

    output = tokenizer.decode(tokens[0], skip_special_tokens=True)
    return output


class Message(BaseModel):
    body: str


app = FastAPI()

security = HTTPBasic()


@app.get("/")
async def root():
    return {"message": "I'm OpenCALM"}


def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = BASIC_AUTH_USERNAME
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = BASIC_AUTH_PASSWORD
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/api/chat")
async def chat(message: Message, username: Annotated[str, Depends(get_current_username)]) -> Message:
    if not RUNNING_ON_GPU:
        return Message(body="This is dummy response.")
    query = message.dict().get('body')
    reply = talk(query)
    return Message(body=reply)
