import os
import shutil
from fastapi import UploadFile
from pathlib import Path



UPLOAD_DIR = "./uploaded_docs"


def save_uploaded_files(files:list[UploadFile])-> list[str]:
    os.makedirs(UPLOAD_DIR,exist_ok=True)
    file_paths = []

    for file in file_paths:
        temp_path = Path(UPLOAD_DIR)/file.filename
        with open(temp_path,"wb") as f:
            shutil.copyfileobj(file.file,f)
        file_paths.append(temp_path)

    return file_paths
        