from fastapi import FastAPI, UploadFile, File
from os import getcwd, remove, listdir
from fastapi.responses import FileResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles

FOLDER = "./data/"
# STATIC_FOLDER = "./static/"

app = FastAPI()

# Static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Upload Images
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(FOLDER + file.filename, 'wb') as image:
        content = await file.read()
        image.write(content)
        image.close()
    return JSONResponse(content={"filename": file.filename}, status_code=200)

# Download files
@app.get("/download/{name_file}")
def download_file(name_file: str):
    #return FileResponse(path=getcwd() + "/" + name_file, media_type='application/octet-stream', filename=name_file)
    return FileResponse(path= FOLDER + name_file, media_type='application/octet-stream', filename=name_file)

# Get Files
@app.get("/file/{name_file}")
def get_file(name_file: str):
    #return FileResponse(path=getcwd() + "/" + name_file)    
    return FileResponse(path=FOLDER + name_file)    

# Delete files
@app.delete("/delete/file/{name_file}")
def delete_file(name_file: str):
    try:
        #remove(getcwd() + "/" + name_file)
        remove(FOLDER + name_file)
        return JSONResponse(content={
            "removed": True
            }, status_code=200)   
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "error_message": "File not found"
        }, status_code=404)

# List Files
@app.get("/list_files")
def list_files():
    files = []
    for file in listdir(FOLDER):
        files.append(file)
    return JSONResponse(content={"files": files}, status_code=200)