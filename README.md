# CampusMate

CampusMate is a desktop organizer for students, with a dashboard, class schedule, task list, attendance tracker, study notes, a Pomodoro timer, and an optional AI Tutor.

## Download

Get the latest macOS app from the [CampusMate Releases page](https://github.com/meaditya1012-sketch/CampusMate-Desktop/releases/latest). The current build is for Apple silicon. It is not Developer ID signed or notarized, so macOS may ask you to Control-click the app and choose **Open** the first time.

## Run from source

Requires Python and `pip`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

CampusMate creates its SQLite tables on first launch. When run from source, its database lives beside `main.py`.

## AI Tutor setup

The AI Tutor connects to Ollama on the same computer and uses `llama3.2:3b`. The rest of CampusMate works without Ollama.

1. Install Ollama from [ollama.com](https://ollama.com/).
2. Download the model with `ollama pull llama3.2:3b`.
3. Start Ollama, then open CampusMate's AI Tutor.

## Build a downloadable macOS app

Build on the Mac architecture you want to distribute (`arm64` for Apple silicon or `x86_64` for Intel). The build machine needs Python and Xcode Command Line Tools.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
./build_macos.sh
```

The build creates `dist/CampusMate.app` and a matching `dist/CampusMate-macOS-<architecture>.zip`. The app stores each user's database in macOS Application Support. Build separately on each Mac architecture you want to support.

This build is not signed with an Apple Developer ID or notarized. macOS may warn users the first time they open it; they can Control-click the app and choose **Open**. Apple Developer signing and notarization are needed for a smoother first launch.

For a first-run walkthrough, unzip the download, drag `CampusMate.app` to Applications, then open it. If macOS blocks the app, Control-click it and choose **Open**.
