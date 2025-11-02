Media Downloader

# Description

This is a media downloader that allows users to download media files from various sources.

# Installation

1. Clone the repository: `git clone https://github.com/dante2182/drop.git`
2. Navigate to the project directory: `cd backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/Scripts/activate`
5. Install the required dependencies: `pip install -r requirements.txt`

# Commands

- Run the server:

```
uvicorn main:app --reload
```

# API Endpoints

- `POST /download`: Download a media file from a given URL.

  - Request Body:

  ```json
  {
    "url": "https://www.youtube.com/watch?v=wyXNQiRCfRg&list=RDmMqz_a9_eGU&index=9",
    "output_format": "mp4"
  }
  ```
