# GitHub Webhook Tracker 🚀

A full-stack Python project to capture and display GitHub events like pushes and pull requests in real time using Flask, MongoDB, and a stylish UI.

---

## 🔗 Live Demo

🌐 [Webhook App on Render](https://webhook-repo-1-lyuy.onrender.com)

---

## 📦 Tech Stack

- **Backend**: Flask + Python
- **Frontend**: HTML + Jinja2 + CSS (Dark Green theme)
- **Database**: MongoDB Atlas (Cloud)
- **Dev Tools**: GitHub Webhooks, GitHub Actions (simulated), Render for hosting

---

## 🧩 Features

- 🟢 Tracks Push Events
- 📦 Detects Pull Requests (opened & reopened)
- ✅ Detects Pull Request Merges
- 🕒 Shows timestamps in IST
- 🗃️ Stores events in MongoDB Atlas
- 🎨 Beautiful dark-themed UI with live updates every 15s

---

## ⚙️ How It Works

1. GitHub Webhook triggers on **push** and **pull_request**
2. Flask receives the POST data at `/webhook`
3. MongoDB stores each event with timestamp
4. `/events` endpoint returns latest 10 events
5. Frontend polls `/events` every 15s to display them

---

## 📁 Project Structure

```bash
webhook-repo/
├── templates/
│   └── index.html     # Frontend UI
├── .env               # MongoDB URI (not pushed to GitHub)
├── .gitignore
├── app.py             # Flask backend
├── requirements.txt
└── README.md
