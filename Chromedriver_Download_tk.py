import requests
import os
import zipfile
import tkinter as tk
from tkinter import ttk

def get_latest_chromedriver_version():
    """Fetch the latest ChromeDriver version from the Chrome for Testing website."""
    url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["channels"]["Stable"]["version"], data["channels"]["Stable"]["downloads"]["chromedriver"]
    else:
        raise Exception("Failed to fetch the latest ChromeDriver version.")

def download_chromedriver(download_url, download_path="chromedriver", progress_label=None, progress_bar=None):
    """Download the specified ChromeDriver."""
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    file_name = os.path.join(download_path, download_url.split("/")[-1])
    
    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # Size of each read chunk

    downloaded_size = 0
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=block_size):
            file.write(chunk)
            downloaded_size += len(chunk)
            if progress_label and progress_bar:
                progress = int(downloaded_size / total_size * 100)
                progress_label.config(text=f"Download Progress: {progress}%")
                progress_bar['value'] = progress
                root.update_idletasks()

    if downloaded_size == total_size:
        print(f"ChromeDriver downloaded successfully: {file_name}")
    else:
        raise Exception("Download failed. Please check if the URL is correct.")

    return file_name

def extract_chromedriver(file_path, extract_to="chromedriver"):
    """Extract the downloaded ChromeDriver zip file."""
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"ChromeDriver extracted to: {extract_to}")
    else:
        raise Exception("Only ZIP files are supported for extraction.")

def update_chromedriver():
    try:
        version, downloads = get_latest_chromedriver_version()
        print(f"Latest ChromeDriver version: {version}")
        
        platform = os.name
        if platform == "nt":  # Windows
            driver_info = next(item for item in downloads if "win64" in item["url"])
        elif platform == "posix" and os.uname().sysname == "Linux":
            driver_info = next(item for item in downloads if "linux64" in item["url"])
        elif platform == "posix" and os.uname().sysname == "Darwin":
            driver_info = next(item for item in downloads if "mac-x64" in item["url"])
        else:
            raise Exception("Unsupported platform.")
        
        download_url = driver_info["url"]
        downloaded_file = download_chromedriver(download_url, progress_label=progress_label, progress_bar=progress_bar)
        extract_chromedriver(downloaded_file)
        
        result_label.config(text="ChromeDriver has been updated successfully.")
    except Exception as e:
        result_label.config(text=f"Error occurred: {e}")

# Tkinter GUI
root = tk.Tk()
root.title("ChromeDriver Updater")

# Update button and result display
update_button = tk.Button(root, text="Update ChromeDriver", command=update_chromedriver)
update_button.pack(pady=10)

# Progress bar display
progress_label = tk.Label(root, text="Download Progress: 0%")
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()
