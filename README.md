# Vox AI - AI Voice Receptionist for Clinics

Vox AI is a production-grade AI voice receptionist platform designed for healthcare, clinics, and hospitals. It features ultra-low latency voice-to-voice capabilities, a robust Master Agent architecture with barge-in interruption handling, AI-driven post-call evaluations, and a beautiful React frontend.

## 🚀 Tech Stack

- **Frontend:** React, TypeScript, Vite, TailwindCSS (Vanilla CSS for custom components), Lucide Icons
- **Backend:** FastAPI (Python), SQLAlchemy, asyncpg
- **Database:** PostgreSQL (via Supabase), Redis (for session management)
- **Voice / Telephony:** LiveKit (WebRTC), Exotel/Twilio (SIP integration)
- **AI Models:** 
  - **LLM:** Google Gemini 2.0 Flash
  - **Speech-to-Text (STT) & Text-to-Speech (TTS):** Sarvam AI (High-accuracy native Indian languages & English), Deepgram (Fallback)

---

## 🛠️ Local Development Setup

To run Vox AI locally for development, you will need to start both the Python Backend server and the React Frontend server.

### 1. Backend Setup

The backend handles the API, database connectivity, and the core AI agent logic.

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the `backend` folder and declare the following variables:
   * `DATABASE_URL`: Set this to your Supabase PostgreSQL connection string. For reliable IPv4 connections, use the Supabase **Session Pooler** host on port `5432`.
     > [!IMPORTANT]
     > If your database password contains `@` (e.g., `Musfir@h123`), it **must** be percent-encoded as `%40` in the URL (e.g., `postgresql://...:Musfir%40h123@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres`).
   * `SARVAM_API_KEY`: Set your Sarvam AI key to enable the primary native Indian languages voice agent integration.
   * `GEMINI_API_KEY`: Google Gemini API key from AI Studio for the voice agent LLM brain.
   * `LIVEKIT_*` keys: For WebRTC voice calling session hosting.

5. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The API will now be running on `http://localhost:8000`.

### 2. Frontend Setup

The frontend provides the Administration dashboards (Clinic view and SuperAdmin view).

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the Vite development server:**
   ```bash
   npm run dev
   ```
   The UI will now be running on `http://localhost:5173`. 
   * Local API requests are proxied directly to the backend on `localhost:8000`.

---

## 🔑 Default Dashboards & Logins

- **Clinic Dashboard:** `http://localhost:5173/login` (Use any credentials in demo mode)
- **SuperAdmin Dashboard:** `http://localhost:5173/superadmin/login` (Hardcoded credentials: `admin@vox-ai.com` / `vox-ai2026`)

## 🚢 Deployment Updates
*(Note: A comprehensive VPS container deployment guide is available in `scripts/setup_vps.sh` for when the application moves to production).*
