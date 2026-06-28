# BrainSpark Backend 🧠

Django REST API for the BrainSpark brain puzzle game app.

## Setup (Local)

```bash
pip install -r requirements.txt
cp .env.example .env         # fill in your keys
python manage.py migrate
python seed_puzzles.py       # add sample puzzles
python manage.py runserver
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/users/register/ | Register new user |
| GET | /api/users/profile/<id>/ | Get user profile |
| GET | /api/users/by-email/?email= | Login by email |
| GET | /api/puzzles/?type=&difficulty= | Get random puzzle |
| GET | /api/puzzles/all/ | Get all puzzles (offline cache) |
| POST | /api/puzzles/verify/ | Check answer |
| POST | /api/sessions/submit/ | Submit game score |
| GET | /api/sessions/history/<id>/ | User game history |
| GET | /api/leaderboard/global/ | Top 50 players |
| GET | /api/leaderboard/weekly/ | This week's top players |
| GET | /api/leaderboard/rank/<id>/ | User's rank |
| GET | /api/daily/ | Today's daily challenge |
| POST | /api/hints/ | Get AI hint for puzzle |
| GET | /api/badges/<id>/ | User's earned badges |

## Deploy to Railway (free)
1. Push to GitHub
2. Connect Railway to your repo
3. Add env variables in Railway dashboard
4. Done — auto deploys on every push!

## Tech Stack
- Python 3.12 + Django 4.2
- Django REST Framework
- SQLite (local) / PostgreSQL (production)
- Gemini API for AI hints (free tier)
