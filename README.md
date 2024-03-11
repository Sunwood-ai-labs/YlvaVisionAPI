# YlvaVisionAPI

<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/YlvaVisionAPI/main/docs/Ylva2.png" height=300px align="right"/>

YlvaVisionAPIは、Webカメラからリアルタイムの画像を取得し、ブロードキャストするためのAPIです。このREADMEでは、APIの機能、セットアップ方法、使用方法について説明します。

**機能**

YlvaVisionAPIは以下の機能を提供します。

- Webカメラからリアルタイムの画像を取得
- 取得した画像をブロードキャスト
- クライアントサイドでブロードキャストを受信し、画像を表示または保存

## セットアップ

APIを実行するには、以下の手順に従ってください。

### 必要なライブラリのインストール

以下のライブラリをインストールしてください。

- FastAPI: `pip install fastapi`
- Uvicorn: `pip install uvicorn`
- OpenCV: `pip install opencv-python`

### Webカメラの接続確認

APIを実行する前に、適切なWebカメラが接続されていることを確認してください。必要に応じて、コード内のカメラIDを変更してください。

### APIの起動

以下のコマンドを実行して、APIを起動します。

```
python api\camera_server_broadcast.py
```

APIが正常に起動すると、`http://localhost:8000/camera`でブロードキャストが開始されます。

## ブロードキャスト

YlvaVisionAPIは、以下のコードを使用してWebカメラからリアルタイムの画像をブロードキャストします。

```python
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
```

このコードは、FastAPIを使用してWebカメラからリアルタイムの画像を取得し、`gen_frames()`関数でフレームをエンコードしてブロードキャストします。

## クライアントサイドの使用方法

以下は、クライアントサイドでYlvaVisionAPIを使用するサンプルコードです。

### ブロードキャストを受信 / リアルタイムで画像を表示

```python
import cv2
import numpy as np
import requests
import time

# ブロードキャストを受信するエンドポイントのURL
url = "http://localhost:8000/camera"

# OpenCVのビデオキャプチャオブジェクトを作成
cap = cv2.VideoCapture(url)

# フレームの処理時間を保存するリスト
frame_times = []

while True:
    start_time = time.time()  # フレームの処理開始時間を記録

    # フレームを読み込む
    ret, frame = cap.read()

    if not ret:
        break

    # フレームの処理時間を計算
    end_time = time.time()
    frame_time = end_time - start_time
    frame_times.append(frame_time)

    # フレームを表示
    cv2.imshow("Camera Stream", frame)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 平均フレーム処理時間を計算
avg_frame_time = sum(frame_times) / len(frame_times)

# 結果を表示
print(f"Average Frame Processing Time: {avg_frame_time:.2f} seconds")
print(f"Average FPS: {1 / avg_frame_time:.2f}")

# リソースを解放
cap.release()
cv2.destroyAllWindows()
```

このコードは、ブロードキャストを受信し、リアルタイムでフレームを表示します。また、フレームの処理時間を計測し、平均フレーム処理時間と平均フレームレートを表示します。

<blockquote class="twitter-tweet" data-media-max-width="560"><p lang="ja" dir="ltr">Claude3 オンリーでWEBカメラをブロードキャストするAPIを自作してリアルタイム表示してみた！ <a href="https://t.co/iE31npQOL1">pic.twitter.com/iE31npQOL1</a></p>&mdash; Maki@Sunwood AI Labs. (@hAru_mAki_ch) <a href="https://twitter.com/hAru_mAki_ch/status/1767180863639609760?ref_src=twsrc%5Etfw">March 11, 2024</a></blockquote> 

### ブロードキャストから画像を取得 / 保存

```python
import cv2
import numpy as np
import requests
import time

# ブロードキャストを受信するエンドポイントのURL
url = "http://localhost:8000/camera"

# OpenCVのビデオキャプチャオブジェクトを作成
cap = cv2.VideoCapture(url)

# 保存するフレームのファイル名
filename = "captured_frame.jpg"

start_time = time.time()  # 処理開始時間を記録

# フレームを読み込む
ret, frame = cap.read()

if ret:
    # フレームを保存
    cv2.imwrite(filename, frame)
    print(f"Frame saved as {filename}")
else:
    print("Failed to capture frame")

# 処理時間を計算
end_time = time.time()
processing_time = end_time - start_time

# 結果を表示
print(f"Processing Time: {processing_time:.2f} seconds")

# リソースを解放
cap.release()
```

このコードは、ブロードキャストから1フレームを取得し、指定したファイル名で保存します。また、処理時間を計測し、結果を表示します。

> 撮影画像

![](https://raw.githubusercontent.com/Sunwood-ai-labs/YlvaVisionAPI/main/demo/captured_frame.jpg)

## まとめ

YlvaVisionAPIを使用することで、Webカメラからリアルタイムの画像を取得し、ブロードキャストすることができます。クライアントサイドでは、ブロードキャストを受信し、画像を表示したり保存したりすることができます。

APIのセットアップと使用方法を理解することで、YlvaVisionAPIをプロジェクトに組み込むことができます。サンプルコードを参考に、必要な機能を実装してください。


<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>