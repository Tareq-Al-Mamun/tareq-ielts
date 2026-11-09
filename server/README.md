# TAREQ IELTS — AI Server

Backend server for AI-powered speech transcription and IELTS Speaking evaluation.

## Quick Start

```bash
cd server
npm install
node server.js
```

Server runs on **http://localhost:3001** and serves the main HTML file at **http://localhost:3001**.

## What It Does

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Health check (used by frontend to detect server status) |
| `/api/transcribe` | POST | Receives audio file, returns transcript via z-ai ASR |
| `/api/evaluate` | POST | Receives transcript + audio metrics, returns IELTS band scores + feedback via z-ai LLM |
| `/` | GET | Serves the main TAREQ IELTS HTML file |

## How It Works

1. **Recording** happens entirely in the browser (MediaRecorder API + Web Speech API for live transcription)
2. **Audio storage** uses IndexedDB (audio blobs are too large for localStorage)
3. **Server-side transcription** (optional fallback) — if the browser's Web Speech API doesn't capture a transcript, the audio is sent to `/api/transcribe` for z-ai ASR
4. **AI evaluation** — when the user clicks "Submit for AI Evaluation", each transcript + audio metrics is sent to `/api/evaluate`, which calls the z-ai LLM with a detailed IELTS examiner prompt

## API Keys

API keys are handled by the z-ai-web-dev SDK and **never exposed** to the frontend. The SDK is initialized on the server only.

## Architecture

```
Browser (HTML file)
  ├── MediaRecorder API     → Records audio
  ├── Web Speech API        → Live transcription (free, browser built-in)
  ├── Web Audio API          → Pronunciation metrics (pitch, volume, pace)
  ├── IndexedDB              → Stores audio blobs locally
  └── localStorage           → Stores transcripts, evaluations, progress
         │
         ▼
Backend (server.js on :3001)
  ├── POST /api/transcribe   → z-ai ASR (speech-to-text)
  └── POST /api/evaluate     → z-ai LLM (IELTS band scoring + feedback)
```

## Offline Behavior

- The website works **100% offline** for all existing features (questions, timers, bookmarks, notes, etc.)
- Recording + live transcription also works offline (Web Speech API is browser built-in)
- Only the **AI evaluation** step requires the server to be running
