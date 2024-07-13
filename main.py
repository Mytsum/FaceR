from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import face_recognition
import base64
import numpy as np
import cv2
app = FastAPI()

class ImageData(BaseModel):
    image1_base64: str
    image2_base64: str

def decode_base64_image(base64_string):
    try:
        img_data = base64.b64decode(base64_string)
        np_array = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        if image is None:
            return None
        if len(image.shape) != 3 or image.shape[2] != 3:
            return None
        return image
    except Exception as e:
        return None


@app.get("/")
def read_root():
    return {"status": "Hi! this is face recognition app."}


# @app.post("/compare_faces")
# def compare_faces(data: ImageData):
#     image1_base64 = data.image1_base64
#     image2_base64 = data.image2_base64
#     return {"status": 200,"image1_base64": image1_base64,"image2_base64": image2_base64}
@app.post("/compare_faces")
def compare_faces(data: ImageData):
    image1_base64 = data.image1_base64
    image2_base64 = data.image2_base64
    if not image1_base64 or not image2_base64:
        raise HTTPException(status_code=400, detail="Please provide both image1_base64 and image2_base64")

    try:
        image1 = decode_base64_image(image1_base64)
        image2 = decode_base64_image(image2_base64)

        image1_encoding = face_recognition.face_encodings(image1)
        image2_encoding = face_recognition.face_encodings(image2)

        if not image1_encoding or not image2_encoding:
            raise HTTPException(status_code=400, detail="No faces found in one of the images")

        image1_encoding = image1_encoding[0]
        image2_encoding = image2_encoding[0]
        results = face_recognition.compare_faces([image1_encoding], image2_encoding)
        face_distance = face_recognition.face_distance([image1_encoding], image2_encoding)[0]

        match = bool(results[0])
        confidence = 1 - face_distance  # Confidence level

        return {"match": match, "confidence": confidence}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))