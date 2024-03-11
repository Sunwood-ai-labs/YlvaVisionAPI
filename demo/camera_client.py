import requests
import os

# APIのエンドポイントURL
api_url = "http://localhost:8000/camera"

# 画像を保存するディレクトリ
save_directory = "camera_images"

# 保存ディレクトリが存在しない場合は作成
os.makedirs(save_directory, exist_ok=True)

# APIから画像を取得
response = requests.get(api_url)

if response.status_code == 200:
    # レスポンスからファイル名を取得（ここではタイムスタンプを使用）
    timestamp = response.headers.get("X-Timestamp", "default")
    file_name = f"camera_image_{timestamp}.jpg"

    # 画像を保存
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, "wb") as file:
        file.write(response.content)
    
    print(f"Image saved successfully: {file_path}")
else:
    print(f"Failed to retrieve image. Status code: {response.status_code}")