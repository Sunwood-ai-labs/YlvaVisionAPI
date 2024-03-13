import cv2
import requests
import numpy as np

def stream_video(url):
    """
    指定されたURLからビデオストリームを受信し、OpenCVを使用して表示します。
    :param url: ストリーミングAPIのURL
    """
    # ストリームからデータを取得するリクエストを送信
    response = requests.get(url, stream=True)

    # バイト列を一時的に保持するバッファ
    byte_buffer = bytes()

    for chunk in response.iter_content(chunk_size=1024):
        byte_buffer += chunk
        # フレームの終端を示すバイト列を探す
        a = byte_buffer.find(b'\xff\xd8')
        b = byte_buffer.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = byte_buffer[a:b+2]
            byte_buffer = byte_buffer[b+2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            # フレームを表示
            cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

# APIのURL
stream_url = 'http://localhost:8001/camera'

# ビデオストリームを開始
stream_video(stream_url)
