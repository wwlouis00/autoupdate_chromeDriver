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

