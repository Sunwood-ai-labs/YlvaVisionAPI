from fastapi import FastAPI, Response
import cv2
import numpy as np
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

# カメラ設定
camera_id = 0
cap = cv2.VideoCapture(camera_id)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

# 最新のフレームを保持する変数
latest_frame = None

async def fetch_camera_frame():
    global latest_frame
    while True:
        ret, frame = cap.read()
        if ret:
            _, img_encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            latest_frame = img_encoded.tobytes()
        await asyncio.sleep(0.01)  # カメラからのフレーム取得間隔

async def gen_frames():
    while True:
        if latest_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
        await asyncio.sleep(0.01)  # クライアントへの送信間隔

@app.on_event("startup")
async def startup_event():
    # カメラフレームのフェッチをバックグラウンドで開始
    asyncio.create_task(fetch_camera_frame())

@app.get("/camera")
async def get_camera_stream():
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace;boundary=frame")

@app.on_event("shutdown")
async def shutdown_event():
    cap.release()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)