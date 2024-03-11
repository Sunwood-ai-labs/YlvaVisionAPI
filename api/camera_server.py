from fastapi import FastAPI, Response
import cv2
import numpy as np
from fastapi.responses import StreamingResponse

app = FastAPI()

# WebカメラのIDを指定（デフォルトは0）
camera_id = 0

@app.get("/camera")
async def get_camera_frame():
    # Webカメラからフレームをキャプチャ
    cap = cv2.VideoCapture(camera_id)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return {"error": "Failed to capture frame from camera"}

    # OpenCVのBGR画像をJPEG画像に変換
    _, img_encoded = cv2.imencode(".jpg", frame)

    # レスポンスを作成
    return StreamingResponse(iter([img_encoded.tobytes()]), media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)