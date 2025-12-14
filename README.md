# 4Plebs YouTube Links Data Mining

A Python tool designed to scrape `/pol/` threads from [4plebs.org](https://archive.4plebs.org/) for music recommendations, extract YouTube links, and download them as high-quality MP3s with metadata.

## Features

- **Automated Scraping**: Crawls "pol music" threads on 4plebs (pages 1-55).
- **Link Extraction**: Identifies and extracts YouTube URLs from threads.
- **Filtering**: Automatically filters out playlists, channels, and search results to focus on individual songs.
- **Audio Downloading**: Uses `yt-dlp` to download audio and `ffmpeg` to convert it to MP3 (192kbps).
- **Resumable Progress**: Saves progress in pickle files (`.pkl`), allowing the script to resume from where it left off.
- **Hibernation Prevention**: Prevents Windows systems from sleeping while the script is running.

## Prerequisites

- **Python 3.x**
- **FFmpeg**: Required for audio conversion.
  - *Windows*: An `ffmpeg.exe` is included in the root directory, but ensuring it is in your system PATH is recommended.
  - *Linux/macOS*: Install via your package manager (e.g., `sudo apt install ffmpeg` or `brew install ffmpeg`).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script:

```bash
python getlinks.py
```

### How it works

1.  **Thread Scraping**: The script searches for threads with the subject "pol music" on pages 1 through 55 of the 4plebs archive. Thread links are saved to `pickles_thread/`.
2.  **Link Extraction**: It visits each thread and extracts YouTube links, saving them to `YT_pickles/`.
3.  **Downloading**: It aggregates all unique YouTube links (filtering out unwanted types) and downloads the audio to the `download_songs/` folder.

## Project Structure

- `getlinks.py`: Main script for scraping and downloading.
- `prevent_hibernation.py`: Utility to keep Windows awake during execution.
- `pickles_thread/`: Stores intermediate data (scraped thread links).
- `YT_pickles/`: Stores intermediate data (extracted YouTube links).
- `download_songs/`: Destination folder for downloaded MP3 files.
- `ffmpeg.exe`: FFmpeg executable (Windows only).

## Notes

- **Network Usage**: This script makes numerous requests to 4plebs and YouTube.
- **Sleep Timers**: The script includes sleep timers to avoid hitting rate limits, but scraping logic is hardcoded for specific pages (1-55).
- **Error Handling**: Failed downloads are skipped.

## Disclaimer

This tool is for educational purposes. Respect the terms of service of the websites you scrape. Downloading copyrighted content may be illegal in your jurisdiction.
