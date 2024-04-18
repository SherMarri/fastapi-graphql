from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schema import tartiflette_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/graphql", tartiflette_app, name="graphql")
app.add_event_handler("startup", tartiflette_app.startup)
