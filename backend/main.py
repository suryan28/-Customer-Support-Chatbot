import os
import re

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import api_llm.qna_db as qna_db
from api_llm.llms import OpenAPI
from api_llm.prompts import Prompts
from zoho.zoho import ZohoDeskClient

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
llm = OpenAPI()
zoho_desk_client = ZohoDeskClient()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = os.getenv('ALLOWED_ORIGINS').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_username(data):
    response = llm.get_text_completion(prompt=Prompts.username_prompt_gen(data))
    answer = response.get('answer')
    isvalid = response.get('isvalid')
    content = {
        "text": f"Hi, {answer}, please let me know if you are inquiring about Baseball ⚾, Softball 🥎, or Soccer ⚽?",
        "username": answer,
        "isvalid": isvalid,
        "custom": {
            "payload": "quickReplies",
            "data": [
                {
                    "title": "Baseball ⚾",
                    "payload": "Baseball",
                },
                {
                    "title": "Softball 🥎",
                    "payload": "Softball",
                },
                {
                    "title": "Soccer ⚽",
                    "payload": "Soccer",
                },
            ],
        },
    }
    return content


def get_sports(data):
    response = llm.get_text_completion(prompt=Prompts.sports_prompt_gen(data))
    answer = response.get('answer').lower()
    isvalid = answer in ('baseball', 'softball', 'soccer')

    content = {"text": "Please let me know if you are a Parent 👨‍👩‍👦, Player ⚽, Coach 🏋️‍♂️, or ICC 🏟️?",
               "sports": answer,
               "isvalid": isvalid,
               "custom": {
                   "payload": "quickReplies",
                   "data": [
                       {
                           "title": "Parent 👨‍👩‍👦",
                           "payload": "Parent",
                       },
                       {
                           "title": "Player ⚽",
                           "payload": "Player",
                       },
                       {
                           "title": "Coach 🏋️‍♂️",
                           "payload": "Coach",
                       },
                       {
                           "title": "ICC 🏟️",
                           "payload": "ICC",
                       },
                   ],
               },
               }
    return content


def get_usertype(data):
    response = llm.get_text_completion(prompt=Prompts.usertype_prompt_gen(data))
    answer = response.get('answer').lower()
    isvalid = answer in ('player', 'coach', 'parent', 'icc')
    content = {"text": "How can I be of assistance today? 🤔💬",
               "usertype": answer,
               "isvalid": isvalid
               }
    return content


def user_qna(data):
    user_query = data.get('text')
    user_query = re.sub(r'[^a-zA-Z0-9\s]', '', user_query)
    user_query = user_query.lower()
    usertype = data.get('flag')
    qna = qna_db.get_qna()
    content = {
        "text": "I'm sorry, I don't understand your question, please ask it a different way",
        "category": "Other"
    }
    if len(user_query) <= 2:
        return content
    if user_query:
        keyword_data = llm.get_text_completion(
            prompt=Prompts.keywords_prompt_gen(user_query, qna.get('keywords_list')))
        if keyword_data.get('answer') == qna.get('keywords_list'):
            return content
    else:
        keyword_data = []
    if not keyword_data or not keyword_data.get('answer'):
        return content
    result = get_keywords_mapping(keyword_data.get('answer'), qna.get('keywords_dict'), qna.get('content_dict'),
                                   usertype)

    if not result or len(result) == 0:
        return content
    return result


def get_keywords_mapping(keywords, keywords_dict, content_dict, usertype):
    try:
        result = []
        key_list = []
        for keyword in keywords:
            for key, value in keywords_dict.items():
                if keyword.lower() in value.lower():
                    key_list.append(key)
                    break
        for key in set(key_list):
            if content_dict[
                key] == "A Please go to <a href='https://usaprimesports.com/workflow/locations' target='_blank' rel='noopener noreferrer'>https://usaprimesports.com/workflow/locations</a> to see all our locations across the country. Is there a USA Prime location near you that your player would like to tryout for?":
                result.append({
                    "text": content_dict[key],
                    "category": "tryouts"
                })
            else:
                result.append({
                    "text": content_dict[key],
                    "category": usertype
                })

        return result
    except Exception as e:
        return None


flag_functions = {
    "username": get_username,
    "sports": get_sports,
    "usertype": get_usertype,
    "player": user_qna,
    "coach": user_qna,
    "parent": user_qna,
    "icc": user_qna
}


@app.post("/chatbot")
async def chatbot(data: dict = Body(...)):
    flag = data.get('flag')
    if flag in flag_functions:
        result = flag_functions[flag](data)
        if type(result) == list:
            return JSONResponse(content=result)
        return JSONResponse(content=[result])

    return JSONResponse(content=[{"text": "Server is facing some issues. Please try again later. 🛠️🕒"}])


@app.post("/raise_ticket")
async def raise_ticket(data: dict = Body(...)):
    return JSONResponse(content=zoho_desk_client.raise_ticket(data))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "home"})


@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
