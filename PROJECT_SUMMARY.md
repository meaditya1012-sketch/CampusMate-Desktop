# CampusMate — Project Summary

CampusMate is a desktop student organizer built with Python, PySide6, and SQLite. It brings class planning, coursework, attendance, study notes, focus sessions, and an optional AI tutor into one desktop app.

## How the project grew

### 1. Student organizer foundation

The first version established the PySide6 desktop window and SQLite database. It introduced the core schedule, task, and attendance screens so students could enter and review their own information.

### 2. Study features and visual direction

The next iteration developed the CampusMate Obsidian look: a dark interface with violet accents, sidebar navigation, cards, and styled tables. The app grew to include a dashboard, Study Center, Pomodoro timer, revision notes, and an AI Tutor screen backed by a local Ollama model.

### 3. Product and macOS release preparation

The latest work unified the screen styling, made the dashboard more prominent, added a CampusMate app icon, and prepared a macOS build. The app now creates its database tables on first launch. Packaged builds store each user's database in macOS Application Support, while source runs continue to use the project folder.

## Features

- **Dashboard:** today's classes, pending tasks, attendance summary, upcoming work, and a shortcut to the AI Tutor.
- **Schedule:** add and view weekly classes with teacher, time, and room details.
- **Tasks:** track assignment deadlines, priorities, and completion state.
- **Attendance:** record attended and total classes and see attendance percentages.
- **Study Center:** manage subjects and weekly goals, save revision notes, and use a 25-minute Pomodoro timer.
- **AI Tutor:** ask questions through a local Ollama service using `llama3.2:3b`.

## Technology

- Python 3.14 for the current macOS build
- PySide6 for the native desktop interface
- SQLite for per-user local data
- PyInstaller for the standalone macOS app bundle
- Ollama for optional local AI responses

## Run and build

Run the source version by installing `requirements.txt` and starting `main.py`. To build the macOS app, install `requirements-dev.txt` and run `./build_macos.sh`. That produces an app bundle and an architecture-labeled ZIP under `dist/`.

The current artifact is `dist/CampusMate-macOS-arm64.zip`, built for Apple silicon. Users with other Mac architectures need a build for their architecture. The app is not Developer ID signed or notarized, so macOS may require users to Control-click and choose **Open** on first launch.

The AI Tutor is optional. It requires Ollama and the `llama3.2:3b` model running on the same computer; schedule, tasks, attendance, notes, and the timer work without it. CampusMate has no accounts, cloud sync, or shared server database, so each user manages their own local records.

## Publishing status

The macOS release and source are published in the clean public repository [CampusMate-Desktop](https://github.com/meaditya1012-sketch/CampusMate-Desktop). This repository starts with a fresh, reviewed source snapshot and does not carry over the local database, old backups, or the development repository's commit history.

## Next steps for a public launch

1. Consider Apple Developer ID signing and notarization to make installation easier for people who download the app.
2. Build separately for Intel Macs if that architecture needs support.
3. If a browser-accessible product is required, build a web interface and hosted data/API layer; this project is currently a native desktop application.
