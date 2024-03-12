from fastapi import FastAPI, Response
import cv2
import numpy as np
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

# WebカメラのIDを指定（デフォルトは0）
camera_id = 0

# カメラオブジェクトをグローバルに保持
cap = cv2.VideoCapture(camera_id)

# カメラの解像度を設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

async def gen_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, img_encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n')
        await asyncio.sleep(0.01)  # 10ミリ秒のディレイを追加

@app.get("/camera")
async def get_camera_stream():
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace;boundary=frame")

@app.on_event("shutdown")
async def shutdown_event():
    # アプリケーションが終了するときにカメラを解放
    cap.release()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)