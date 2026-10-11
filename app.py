import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

st.set_page_config(page_title="TaskPilot AI", page_icon="🧭", layout="wide")

st.title("🧭 TaskPilot AI")
st.caption("Turn your task list into a clear, manageable action plan.")
st.info("This starter version uses transparent, rule-based prioritization. It does not call an external AI model.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

def priority_score(task):
    """Higher score means the task should be considered sooner."""
    today = date.today()
    days_left = (task["Deadline"] - today).days
    urgency = 50 if days_left < 0 else 40 if days_left == 0 else 30 if days_left <= 2 else 20 if days_left <= 7 else 10
    importance = {"High": 30, "Medium": 20, "Low": 10}.get(task["Importance"], 10)
    effort = max(1, int(task["Estimated hours"]))
    # Slightly favor tasks that can be completed quickly when other factors are equal.
    quick_finish_bonus = max(0, 8 - effort)
    return urgency + importance + quick_finish_bonus

def status_label(task):
    if task["Status"] == "Completed":
        return "Completed"
    if task["Deadline"] < date.today():
        return "Overdue"
    if task["Deadline"] <= date.today() + timedelta(days=2):
        return "Due soon"
    return "Upcoming"

with st.sidebar:
    st.header("➕ Add a task")
    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task name", placeholder="e.g., Finish Python assignment")
        deadline = st.date_input("Deadline", value=date.today() + timedelta(days=1))
        importance = st.selectbox("Importance", ["High", "Medium", "Low"])
        hours = st.number_input("Estimated hours", min_value=1, max_value=100, value=2, step=1)
        notes = st.text_area("Notes (optional)", placeholder="What needs to be done?")
        submitted = st.form_submit_button("Add task", use_container_width=True)
        if submitted:
            if not title.strip():
                st.error("Please enter a task name.")
            else:
                st.session_state.tasks.append({
                    "ID": max([t["ID"] for t in st.session_state.tasks], default=0) + 1,
                    "Task": title.strip(),
                    "Deadline": deadline,
                    "Importance": importance,
                    "Estimated hours": int(hours),
                    "Notes": notes.strip(),
                    "Status": "Pending",
                })
                st.success("Task added.")

    st.divider()
    st.header("🗓️ Plan settings")
    available_hours = st.number_input("Hours available today", min_value=1, max_value=24, value=3)
    st.caption("The suggested plan fits tasks into the available hours as closely as possible.")

tasks = st.session_state.tasks
if not tasks:
    st.subheader("Get started")
    st.write("Add your first task from the sidebar, or load the example tasks below.")
    if st.button("Load example tasks"):
        today = date.today()
        examples = [
            ("Complete laboratory record", 0, "High", 1, "Finish calculations and sign-off."),
            ("Finish Python assignment", 1, "High", 2, "Complete and test the code."),
            ("Prepare project presentation", 2, "Medium", 2, "Create slides and rehearse."),
            ("Revise thermodynamics", 4, "Medium", 3, "Review key concepts and practice questions."),
        ]
        for name, offset, imp, hrs, note in examples:
            st.session_state.tasks.append({
                "ID": max([t["ID"] for t in st.session_state.tasks], default=0) + 1,
                "Task": name, "Deadline": today + timedelta(days=offset),
                "Importance": imp, "Estimated hours": hrs, "Notes": note, "Status": "Pending"
            })
        st.rerun()
    st.stop()

df = pd.DataFrame(tasks)
total = len(tasks)
completed = sum(t["Status"] == "Completed" for t in tasks)
pending = total - completed
overdue = sum(t["Status"] != "Completed" and t["Deadline"] < date.today() for t in tasks)
progress = completed / total if total else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total tasks", total)
m2.metric("Pending", pending)
m3.metric("Overdue", overdue)
m4.metric("Completion", f"{progress:.0%}")
st.progress(progress)

st.subheader("📋 Your tasks")
display = []
for task in tasks:
    display.append({
        "Task": task["Task"],
        "Deadline": task["Deadline"].strftime("%d %b %Y"),
        "Importance": task["Importance"],
        "Estimated hours": task["Estimated hours"],
        "Status": status_label(task),
        "Progress": task["Status"],
    })
st.dataframe(pd.DataFrame(display), use_container_width=True, hide_index=True)

st.subheader("⚡ Smart priority list")
active_tasks = [t for t in tasks if t["Status"] != "Completed"]
ranked = sorted(active_tasks, key=lambda t: (-priority_score(t), t["Deadline"], t["Task"].lower()))
if not ranked:
    st.success("All tasks are completed. Great work!")
else:
    for index, task in enumerate(ranked, start=1):
        days = (task["Deadline"] - date.today()).days
        if days < 0:
            timing = f"{abs(days)} day(s) overdue"
        elif days == 0:
            timing = "Due today"
        elif days == 1:
            timing = "Due tomorrow"
        else:
            timing = f"Due in {days} days"
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"**{index}. {task['Task']}**")
            col1.caption(f"{timing} · {task['Importance']} importance · {task['Estimated hours']} hour(s)")
            col2.metric("Priority", priority_score(task))

st.subheader("🗓️ Suggested plan for today")
remaining_hours = int(available_hours)
planned = []
for task in ranked:
    effort = int(task["Estimated hours"])
    if effort <= remaining_hours:
        planned.append(task)
        remaining_hours -= effort
if planned:
    for i, task in enumerate(planned, start=1):
        st.write(f"**{i}. {task['Task']}** — {task['Estimated hours']} hour(s)")
    st.caption(f"Planned {available_hours - remaining_hours} of {available_hours} available hour(s).")
else:
    st.warning("No full task fits the available time. Increase today's hours or break a task into smaller steps.")

st.subheader("✅ Update task status")
task_options = {f"{t['ID']} — {t['Task']}": t["ID"] for t in tasks}
selected_label = st.selectbox("Choose a task", list(task_options.keys()))
selected_id = task_options[selected_label]
selected_task = next(t for t in tasks if t["ID"] == selected_id)
new_status = st.radio("Status", ["Pending", "Completed"], horizontal=True, index=1 if selected_task["Status"] == "Completed" else 0)
c1, c2 = st.columns(2)
with c1:
    if st.button("Save status", use_container_width=True):
        selected_task["Status"] = new_status
        st.rerun()
with c2:
    if st.button("Delete selected task", type="secondary", use_container_width=True):
        st.session_state.tasks = [t for t in tasks if t["ID"] != selected_id]
        st.rerun()

st.subheader("📤 Export")
export_df = pd.DataFrame(st.session_state.tasks)
if not export_df.empty:
    export_df["Deadline"] = export_df["Deadline"].astype(str)
    st.download_button(
        "Download tasks as CSV",
        data=export_df.to_csv(index=False).encode("utf-8"),
        file_name="taskpilot_tasks.csv",
        mime="text/csv",
        use_container_width=False,
    )

st.caption("TaskPilot AI · Student productivity prototype · Review suggested priorities and adjust them to your needs.")
