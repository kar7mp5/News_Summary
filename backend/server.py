# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from ArticleTools import get_req, summarize_article

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_content")
async def get_content(link):
    df = pd.DataFrame(get_req())
    text = summarize_article(df['link'][1])

    return {'text': text}
