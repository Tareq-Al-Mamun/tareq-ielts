# 🚀 Deploy TAREQ IELTS to Netlify (with Gemini AI evaluation)

This guide shows you how to host the TAREQ IELTS website on **Netlify** and connect it to a **Gemini-powered backend** so AI evaluation works in production.

## ⚠️ Important: Netlify is for static files only

Netlify hosts the HTML/CSS/JS of your website, but it **cannot** run the Node.js backend that talks to Google Gemini. So you need to deploy **two things**:

| What | Where | Cost |
|---|---|---|
| **Frontend** (the HTML website) | Netlify | Free |
| **Backend** (Node.js + Gemini API) | Railway (or Render / Fly.io) | Free |

The frontend will talk to the backend over HTTPS. This is exactly how production websites work.

---

## Step 1: Prepare your project files

Your project should look like this:

```
tareq-ielts/
├── download/                            ← frontend (Netlify)
│   └── TAREQ_IELTS_Speaking_Practice.html
├── server/                              ← backend (Railway)
│   ├── server.js
│   ├── package.json
│   ├── .env                             ← your GEMINI_API_KEY (gitignored)
│   └── ...
├── netlify/
│   └── netlify.toml                     ← Netlify config
├── render.yaml                          ← optional Render config
├── Dockerfile                           ← optional Fly.io config
└── .gitignore
```

All these files are already created for you in `/home/z/my-project/`.

---

## Step 2: Push to GitHub

Netlify and Railway both work best with a GitHub repo.

```bash
cd /home/z/my-project
git init
git add .
git commit -m "TAREQ IELTS with Gemini AI evaluation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/tareq-ielts.git
git push -u origin main
```

⚠️ **IMPORTANT**: Verify `.env` is in `.gitignore` (it is) before pushing — never commit your Gemini API key.

---

## Step 3: Deploy the backend on Railway

Railway gives you 500 free hours/month — enough for individual use.

1. Visit **https://railway.app** → sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `tareq-ielts` repo
4. Railway auto-detects Node.js. Set these settings:
   - **Root Directory**: `server`
   - **Build Command**: `npm install`
   - **Start Command**: `node server.js`
5. Go to the **Variables** tab and add:
   - `GEMINI_API_KEY` = (paste your Gemini API key)
   - `GEMINI_MODEL` = `gemini-1.5-flash` (optional, this is the default)
6. Click **Deploy**. Railway will give you a URL like:
   `https://tareq-ielts-api-production.up.railway.app`
7. Test it by visiting `https://YOUR-RAILWAY-URL/api/health` in your browser. You should see:
   ```json
   {"status":"ok","provider":"gemini","geminiAvailable":true,"geminiModel":"gemini-1.5-flash"}
   ```

### Alternative: Render.com
Use `render.yaml` (already created for you). Visit https://render.com → New → Web Service → connect GitHub → it will auto-read `render.yaml`. Set `GEMINI_API_KEY` in the dashboard.

### Alternative: Fly.io
```bash
cd /home/z/my-project
fly launch        # uses Dockerfile
fly secrets set GEMINI_API_KEY=your-key-here
```

---

## Step 4: Deploy the frontend on Netlify

1. Visit **https://app.netlify.com** → sign in with GitHub
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect your GitHub account and select your `tareq-ielts` repo
4. Configure the build:
   - **Base directory**: leave blank (root)
   - **Build command**: leave blank (the HTML is already built)
   - **Publish directory**: `download`
   - (Netlify will auto-read `netlify/netlify.toml`)
5. Click **Deploy site**. Netlify gives you a URL like:
   `https://tareq-ielts.netlify.app`

### Quick alternative: Drag-and-drop
If you don't want to use GitHub:
1. Visit https://app.netlify.com/drop
2. Drag the `download/` folder onto the page
3. Done — Netlify gives you a URL instantly

---

## Step 5: Connect the frontend to the backend

You have two ways to link them:

### Option A — via URL parameter (easy, shareable)
Visit your Netlify site with the backend URL as a query parameter:
```
https://tareq-ielts.netlify.app/?api=https://tareq-ielts-api-production.up.railway.app
```
The frontend saves this URL to localStorage and uses it for all future visits. The `?api=...` part is automatically stripped from the URL after saving.

### Option B — via Settings page (permanent)
1. Open your Netlify site: `https://tareq-ielts.netlify.app`
2. Go to **Settings** → **AI Evaluation Server**
3. Enter your Railway backend URL: `https://tareq-ielts-api-production.up.railway.app`
4. Click **"💾 Save & Test Connection"**
5. The website tests the `/api/health` endpoint and shows:
   `✓ Connected — provider: gemini (Gemini)`
6. Reload the page. Done!

---

## Step 6: Test AI evaluation

1. Open `https://tareq-ielts.netlify.app`
2. Click **"Speaking Part 1"** → pick any topic → click "🎙 Record Answer"
3. Allow microphone access → speak → click "⏹ Stop"
4. Within ~20 seconds, the Gemini evaluation appears inline below the question:
   - Band score badge
   - "gemini" provider badge
   - 4 criteria scores (FC, LR, GRA, PR)
   - Detailed feedback (grammar corrections, vocab improvements, improvement plan)

If you see `● AI Server Online` on the AI Evaluation page, you're good.

---

## 📊 Free tier limits (cost = $0)

| Service | Free tier | Sufficient for |
|---|---|---|
| **Netlify** | 100 GB bandwidth, 300 min build/month | ~10k visitors/month |
| **Railway** | 500 hours/month, $5 credit | 24/7 backend (~720h needed for always-on, may need to pay $5/month) |
| **Render** | 750 hours/month, sleeps after 15 min idle | Always-on backend, but cold starts (~30s) |
| **Gemini API** | 15 RPM, 1500 requests/day, 1M tokens/min | ~1500 evaluations/day |

**Recommendation**: Use **Railway** if you don't mind paying $5/month after the trial, or **Render** if you want fully free (but with cold starts). For purely free with no cold starts, use **Fly.io**.

---

## 🔒 Security checklist

- ✅ `GEMINI_API_KEY` is in `server/.env` (gitignored, never in frontend)
- ✅ Set `GEMINI_API_KEY` as a Railway/Render environment variable (NOT in your repo)
- ✅ CORS is enabled in the backend (`app.use(cors())`)
- ✅ Audio recordings stay in the user's browser (IndexedDB) — only transcripts are sent to Gemini
- ✅ The backend never logs or returns the API key

---

## 🌐 Custom domain (optional)

### Netlify (frontend)
1. Netlify dashboard → your site → **Domain settings** → **Add custom domain**
2. Add `tareqielts.com` (or any domain you own)
3. Update your DNS to point to Netlify's nameservers

### Railway (backend)
1. Railway dashboard → your service → **Settings** → **Networking** → **Generate Domain**
2. Or add a custom domain (e.g., `api.tareqielts.com`)

After both are configured, just update the API URL in the website's Settings page.

---

## 🆘 Troubleshooting

### "AI Server Offline" badge
→ The frontend can't reach the backend. Check:
1. Is the Railway/Render service running? Visit `https://YOUR-BACKEND/api/health`
2. Did you set the API URL via `?api=` or Settings page?
3. Open browser DevTools (F12) → Console — what error do you see?
4. Check the backend logs on Railway/Render

### CORS errors in browser console
→ Your backend isn't allowing the Netlify origin. The `server.js` already has `app.use(cors())` (allows all origins). If you've restricted CORS, add your Netlify URL to the allowed list.

### Evaluation times out (>60s)
→ Gemini 1.5-flash should respond in 15–30s. If it's slower:
1. Check your Gemini API quota at https://aistudio.google.com/app/usage
2. Try reducing the transcript length (long answers take longer)
3. Switch to `gemini-1.5-flash-8b` (cheaper, faster, slightly lower quality):
   - Set `GEMINI_MODEL=gemini-1.5-flash-8b` in Railway/Render env vars

### Mock test evaluation fails
→ Mock tests send 10 answers (~10KB request), which can take 30–60s. If Railway/Render times out:
- Railway: default timeout is generous, should work
- Render: free tier has 100s timeout, should work
- If using serverless (Vercel/Netlify Functions): switch to Railway — serverless has 10s limit on free tier

### "provider": "z-ai" instead of "gemini"
→ The `GEMINI_API_KEY` env var isn't being read. Check:
1. Railway/Render dashboard → Variables → `GEMINI_API_KEY` is set
2. Backend logs (on startup): should say `✅ Google Gemini SDK initialized`
3. If not, the key might be invalid or the SDK not installed

### Recording doesn't work
→ Microphone access requires HTTPS. Netlify automatically serves over HTTPS, so this works. If you deployed elsewhere, make sure HTTPS is enabled.

---

## 📁 Deployment files summary

| File | Purpose |
|---|---|
| `netlify/netlify.toml` | Netlify config (publish dir, redirects, headers) |
| `server/railway.json` | Railway deployment config + env var definitions |
| `render.yaml` | Render.com deployment config (alternative) |
| `Dockerfile` | Docker config for Fly.io / any container host |
| `.gitignore` | Prevents `.env` from being committed |
| `server/SETUP.md` | Detailed setup guide (already created earlier) |

---

## ✅ Production checklist

Before sharing your website with students, verify:

- [ ] Netlify site is live (visit `https://YOUR-SITE.netlify.app`)
- [ ] Railway/Render backend is live (visit `https://YOUR-BACKEND/api/health` → returns `provider: "gemini"`)
- [ ] API URL is set in the website (Settings → AI Evaluation Server → Connected)
- [ ] Part 1 recording → evaluation appears within 30s
- [ ] Part 2 cue card → evaluation appears within 30s
- [ ] Part 3 question → evaluation appears within 30s
- [ ] Full Mock Test → all 10 answers evaluated, full report renders
- [ ] Evaluation History page shows past evaluations
- [ ] Microphone permission prompt appears on Chrome/Firefox/Safari
- [ ] HTTPS works (no mixed-content warnings in DevTools)

Once all boxes are checked, share your Netlify URL with students! 🎓
