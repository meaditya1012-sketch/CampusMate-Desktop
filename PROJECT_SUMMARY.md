# CampusMate — Project Summary

CampusMate is a desktop student organizer built with Python, PySide6, and SQLite. It brings class planning, coursework, attendance, study notes, focus sessions, and an optional AI tutor into one desktop app.

## How the project grew

### 1. Student organizer foundation

The first version established the PySide6 desktop window and SQLite database. It introduced the core schedule, task, and attendance screens so students could enter and review their own information.

### 2. Study features and visual direction

The next iteration added the dashboard, Study Center, Pomodoro timer, revision notes, and an AI Tutor screen backed by a local Ollama model. An early dark interface established the sidebar and card layout.

### 3. Product and macOS release preparation

The product pass replaced the dark prototype styling with a calmer light interface, refined navigation, cards, and page headers, and improved the Study Center scrolling layout. The dashboard foregrounds the day’s classes and upcoming tasks. The Mac screens now follow the phone app's card layouts and actions for schedule, tasks, attendance, study subjects, notes, and focus time. The desktop app also retains its local Ollama AI Tutor. The project includes a CampusMate app icon and macOS build. Packaged builds store each user's database in macOS Application Support, while source runs continue to use the project folder.

The phone-friendly installable web app brings the dashboard, schedule, tasks, attendance, study subjects, revision notes, and focus timer to a browser. It can be added to an iPhone or Android home screen and saves each tester's information in that browser's local storage. It does not provide accounts, cloud sync, or the local Ollama connection used by the desktop AI Tutor.

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
- HTML, CSS, and JavaScript for the phone-friendly browser preview

## Run and build

Run the source version by installing `requirements.txt` and starting `main.py`. To build the macOS app, install `requirements-dev.txt` and run `./build_macos.sh`. That produces an app bundle and an architecture-labeled ZIP under `dist/`.

The current artifact is `dist/CampusMate-macOS-arm64.zip`, built for Apple silicon. Users with other Mac architectures need a build for their architecture. The app is not Developer ID signed or notarized, so macOS may require users to Control-click and choose **Open** on first launch.

The AI Tutor is optional. It requires Ollama and the `llama3.2:3b` model running on the same computer; schedule, tasks, attendance, notes, and the timer work without it. CampusMate has no accounts, cloud sync, or shared server database, so each user manages their own local records.

## Publishing status

The app and its clean source snapshot are publicly available in [CampusMate-Desktop](https://github.com/meaditya1012-sketch/CampusMate-Desktop). The [installable web app](https://meaditya1012-sketch.github.io/CampusMate-Desktop/) is intended for phone browser testing; the latest Apple silicon build is attached to the [GitHub Releases page](https://github.com/meaditya1012-sketch/CampusMate-Desktop/releases/latest). The original development repository remains private because its older history contains a tracked database and backup artifacts.

## Next steps for a public launch

1. Consider Apple Developer ID signing and notarization to make installation easier for people who download the app.
2. Build separately for Intel Macs if that architecture needs support.
3. Add accounts and a hosted data service if people need their Mac and phone records to synchronize.
