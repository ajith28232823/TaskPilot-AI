# TaskPilot AI 🧭

**Turn your task list into a clear, manageable action plan.**

TaskPilot AI is a student productivity web app that helps users capture tasks, rank them by deadline and importance, create a simple plan for the day, and track progress.

> **Current implementation note:** This version uses a transparent rule-based priority score. It does not connect to an external AI model/API yet, so describe it as an automation/productivity prototype rather than claiming live generative-AI features.

## Features

- Add tasks with deadlines, importance, estimated effort, and notes
- Rule-based priority ranking
- Today-plan suggestion based on available hours
- Pending/completed tracking and progress dashboard
- Overdue and due-soon indicators
- CSV export
- Example tasks to test the app quickly

## Built with

- Python
- Streamlit
- Pandas

## Run locally

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Create a virtual environment (recommended):

   **Windows**
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the app:
   ```bash
   streamlit run app.py
   ```
7. Open the local address shown in your terminal (usually `http://localhost:8501`).

## Deploy online

You can deploy this app using Streamlit Community Cloud:

1. Push `app.py`, `requirements.txt`, and `README.md` to a **public GitHub repository**.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
4. Deploy, then test the public app URL.

## Priority logic

The demo assigns points based on deadline urgency and importance, with a small tie-breaker bonus for shorter tasks. The score is a transparent heuristic, not a trained machine-learning model. Users should review the generated plan and change priorities when necessary.

## Suggested demo flow

1. Click **Load example tasks**.
2. Show the dashboard metrics.
3. Add a task with a deadline today.
4. Show how the priority list changes.
5. Mark a task completed.
6. Download the CSV.

## Limitations and next steps

- Tasks are stored in the current app session; they are not yet saved permanently in a database.
- The schedule only fits whole tasks into available hours; it does not split tasks automatically.
- No external AI API is connected in this starter version.

Potential future improvements: persistent storage, calendar integration, reminders, task breakdown, and an AI model/API for natural-language planning.

## License

This project is provided for educational and hackathon prototyping. Add a license file if you want to specify reuse permissions.
