from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove, makedirs
from shutil import rmtree
import pathlib
import uuid

from modules.detection import compare_images

router = APIRouter()

@router.post("/upload")
async def upload_file(file_photo: UploadFile = File(...), file_ine: UploadFile = File(...),file_video: UploadFile = File(...)):
    file_new_name = uuid.uuid4()
    
    imagen=["jpg","jpeg","png","gif"]
    video=["avi","mp4","mkv"]
    
    makedirs('uploads', exist_ok=True)
    makedirs('uploads/photo', exist_ok=True)
    makedirs('uploads/ine', exist_ok=True)
    makedirs('uploads/video', exist_ok=True)
    
    file_name_photo = pathlib.Path(file_photo.filename)
    file_name_ine = pathlib.Path(file_ine.filename)
    file_name_video = pathlib.Path(file_video.filename)
    
    if file_name_photo.suffix[1:] in imagen and file_name_ine.suffix[1:] in imagen and file_name_video.suffix[1:] in video :
        with open(getcwd() + "/uploads/photo/" + str(file_new_name) + file_name_photo.suffix , "wb") as myfile_photo:
            content = await file_photo.read()
            myfile_photo.write(content)
            myfile_photo.close()
    
        with open(getcwd() + "/uploads/ine/" + str(file_new_name) + file_name_ine.suffix , "wb") as myfile_ine:
            content = await file_ine.read()
            myfile_ine.write(content)
            myfile_ine.close()

        with open(getcwd() + "/uploads/video/" + str(file_new_name) + file_name_video.suffix , "wb") as myfile_video:
            content = await file_video.read()
            myfile_video.write(content)
            myfile_video.close()
        
        return JSONResponse(content={
                "message": "Files saved",
                "photo": myfile_photo.name,
                "ine": myfile_ine.name,
                "video": myfile_video.name,
                "detection": compare_images(Know= myfile_photo.name, Unknown= myfile_ine.name, Video=myfile_video.name)
                }, status_code=200)

    else:
        return JSONResponse(content={
            "message": "File not saved, verify send photo, ine, video",
            }, status_code=400)

@router.get("/file/{type_file}/{name_file}")
def get_file(type_file: str, name_file: str):
    return FileResponse(getcwd() + "/uploads/"+type_file +"/"+ name_file)


@router.get("/download/{type_file}/{name_file}")
def download_file(type_file:str, name_file: str):
    return FileResponse(getcwd() + "/uploads/"+type_file+"/" + name_file, media_type="application/octet-stream", filename=name_file)


@router.delete("/delete/{type_file}/{name_file}")
def delete_file(type_file:str, name_file: str):
    try:
        remove(getcwd() + "/uploads/"+ type_file + "/" + name_file)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "message": "File not found"
        }, status_code=404)
