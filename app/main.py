from fastapi import FastAPI, Depends
from app.core.settings import Settings, get_settings

app = FastAPI()


@app.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "env": settings.ENV}
