from fastapi import FastAPI
from src.app.apis.abacus_neurofeedback import router

app = FastAPI()
app.include_router(router)
