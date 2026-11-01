# CampusMate

CampusMate is a student planner for Mac and phones, with a dashboard, class schedule, task list, attendance tracker, study notes, and a Pomodoro timer. The Mac app also includes an optional local AI Tutor.

![CampusMate dashboard preview](assets/campusmate-dashboard-preview.png)

## Try the phone-friendly web preview

Open the [CampusMate phone app](https://meaditya1012-sketch.github.io/CampusMate-Desktop/) in Safari or Chrome. On iPhone, use **Share → Add to Home Screen**; on Android, open Chrome's menu and choose **Install app** or **Add to Home screen**. It then opens from a home-screen icon. The Mac app and phone app use separate local data; records do not sync between them. The optional AI Tutor is currently available in the Mac app when Ollama is running locally.

## Download

Download the latest macOS app from the [public CampusMate-Desktop release](https://github.com/meaditya1012-sketch/CampusMate-Desktop/releases/latest). The current build is for Apple silicon. The app is not Developer ID signed or notarized, so macOS may ask you to Control-click it and choose **Open** the first time.

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

For a first-run walkthrough, unzip the download, drag `CampusMate.app` to Applications, then open it. If macOS blocks the app because it is not Developer ID signed, Control-click it and choose **Open**.
