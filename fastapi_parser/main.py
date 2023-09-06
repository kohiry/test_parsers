"""Модуль запуска приложнеия."""
import asyncio
from parser import download_all_photos
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/download_photo")
async def download_photo_endpoint(folder: str):
    """dowqnload_all_photos(url).

    Функция для загрузки всех фотографий в заданную папку.

    Аргументы:
        folder (str): folder для загрузки фотографий.

    Возвращает:
        {status: succes}
    """
    asyncio.create_task(download_all_photos(folder))
    return JSONResponse(content={"status": "downloading"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
