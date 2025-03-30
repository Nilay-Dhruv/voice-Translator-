import sys
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout
from PyQt5.QtGui import QMovie, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)
        self.tts_engine.setProperty('rate', 140)

        self.greet_user()

    def initUI(self):
        self.setWindowTitle("Speech Translator")
        self.setGeometry(400, 200, 600, 500)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("black"))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.greeting_label = QLabel("", self)
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("color: yellow; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.greeting_label)

        lang_layout = QHBoxLayout()
        self.language_select = QComboBox(self)
        self.languages = {"Gujarati": "gu", "Hindi": "hi", "Spanish": "es", "French": "fr", "German": "de"}
        self.language_select.addItems(self.languages.keys())
        lang_layout.addStretch()
        lang_layout.addWidget(self.language_select)
        layout.addLayout(lang_layout)

        self.gif_label = QLabel(self)
        self.movie = QMovie("D:/projects/voice tranlator/b.gif")
        self.gif_label.setMovie(self.movie)
        self.gif_label.setScaledContents(True)
        self.movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)

        self.start_button = QPushButton("Start Listening", self)
        self.start_button.clicked.connect(self.start_listening)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.result_label = QLabel("Translation will appear here", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def greet_user(self):
        current_hour = datetime.datetime.now().hour

        if 5 <= current_hour < 12:
            greeting = "Good Morning, how may I help you!"
        elif 12 <= current_hour < 18:
            greeting = "Good Afternoon, how may I help you!"
        else:
            greeting = "Good Evening, how may I help you!"

        self.greeting_label.setText(greeting)
        QTimer.singleShot(500, lambda: self.speak_text(greeting))

    def start_listening(self):
        target_language = self.languages[self.language_select.currentText()]

        with sr.Microphone() as source:
            self.movie.start()
            self.result_label.setText("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
                self.result_label.setText(f"Translated: {translated_text}")

                QTimer.singleShot(200, lambda: self.speak_text(translated_text))

            except sr.UnknownValueError:
                self.result_label.setText("Could not understand the audio.")
            except sr.RequestError:
                self.result_label.setText("Speech Recognition service error.")
            except Exception as e:
                self.result_label.setText(f"Error: {e}")

    def speak_text(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        self.movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())
