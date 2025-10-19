# ChromeDriver Auto-Update Tool

## Overview

This tool provides a simple graphical user interface (GUI) for automatically downloading and updating the latest version of ChromeDriver. The program fetches the latest version information from the official Chrome for Testing website, downloads the corresponding driver, and extracts it to a specified directory.

## Features

* Automatically retrieves the latest ChromeDriver version.
* Downloads the ChromeDriver version suitable for your system (Windows/Linux/macOS).
* Displays a progress bar during the download.
* Automatically extracts the driver after download.

## System Requirements

* Python 3.x
* `requests` and `tkinter` Python packages.

## Dependencies

Please make sure the following Python packages are installed:

```sh
pip install requests
```

`tkinter` is included in the standard Python library and does not require installation.

## Usage

1. Ensure the `requests` package is installed.
2. Run the Python script.
3. Click the "Update ChromeDriver" button. The program will automatically download and extract the latest ChromeDriver.

## Notes

* The tool automatically selects the appropriate ChromeDriver version based on your operating system.
* If an error occurs during execution, please check your network connection or verify that the ChromeDriver download URL is accessible.
* Supported platforms: Windows, Linux, and macOS.

## References

* [Chrome for Testing Official Website](https://googlechromelabs.github.io/chrome-for-testing/)
* [ChromeDriver Official Downloads](https://sites.google.com/chromium.org/driver/)
