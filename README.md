# Video Frame Similarity Search using FastAPI

## Overview

This is a full-stack application built using **FastAPI** that allows users to:

- Upload a video
- Automatically extract frames from the video
- Compute feature vectors for each frame
- Upload a query image to find similar frames
- View matching frames and similarity scores

The system provides a simple web interface for uploading and querying, and uses a vector database for fast similarity search.

---

## Purpose

The purpose of this project is to demonstrate the ability to:

- Build scalable APIs using FastAPI
- Work with OpenCV for image and video processing
- Apply deep learning feature extraction techniques
- Integrate with vector databases like Qdrant
- Create clean, functional UI using HTML and JS
- Deploy machine learning as a real-world service

---

## Technologies Used

| Area             | Technology        |
|------------------|-------------------|
| Backend API      | FastAPI           |
| UI Rendering     | Jinja2 Templates  |
| Video Processing | OpenCV            |
| Feature Vectors  | Color Histograms / CNNs |
| Vector Database  | Qdrant (in-memory or persistent) |
| Deployment       | Uvicorn           |
| Frontend         | HTML, JavaScript  |

---

## Features

### 1. Video Upload
- Upload `.mp4` video via web UI
- Extracts frames automatically
- Each frame is vectorized and stored for similarity search

### 2. Image-Based Search
- Upload any image (e.g. screenshot of another video)
- Finds the most visually similar frames from uploaded videos
- Displays results with similarity scores

### 3. Unified Interface
- Upload, search, and view results on the same page
- Clean, student-friendly UI
- No reloads, interactive experience

---

## How It Works

1. **Video Upload**
    - Saves video temporarily
    - Extracts frames at 1-second intervals
    - Converts frames to feature vectors
    - Stores them in a vector database

2. **Query Image**
    - Converts uploaded image into a feature vector
    - Searches for similar vectors using cosine similarity
    - Returns top matches with image previews and scores

---

## How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/video-frame-search
cd video-frame-search
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Server
```bash
uvicorn app.main:app --reload
```
### 4. Open in Browser
Visit:
http://127.0.0.1:8000


