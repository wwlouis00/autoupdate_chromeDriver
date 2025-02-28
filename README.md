# ChromeDriver 自動更新工具

## 簡介
本工具提供一個簡單的圖形化介面 (GUI)，用於自動下載並更新最新版本的 ChromeDriver。程式會從 Chrome for Testing 官方網站取得最新版本資訊，下載相應的驅動程式，並解壓縮到指定目錄。

## 功能
- 自動取得最新的 ChromeDriver 版本。
- 根據系統類型 (Windows/Linux/macOS) 下載對應版本的 ChromeDriver。
- 下載過程中顯示進度條。
- 下載完成後自動解壓縮。

## 環境需求
- Python 3.x
- 需要安裝 `requests` 和 `tkinter` 套件。

## 依賴套件
請確保已安裝以下 Python 套件：
```sh
pip install requests
```
`tkinter` 為 Python 標準庫的一部分，無需額外安裝。

## 程式碼
```python
import requests
import os
import zipfile
import tkinter as tk
from tkinter import ttk

def get_latest_chromedriver_version():
    """從 Chrome for Testing 網站取得最新的 ChromeDriver 版本。"""
    url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["channels"]["Stable"]["version"], data["channels"]["Stable"]["downloads"]["chromedriver"]
    else:
        raise Exception("無法取得最新 ChromeDriver 版本資訊。")

def download_chromedriver(download_url, download_path="chromedriver", progress_label=None, progress_bar=None):
    """下載指定的 ChromeDriver。"""
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    file_name = os.path.join(download_path, download_url.split("/")[-1])
    
    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 每次讀取的塊大小

    downloaded_size = 0
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=block_size):
            file.write(chunk)
            downloaded_size += len(chunk)
            if progress_label and progress_bar:
                progress = int(downloaded_size / total_size * 100)
                progress_label.config(text=f"下載進度: {progress}%")
                progress_bar['value'] = progress
                root.update_idletasks()

    if downloaded_size == total_size:
        print(f"ChromeDriver 下載完成，儲存於: {file_name}")
    else:
        raise Exception("下載失敗，請確認 URL 是否正確。")

    return file_name

def extract_chromedriver(file_path, extract_to="chromedriver"):
    """解壓縮下載的 ChromeDriver。"""
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"ChromeDriver 已解壓縮至: {extract_to}")
    else:
        raise Exception("僅支援 ZIP 格式的檔案解壓縮。")

def update_chromedriver():
    try:
        version, downloads = get_latest_chromedriver_version()
        print(f"最新 ChromeDriver 版本為: {version}")
        
        platform = os.name
        if platform == "nt":  # Windows
            driver_info = next(item for item in downloads if "win64" in item["url"])
        elif platform == "posix" and os.uname().sysname == "Linux":
            driver_info = next(item for item in downloads if "linux64" in item["url"])
        elif platform == "posix" and os.uname().sysname == "Darwin":
            driver_info = next(item for item in downloads if "mac-x64" in item["url"])
        else:
            raise Exception("未支援的平台。")
        
        download_url = driver_info["url"]
        downloaded_file = download_chromedriver(download_url, progress_label=progress_label, progress_bar=progress_bar)
        extract_chromedriver(downloaded_file)
        
        result_label.config(text="ChromeDriver 已完成更新。")
    except Exception as e:
        result_label.config(text=f"發生錯誤: {e}")

# Tkinter GUI
root = tk.Tk()
root.title("ChromeDriver 更新")

# 下載按鈕和結果顯示
update_button = tk.Button(root, text="更新 ChromeDriver", command=update_chromedriver)
update_button.pack(pady=10)

# 進度條顯示
progress_label = tk.Label(root, text="下載進度：0%")
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()
```

## 使用方法
1. 確保已安裝 `requests` 套件。
2. 執行 Python 腳本。
3. 點擊「更新 ChromeDriver」按鈕，程式將自動下載並解壓縮最新的 ChromeDriver。

## 注意事項
- 本工具會根據系統類型選擇適合的 ChromeDriver 版本。
- 若執行過程中發生錯誤，請確認網路連線是否正常，或檢查 ChromeDriver 下載 URL 是否可用。
- 目前支援 Windows、Linux 和 macOS 平台。

## 參考資料
- [Chrome for Testing 官方網站](https://googlechromelabs.github.io/chrome-for-testing/)
- [ChromeDriver 官方下載](https://sites.google.com/chromium.org/driver/)

