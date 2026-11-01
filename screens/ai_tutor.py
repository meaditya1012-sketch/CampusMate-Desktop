
import json
import urllib.request
import urllib.error

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QPlainTextEdit, QMessageBox
)


MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/chat"


class AIWorker(QThread):
    response_ready = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, messages):
        super().__init__()
        self.messages = messages

    def run(self):
        try:
            payload = {
                "model": MODEL,
                "messages": self.messages,
                "stream": False
            }

            request = urllib.request.Request(
                OLLAMA_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(
                request, timeout=180
            ) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            answer = result.get("message", {}).get(
                "content", ""
            ).strip()

            if answer:
                self.response_ready.emit(answer)
            else:
                self.error_occurred.emit(
                    "Ollama returned an empty response."
                )

        except urllib.error.URLError as error:
            self.error_occurred.emit(
                f"Could not connect to Ollama:\n{error}\n\n"
                "Check that Ollama is running."
            )
        except Exception as error:
            self.error_occurred.emit(str(error))


class AITutorScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("aiTutorScreen")

        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are CampusMate AI Tutor, a helpful tutor "
                    "for first-year engineering students. Explain "
                    "concepts in simple language, show steps for "
                    "calculations, give examples, and encourage "
                    "understanding. If you are unsure, say so."
                )
            }
        ]

        self.worker = None
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 28, 34, 26)
        layout.setSpacing(13)

        header_row = QHBoxLayout()
        header_row.setSpacing(14)

        heading_group = QVBoxLayout()
        heading_group.setSpacing(4)
        heading = QLabel("AI Tutor")
        heading.setObjectName("pageTitle")

        subtitle = QLabel("A patient study partner, ready when you are.")
        subtitle.setObjectName("pageSubtitle")
        heading_group.addWidget(heading)
        heading_group.addWidget(subtitle)
        header_row.addLayout(heading_group, 1)

        model_badge = QLabel(f"●  Local model  ·  {MODEL}")
        model_badge.setObjectName("modelBadge")
        model_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_row.addWidget(model_badge, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(header_row)

        prompt_row = QHBoxLayout()
        prompt_row.setSpacing(8)
        for prompt in [
            "Explain a concept",
            "Walk me through a problem",
            "Quiz me",
        ]:
            prompt_button = QPushButton(prompt)
            prompt_button.setObjectName("promptButton")
            prompt_button.setCursor(Qt.CursorShape.PointingHandCursor)
            prompt_button.clicked.connect(
                lambda _checked=False, value=prompt: self.use_prompt(value)
            )
            prompt_row.addWidget(prompt_button)
        prompt_row.addStretch()
        layout.addLayout(prompt_row)

        self.chat_display = QPlainTextEdit()
        self.chat_display.setObjectName("aiChatDisplay")
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText(
            "Your conversation will appear here..."
        )
        layout.addWidget(self.chat_display, 1)

        input_row = QHBoxLayout()

        self.question_input = QLineEdit()
        self.question_input.setObjectName("aiQuestionInput")
        self.question_input.setPlaceholderText(
            "Ask a question about maths, physics, Python..."
        )
        self.question_input.returnPressed.connect(self.send_question)

        self.send_button = QPushButton("Send ➤")
        self.send_button.setObjectName("primaryButton")
        self.send_button.clicked.connect(self.send_question)

        input_row.addWidget(self.question_input, 1)
        input_row.addWidget(self.send_button)

        layout.addLayout(input_row)

        clear_button = QPushButton("Clear Chat")
        clear_button.setObjectName("secondaryButton")
        clear_button.clicked.connect(self.clear_chat)
        footer_row = QHBoxLayout()
        footer_row.addStretch()
        footer_row.addWidget(clear_button)
        layout.addLayout(footer_row)

        self.chat_display.appendPlainText(
            "CampusMate: Hi! I'm your AI Tutor. "
            "What would you like to learn today?\n"
        )

    def use_prompt(self, prompt):
        examples = {
            "Explain a concept": "Explain a difficult concept in simple steps.",
            "Walk me through a problem": "Walk me through this problem step by step: ",
            "Quiz me": "Quiz me on a topic and wait for my answer.",
        }
        self.question_input.setText(examples.get(prompt, prompt))
        self.question_input.setFocus()

    def send_question(self):
        question = self.question_input.text().strip()

        if not question:
            return

        if self.worker is not None and self.worker.isRunning():
            return

        self.chat_display.appendPlainText(
            f"You: {question}\n"
        )
        self.question_input.clear()

        self.messages.append({
            "role": "user",
            "content": question
        })

        self.send_button.setEnabled(False)
        self.send_button.setText("Thinking...")
        self.chat_display.appendPlainText(
            "CampusMate: Thinking...\n"
        )

        self.worker = AIWorker(list(self.messages))
        self.worker.response_ready.connect(self.show_response)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.start()

    def show_response(self, answer):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.BlockUnderCursor)

        if cursor.selectedText() == "CampusMate: Thinking...":
            cursor.removeSelectedText()
            cursor.deleteChar()

        self.chat_display.appendPlainText(
            f"CampusMate: {answer}\n"
        )

        self.messages.append({
            "role": "assistant",
            "content": answer
        })

        self.finish_request()

    def show_error(self, error):
        self.chat_display.appendPlainText(
            f"Error: {error}\n"
        )

        # Remove the unanswered question from conversation history.
        if self.messages and self.messages[-1]["role"] == "user":
            self.messages.pop()

        self.finish_request()

    def finish_request(self):
        self.send_button.setEnabled(True)
        self.send_button.setText("Send ➤")
        self.question_input.setFocus()

    def clear_chat(self):
        self.messages = self.messages[:1]
        self.chat_display.clear()
        self.chat_display.appendPlainText(
            "CampusMate: Chat cleared! What shall we learn next?\n"
        )
