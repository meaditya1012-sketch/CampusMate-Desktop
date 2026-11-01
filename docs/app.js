(() => {
  "use strict";

  const STORAGE_KEY = "campusmate.web.v1";
  const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const content = document.getElementById("content");
  const dialog = document.getElementById("dialog");
  const dialogContent = document.getElementById("dialog-content");
  const toastElement = document.getElementById("toast");
  const pages = {
    home: ["Home", "A clear view of your day."],
    schedule: ["Schedule", "Keep your week in view."],
    tasks: ["Tasks", "Make room for the work that matters."],
    study: ["Study Center", "Build steady progress, one session at a time."],
    attendance: ["Attendance", "Know where you stand in every subject."],
    tutor: ["AI Tutor", "A study partner for your questions."],
  };

  let currentPage = "home";
  let taskFilter = "open";
  let toastTimeout;
  let timerSeconds = 25 * 60;
  let timerInterval = null;

  function freshState() {
    return { classes: [], tasks: [], attendance: [], subjects: [], notes: [] };
  }

  function loadState() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
      if (!saved || typeof saved !== "object") return freshState();
      const empty = freshState();
      return Object.fromEntries(Object.keys(empty).map((key) => [
        key,
        Array.isArray(saved[key]) ? saved[key] : [],
      ]));
    } catch {
      return freshState();
    }
  }

  let state = loadState();

  function makeId() {
    return globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[character]);
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      return true;
    } catch {
      showToast("Could not save in this browser. Check available storage.");
      return false;
    }
  }

  function showToast(message) {
    toastElement.textContent = message;
    toastElement.classList.add("is-visible");
    window.clearTimeout(toastTimeout);
    toastTimeout = window.setTimeout(() => toastElement.classList.remove("is-visible"), 2600);
  }

  function todayName() {
    return new Intl.DateTimeFormat(undefined, { weekday: "long" }).format(new Date());
  }

  function todayLabel() {
    return new Intl.DateTimeFormat(undefined, {
      weekday: "long",
      month: "long",
      day: "numeric",
    }).format(new Date());
  }

  function formatDate(value, options = { month: "short", day: "numeric", year: "numeric" }) {
    if (!value) return "No due date";
    const parts = String(value).slice(0, 10).split("-").map(Number);
    if (parts.length !== 3 || parts.some(Number.isNaN)) return escapeHtml(value);
    const date = new Date(parts[0], parts[1] - 1, parts[2]);
    return new Intl.DateTimeFormat(undefined, options).format(date);
  }

  function formatTime(value) {
    if (!value || !/^\d{2}:\d{2}$/.test(value)) return escapeHtml(value || "");
    const [hour, minute] = value.split(":").map(Number);
    const suffix = hour >= 12 ? "PM" : "AM";
    return `${hour % 12 || 12}:${String(minute).padStart(2, "0")} ${suffix}`;
  }

  function fullTimeRange(item) {
    if (!item.startTime) return "Time not set";
    return `${formatTime(item.startTime)}${item.endTime ? ` – ${formatTime(item.endTime)}` : ""}`;
  }

  function sortedClasses(list = state.classes) {
    return [...list].sort((a, b) => {
      const dayOrder = DAYS.indexOf(a.day) - DAYS.indexOf(b.day);
      return dayOrder || String(a.startTime).localeCompare(String(b.startTime));
    });
  }

  function sortedTasks(list = state.tasks) {
    return [...list].sort((a, b) => {
      if (!a.dueDate) return b.dueDate ? 1 : 0;
      if (!b.dueDate) return -1;
      return a.dueDate.localeCompare(b.dueDate);
    });
  }

  function escapeMultiline(value) {
    return escapeHtml(value).replace(/\n/g, "<br>");
  }

  function emptyState(title, description, action = "") {
    return `<div class="empty-state">
      <span class="empty-mark" aria-hidden="true">✦</span>
      <div><h2 class="empty-title">${escapeHtml(title)}</h2>
      <p class="empty-copy">${escapeHtml(description)}</p>${action}</div>
    </div>`;
  }

  function pageHeader(title, subtitle, action = "") {
    return `<header class="page-heading"><div><h1 class="page-title">${escapeHtml(title)}</h1>
      <p class="page-subtitle">${escapeHtml(subtitle)}</p></div>${action ? `<div class="heading-actions">${action}</div>` : ""}</header>`;
  }

  function primaryAction(label, action, icon = "+") {
    return `<button class="button button-primary" type="button" data-action="${action}"><span aria-hidden="true">${icon}</span>${escapeHtml(label)}</button>`;
  }

  function classRow(item, compact = false) {
    const detail = [item.teacher, item.room ? `Room ${item.room}` : ""].filter(Boolean).join(" · ");
    if (compact) {
      return `<div class="list-row"><span class="row-dot">●</span><div class="row-copy">
        <div class="row-title">${escapeHtml(item.subject)}</div><div class="row-meta">${escapeHtml(detail || item.day)}</div>
      </div><div class="row-trailing">${escapeHtml(fullTimeRange(item))}</div></div>`;
    }
    return `<article class="schedule-item"><div class="schedule-time">${escapeHtml(fullTimeRange(item))}<span class="schedule-day">${escapeHtml(item.day)}</span></div>
      <div><div class="schedule-subject">${escapeHtml(item.subject)}</div><div class="schedule-detail">${escapeHtml(detail || "Class")}</div></div>
      <button class="button button-quiet button-icon" type="button" data-action="delete-class" data-id="${escapeHtml(item.id)}" aria-label="Remove ${escapeHtml(item.subject)}">×</button></article>`;
  }

  function taskRow(item, compact = false) {
    const complete = Boolean(item.completed);
    const priority = String(item.priority || "Medium").toLowerCase();
    const statusText = item.dueDate ? formatDate(item.dueDate, { month: "short", day: "numeric" }) : "No due date";
    if (compact) {
      return `<div class="list-row"><span class="row-dot amber">●</span><div class="row-copy">
        <div class="row-title">${escapeHtml(item.title)}</div><div class="row-meta">${escapeHtml(item.subject || "Assignment")}</div>
      </div><div class="row-trailing">${escapeHtml(statusText)}</div></div>`;
    }
    return `<article class="task-item${complete ? " is-complete" : ""}">
      <button class="task-toggle" type="button" data-action="toggle-task" data-id="${escapeHtml(item.id)}" aria-pressed="${complete}" aria-label="Mark ${escapeHtml(item.title)} ${complete ? "open" : "complete"}">${complete ? "✓" : ""}</button>
      <div class="task-copy"><div class="item-title">${escapeHtml(item.title)}</div><div class="item-detail">${escapeHtml(item.subject || "Assignment")} · ${escapeHtml(statusText)}</div></div>
      <span class="priority ${escapeHtml(priority)}">${escapeHtml(item.priority || "Medium")}</span>
      <button class="button button-quiet button-icon button-danger" type="button" data-action="delete-task" data-id="${escapeHtml(item.id)}" aria-label="Delete ${escapeHtml(item.title)}">×</button>
    </article>`;
  }

  function attendanceStatus(percent) {
    if (percent >= 75) return ["On track", "good"];
    if (percent >= 65) return ["Watch", "watch"];
    return ["At risk", "risk"];
  }

  function attendanceRow(item) {
    const total = Number(item.total) || 0;
    const attended = Number(item.attended) || 0;
    const percent = total ? (attended / total) * 100 : 0;
    const [status, statusClass] = attendanceStatus(percent);
    const width = Math.max(0, Math.min(100, percent));
    return `<article class="attendance-item"><div><div class="attendance-top"><div class="item-title">${escapeHtml(item.subject)}</div>
        <strong class="attendance-percent">${percent.toFixed(1)}%</strong></div>
        <div class="item-detail">${attended} attended out of ${total} classes</div>
        <div class="progress-track" role="progressbar" aria-label="${escapeHtml(item.subject)} attendance" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${width.toFixed(0)}"><div class="progress-fill" style="width:${width}%"></div></div>
      </div><div class="attendance-actions"><span class="status-pill ${statusClass}">${status}</span>
        <button class="button button-small" type="button" data-action="mark-present" data-id="${escapeHtml(item.id)}" aria-label="Mark one ${escapeHtml(item.subject)} class attended">Present</button>
        <button class="button button-small" type="button" data-action="mark-absent" data-id="${escapeHtml(item.id)}" aria-label="Mark one ${escapeHtml(item.subject)} class missed">Missed</button>
        <button class="button button-small" type="button" data-action="edit-attendance" data-id="${escapeHtml(item.id)}">Edit</button>
        <button class="button button-small button-quiet button-danger" type="button" data-action="delete-attendance" data-id="${escapeHtml(item.id)}" aria-label="Remove ${escapeHtml(item.subject)}">×</button>
      </div></article>`;
  }

  function subjectRow(item) {
    const goal = Number(item.goalHours) || 0;
    const completed = Number(item.completedHours) || 0;
    const percent = goal ? Math.min(100, Math.max(0, completed / goal * 100)) : 0;
    return `<article class="subject-item"><div class="subject-top"><div class="item-title">${escapeHtml(item.name)}</div><div class="subject-goal">${goal} hr${goal === 1 ? "" : "s"} / week</div></div>
      <div class="progress-track" aria-label="${escapeHtml(item.name)} study progress"><div class="progress-fill" style="width:${percent}%"></div></div>
      <div class="subject-progress-label"><span>${completed.toFixed(1)} hours studied</span><strong>${Math.round(percent)}%</strong></div>
      <button class="button button-small subject-add-time" type="button" data-action="add-study-time" data-id="${escapeHtml(item.id)}">+ 30 min</button>
    </article>`;
  }

  function noteRow(item) {
    const preview = String(item.content || "").slice(0, 110);
    return `<article class="note-item"><span class="note-icon" aria-hidden="true">▤</span><div class="note-copy">
      <button class="panel-link" type="button" data-action="open-note" data-id="${escapeHtml(item.id)}">${escapeHtml(item.title)}</button>
      <div class="row-meta">${escapeHtml(item.subject || "General")} · ${escapeHtml(formatDate(item.createdAt, { month: "short", day: "numeric" }))}</div>
      <div class="note-preview">${escapeHtml(preview)}</div></div>
      <button class="button button-quiet button-icon button-danger" type="button" data-action="delete-note" data-id="${escapeHtml(item.id)}" aria-label="Delete note ${escapeHtml(item.title)}">×</button></article>`;
  }

  function renderHome() {
    const classesToday = sortedClasses(state.classes.filter((item) => item.day === todayName()));
    const openTasks = sortedTasks(state.tasks.filter((item) => !item.completed));
    const average = state.attendance.length
      ? state.attendance.reduce((sum, item) => sum + (Number(item.total) ? Number(item.attended) / Number(item.total) * 100 : 0), 0) / state.attendance.length
      : null;
    const attendanceValue = average === null ? "—" : `${average.toFixed(0)}%`;

    const classContent = classesToday.length
      ? classesToday.slice(0, 4).map((item) => classRow(item, true)).join("")
      : `<p class="empty-copy">No classes today. Add a class to plan your week.</p>`;
    const taskContent = openTasks.length
      ? openTasks.slice(0, 4).map((item) => taskRow(item, true)).join("")
      : `<p class="empty-copy">You're all caught up. Enjoy the breathing room.</p>`;

    return `<section class="hero"><div class="hero-copy"><p class="hero-eyebrow">YOUR DAY, IN SYNC</p><h1>Make today count.</h1>
      <p class="hero-subtitle">Classes, coursework and focus time — all in one place.</p></div>
      <div class="hero-side"><span class="hero-date">${escapeHtml(todayLabel())}</span><button class="button" type="button" data-page="tutor">Ask your AI tutor →</button></div></section>
      <section class="stats-grid" aria-label="Your overview">
        <article class="stat-card"><p class="stat-label">Classes today</p><div class="stat-value">${classesToday.length}</div><div class="stat-accent"></div></article>
        <article class="stat-card mint"><p class="stat-label">Open tasks</p><div class="stat-value">${openTasks.length}</div><div class="stat-accent"></div></article>
        <article class="stat-card amber"><p class="stat-label">Attendance</p><div class="stat-value">${attendanceValue}</div><div class="stat-accent"></div></article>
      </section>
      <section class="dashboard-grid">
        <article class="panel"><div class="panel-header"><h2 class="panel-title">Today’s classes</h2><button class="panel-link" type="button" data-page="schedule">View schedule →</button></div>${classContent}</article>
        <article class="panel"><div class="panel-header"><h2 class="panel-title">Coming up</h2><button class="panel-link" type="button" data-page="tasks">All tasks →</button></div>${taskContent}</article>
      </section>`;
  }

  function renderSchedule() {
    const action = primaryAction("Add class", "add-class");
    const classes = sortedClasses();
    const list = classes.length
      ? `<div class="schedule-list">${classes.map((item) => classRow(item)).join("")}</div>`
      : emptyState("Your week is open", "Add your first class to start building a timetable.", primaryAction("Add a class", "add-class"));
    return `${pageHeader("Schedule", "Keep your week in view.", action)}${list}`;
  }

  function renderTasks() {
    const action = primaryAction("Add task", "add-task");
    const list = sortedTasks().filter((item) => {
      if (taskFilter === "open") return !item.completed;
      if (taskFilter === "done") return Boolean(item.completed);
      return true;
    });
    const body = list.length
      ? `<div class="task-list">${list.map((item) => taskRow(item)).join("")}</div>`
      : emptyState(taskFilter === "done" ? "No completed tasks yet" : "Your task list is clear", taskFilter === "done" ? "Finished tasks will show up here." : "Add an assignment or deadline and it will show up here.", taskFilter === "open" ? primaryAction("Add a task", "add-task") : "");
    return `${pageHeader("Tasks", "Make room for the work that matters.", action)}
      <div class="filter-row" role="group" aria-label="Filter tasks">
        <button class="filter-chip" type="button" data-filter="open" aria-pressed="${taskFilter === "open"}">Open</button>
        <button class="filter-chip" type="button" data-filter="all" aria-pressed="${taskFilter === "all"}">All</button>
        <button class="filter-chip" type="button" data-filter="done" aria-pressed="${taskFilter === "done"}">Completed</button>
      </div>${body}`;
  }

  function renderAttendance() {
    const action = primaryAction("Add subject", "add-attendance");
    const body = state.attendance.length
      ? `<div class="attendance-list">${[...state.attendance].sort((a, b) => a.subject.localeCompare(b.subject)).map(attendanceRow).join("")}</div>`
      : emptyState("Start tracking attendance", "Add a subject and log each class to see your progress.", primaryAction("Add a subject", "add-attendance"));
    return `${pageHeader("Attendance", "Know where you stand in every subject.", action)}${body}`;
  }

  function renderStudy() {
    const subjectPanel = `<section class="surface"><div class="surface-header"><h2 class="surface-title">My subjects</h2>${primaryAction("Add", "add-subject")}</div>
      ${state.subjects.length ? `<div class="subject-list">${[...state.subjects].sort((a, b) => a.name.localeCompare(b.name)).map(subjectRow).join("")}</div>` : emptyState("Choose what to focus on", "Add a subject and set a weekly study goal.", primaryAction("Add a subject", "add-subject"))}</section>`;
    const noteSubjectPanel = `<section class="surface"><div class="surface-header"><h2 class="surface-title">Study notes</h2>${primaryAction("New note", "add-note")}</div>
      ${state.notes.length ? `<div class="note-list">${[...state.notes].sort((a, b) => b.createdAt.localeCompare(a.createdAt)).map(noteRow).join("")}</div>` : emptyState("Keep your best ideas close", "Save a revision note so you can find it when you need it.", primaryAction("Write a note", "add-note"))}</section>`;
    const timerPanel = `<section class="surface timer-panel"><h2 class="surface-title">Pomodoro focus</h2><div id="timer-face" class="timer-face">${formatTimer()}</div>
      <p class="timer-caption">A focused 25-minute session, then a short break.</p><div class="timer-actions">
        <button class="button button-primary" type="button" data-action="timer-start">${timerInterval ? "Pause" : "Start focus"}</button>
        <button class="button" type="button" data-action="timer-reset">Reset</button></div></section>`;
    return `${pageHeader("Study Center", "Build steady progress, one session at a time.")}
      <div class="study-grid"><div class="study-column">${subjectPanel}${timerPanel}</div><div class="study-column">${noteSubjectPanel}</div></div>`;
  }

  function renderTutor() {
    return `${pageHeader("AI Tutor", "A study partner for your questions.")}
      <section class="tutor-card"><div class="tutor-mark" aria-hidden="true">✧</div><div>
        <h2>The phone preview keeps your questions private.</h2>
        <p>The desktop AI Tutor connects to Ollama running on the same computer. This browser demo has no AI service connected, so it does not send your questions anywhere.</p>
        <a class="button button-primary" href="https://github.com/meaditya1012-sketch/CampusMate-Desktop/releases/latest" target="_blank" rel="noopener">View the Mac app</a>
        <div class="prompt-suggestions" aria-label="Ideas to try in the desktop app"><span class="prompt-suggestion">Explain a concept</span><span class="prompt-suggestion">Walk through a problem</span><span class="prompt-suggestion">Quiz me</span></div>
      </div></section>`;
  }

  function render() {
    const page = pages[currentPage] || pages.home;
    document.title = `${page[0]} · CampusMate`;
    content.innerHTML = currentPage === "home" ? renderHome()
      : currentPage === "schedule" ? renderSchedule()
        : currentPage === "tasks" ? renderTasks()
          : currentPage === "attendance" ? renderAttendance()
            : currentPage === "study" ? renderStudy()
              : renderTutor();

    document.querySelectorAll("[data-page].nav-link").forEach((button) => {
      if (button.dataset.page === currentPage) button.setAttribute("aria-current", "page");
      else button.removeAttribute("aria-current");
    });
    if (currentPage === "study") updateTimerFace();
  }

  function navigate(page) {
    if (!pages[page]) return;
    currentPage = page;
    render();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  document.addEventListener("click", (event) => {
    const pageButton = event.target.closest("[data-page]");
    if (pageButton) {
      event.preventDefault();
      navigate(pageButton.dataset.page);
      return;
    }

    const filterButton = event.target.closest("[data-filter]");
    if (filterButton) {
      taskFilter = filterButton.dataset.filter;
      render();
      return;
    }

    const actionButton = event.target.closest("[data-action]");
    if (!actionButton) return;
    handleAction(actionButton.dataset.action, actionButton.dataset.id);
  });

  function confirmRemove(message) {
    return window.confirm(message);
  }

  function handleAction(action, id) {
    if (action === "add-class") return openForm("class");
    if (action === "add-task") return openForm("task");
    if (action === "add-attendance") return openForm("attendance");
    if (action === "add-subject") return openForm("subject");
    if (action === "add-note") return openForm("note");

    if (action === "toggle-task") {
      const task = state.tasks.find((item) => item.id === id);
      if (!task) return;
      task.completed = !task.completed;
      saveState();
      render();
      showToast(task.completed ? "Task completed." : "Task moved back to open.");
      return;
    }
    if (action === "delete-task") {
      const task = state.tasks.find((item) => item.id === id);
      if (!task || !confirmRemove(`Delete “${task.title}”?`)) return;
      state.tasks = state.tasks.filter((item) => item.id !== id);
      saveState(); render(); showToast("Task deleted."); return;
    }
    if (action === "delete-class") {
      const item = state.classes.find((entry) => entry.id === id);
      if (!item || !confirmRemove(`Remove ${item.subject} from your schedule?`)) return;
      state.classes = state.classes.filter((entry) => entry.id !== id);
      saveState(); render(); showToast("Class removed."); return;
    }
    if (action === "mark-present" || action === "mark-absent") {
      const item = state.attendance.find((entry) => entry.id === id);
      if (!item) return;
      item.total = Number(item.total) + 1;
      if (action === "mark-present") item.attended = Number(item.attended) + 1;
      saveState(); render(); showToast(action === "mark-present" ? "Attendance marked present." : "Attendance marked missed."); return;
    }
    if (action === "delete-attendance") {
      const item = state.attendance.find((entry) => entry.id === id);
      if (!item || !confirmRemove(`Remove attendance for ${item.subject}?`)) return;
      state.attendance = state.attendance.filter((entry) => entry.id !== id);
      saveState(); render(); showToast("Attendance record removed."); return;
    }
    if (action === "edit-attendance") {
      const item = state.attendance.find((entry) => entry.id === id);
      if (item) openForm("attendance", item);
      return;
    }
    if (action === "add-study-time") {
      const subject = state.subjects.find((item) => item.id === id);
      if (!subject) return;
      subject.completedHours = Number(subject.completedHours || 0) + 0.5;
      saveState(); render(); showToast("Added 30 minutes of study time."); return;
    }
    if (action === "open-note") {
      const note = state.notes.find((item) => item.id === id);
      if (note) openNote(note);
      return;
    }
    if (action === "delete-note") {
      const note = state.notes.find((item) => item.id === id);
      if (!note || !confirmRemove(`Delete the note “${note.title}”?`)) return;
      state.notes = state.notes.filter((item) => item.id !== id);
      saveState(); render(); showToast("Note deleted."); return;
    }
    if (action === "timer-start") {
      if (timerInterval) {
        window.clearInterval(timerInterval);
        timerInterval = null;
      } else {
        if (timerSeconds <= 0) timerSeconds = 25 * 60;
        timerInterval = window.setInterval(() => {
          timerSeconds = Math.max(0, timerSeconds - 1);
          updateTimerFace();
          if (timerSeconds === 0) {
            window.clearInterval(timerInterval);
            timerInterval = null;
            if ("vibrate" in navigator) navigator.vibrate([150, 80, 150]);
            showToast("Focus session complete. Nice work.");
            if (currentPage === "study") render();
          }
        }, 1000);
      }
      render(); return;
    }
    if (action === "timer-reset") {
      window.clearInterval(timerInterval);
      timerInterval = null;
      timerSeconds = 25 * 60;
      render(); return;
    }
  }

  function formatTimer() {
    const minutes = Math.floor(timerSeconds / 60);
    const seconds = timerSeconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
  }

  function updateTimerFace() {
    const face = document.getElementById("timer-face");
    if (face) face.textContent = formatTimer();
    const button = content.querySelector('[data-action="timer-start"]');
    if (button) button.textContent = timerInterval ? "Pause" : "Start focus";
  }

  function showDialog(title, subtitle, body, onSubmit) {
    dialogContent.innerHTML = `<form class="dialog-inner" id="entry-form"><header class="dialog-header"><div><h2 class="dialog-title">${escapeHtml(title)}</h2>${subtitle ? `<p class="dialog-subtitle">${escapeHtml(subtitle)}</p>` : ""}</div>
      <button class="button button-quiet button-icon" type="button" data-close-dialog aria-label="Close dialog">×</button></header>
      <div class="form-grid">${body}</div><div class="form-actions"><button class="button" type="button" data-close-dialog>Cancel</button><button class="button button-primary" type="submit">Save</button></div></form>`;
    const form = document.getElementById("entry-form");
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const result = onSubmit(Object.fromEntries(new FormData(form).entries()));
      if (result !== false) {
        dialog.close();
        render();
      }
    });
    dialog.showModal();
    form.querySelector("input, select, textarea")?.focus();
  }

  function field(name, label, type = "text", value = "", options = {}) {
    const full = options.full ? " full" : "";
    const required = options.required === false ? "" : " required";
    const min = options.min !== undefined ? ` min="${escapeHtml(options.min)}"` : "";
    const max = options.max !== undefined ? ` max="${escapeHtml(options.max)}"` : "";
    const step = options.step !== undefined ? ` step="${escapeHtml(options.step)}"` : "";
    const id = `field-${name}`;
    const input = options.choices
      ? `<select id="${id}" name="${name}"${required}>${options.choices.map((choice) => `<option value="${escapeHtml(choice.value)}"${choice.value === value ? " selected" : ""}>${escapeHtml(choice.label)}</option>`).join("")}</select>`
      : type === "textarea"
        ? `<textarea id="${id}" name="${name}" placeholder="${escapeHtml(options.placeholder || "")}"${required}>${escapeHtml(value)}</textarea>`
        : `<input id="${id}" name="${name}" type="${type}" value="${escapeHtml(value)}" placeholder="${escapeHtml(options.placeholder || "")}"${required}${min}${max}${step} />`;
    return `<div class="form-field${full}"><label for="${id}">${escapeHtml(label)}</label>${input}</div>`;
  }

  function openForm(kind, existing = null) {
    const item = existing || {};
    if (kind === "class") {
      const body = field("subject", "Subject", "text", item.subject || "", { placeholder: "e.g. Data Structures" })
        + field("teacher", "Teacher", "text", item.teacher || "", { required: false, placeholder: "e.g. Prof. Shah" })
        + field("day", "Day", "select", item.day || todayName(), { choices: DAYS.map((day) => ({ value: day, label: day })) })
        + field("startTime", "Starts", "time", item.startTime || "09:00")
        + field("endTime", "Ends", "time", item.endTime || "10:00")
        + field("room", "Room", "text", item.room || "", { required: false, placeholder: "e.g. B-204" });
      showDialog("Add a class", "Add the details you want to see in your timetable.", body, (values) => {
        if (values.startTime >= values.endTime) { showToast("End time must be later than start time."); return false; }
        state.classes.push({ id: makeId(), ...values });
        saveState(); showToast("Class added to your schedule.");
      });
      return;
    }
    if (kind === "task") {
      const body = field("title", "Task", "text", item.title || "", { full: true, placeholder: "e.g. Finish the lab report" })
        + field("subject", "Subject", "text", item.subject || "", { placeholder: "e.g. Physics", required: false })
        + field("dueDate", "Due date", "date", item.dueDate || "", { required: false })
        + field("priority", "Priority", "select", item.priority || "Medium", { choices: ["Low", "Medium", "High"].map((value) => ({ value, label: value })) });
      showDialog("Add a task", "Give your next piece of work a place on the list.", body, (values) => {
        state.tasks.push({ id: makeId(), completed: false, ...values });
        saveState(); showToast("Task added.");
      });
      return;
    }
    if (kind === "attendance") {
      const body = field("subject", "Subject", "text", item.subject || "", { full: true, placeholder: "e.g. Applied Mathematics" })
        + field("attended", "Classes attended", "number", item.attended ?? 0, { min: 0, step: 1 })
        + field("total", "Classes held", "number", item.total ?? 1, { min: 1, step: 1 });
      showDialog(item.id ? "Edit attendance" : "Add attendance", "Enter the classes you have attended so far.", body, (values) => {
        const attended = Number(values.attended);
        const total = Number(values.total);
        if (!Number.isInteger(attended) || !Number.isInteger(total) || total < 1 || attended < 0 || attended > total) {
          showToast("Use whole numbers, with attended classes no more than total classes.");
          return false;
        }
        const duplicate = state.attendance.find((entry) => entry.id !== item.id && entry.subject.toLowerCase() === values.subject.trim().toLowerCase());
        if (duplicate) { showToast("That subject is already being tracked. Edit its existing record."); return false; }
        if (item.id) Object.assign(item, { subject: values.subject.trim(), attended, total });
        else state.attendance.push({ id: makeId(), subject: values.subject.trim(), attended, total });
        saveState(); showToast("Attendance saved.");
      });
      return;
    }
    if (kind === "subject") {
      const body = field("name", "Subject", "text", item.name || "", { full: true, placeholder: "e.g. Linear Algebra" })
        + field("goalHours", "Weekly goal (hours)", "number", item.goalHours || 10, { min: 0.5, step: 0.5 });
      showDialog("Add a subject", "Set a small weekly target you can work toward.", body, (values) => {
        const goalHours = Number(values.goalHours);
        if (!Number.isFinite(goalHours) || goalHours <= 0) { showToast("Enter a weekly goal greater than zero."); return false; }
        if (state.subjects.some((entry) => entry.name.toLowerCase() === values.name.trim().toLowerCase())) { showToast("That subject is already in your study list."); return false; }
        state.subjects.push({ id: makeId(), name: values.name.trim(), goalHours, completedHours: 0 });
        saveState(); showToast("Subject added.");
      });
      return;
    }
    if (kind === "note") {
      const subjectChoices = [{ value: "", label: "General" }, ...state.subjects.map((subject) => ({ value: subject.name, label: subject.name }))];
      const body = field("title", "Note title", "text", "", { full: true, placeholder: "e.g. Key ideas from chapter 3" })
        + field("subject", "Subject", "select", "", { full: true, choices: subjectChoices })
        + field("content", "Your notes", "textarea", "", { full: true, placeholder: "Write a useful summary, formula, or question..." });
      showDialog("Write a study note", "Keep a helpful idea close for your next revision session.", body, (values) => {
        state.notes.push({ id: makeId(), title: values.title.trim(), subject: values.subject, content: values.content.trim(), createdAt: new Date().toISOString() });
        saveState(); showToast("Note saved on this device.");
      });
    }
  }

  function openNote(note) {
    dialogContent.innerHTML = `<div class="dialog-inner"><header class="dialog-header"><div><h2 class="dialog-title">${escapeHtml(note.title)}</h2><p class="dialog-subtitle">${escapeHtml(note.subject || "General")} · ${escapeHtml(formatDate(note.createdAt, { month: "long", day: "numeric", year: "numeric" }))}</p></div>
      <button class="button button-quiet button-icon" type="button" data-close-dialog aria-label="Close note">×</button></header><div class="note-body">${escapeMultiline(note.content)}</div></div>`;
    dialog.showModal();
  }

  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-close-dialog]")) dialog.close();
    if (event.target === dialog) dialog.close();
  });

  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", () => navigator.serviceWorker.register("./sw.js").catch(() => {}));
  }

  render();
})();
