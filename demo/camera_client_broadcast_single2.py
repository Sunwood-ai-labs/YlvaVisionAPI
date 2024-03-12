import cv2
import numpy as np
import requests
import time

# ブロードキャストを受信するエンドポイントのURL
url = "http://localhost:8000/camera"

# OpenCVのビデオキャプチャオブジェクトを作成
cap = cv2.VideoCapture(url)

# 保存するフレームのファイル名
filename = "captured_frame2.jpg"

start_time = time.time()  # 処理開始時間を記録

while True:
    # フレームを読み込む
    ret, frame = cap.read()

    if not ret:
        break

    # フレームを表示
    cv2.imshow("Frame", frame)

    # 'q'キーが押されたら終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 最後のフレームを保存
cv2.imwrite(filename, frame)
print(f"Frame saved as {filename}")

# 処理時間を計算
end_time = time.time()
processing_time = end_time - start_time

# 結果を表示
print(f"Processing Time: {processing_time:.2f} seconds")

# リソースを解放
cap.release()
cv2.destroyAllWindows()