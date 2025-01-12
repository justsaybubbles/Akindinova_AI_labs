from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QTextEdit, QLabel, QWidget
from text_generator import load_tokenizer_and_model, generate_text, load_config
from typing import Optional, List, Tuple


class TextGeneratorApp(QWidget):
    def __init__(self, config_files: List[str]):
        super().__init__()
        self.setWindowTitle("Генератор текста с несколькими ruGPT")
        self.setGeometry(100, 100, 1000, 800)

        # Загружаем конфигурации и модели
        self.models = []
        self.tokenizers = []
        for config_file in config_files:
            config = load_config(config_file)
            tokenizer, model = load_tokenizer_and_model(config["model_name"])
            if tokenizer and model:
                self.models.append(model)
                self.tokenizers.append(tokenizer)
            else:
                self.models.append(None)
                self.tokenizers.append(None)

        if not all(self.models):
            self.display_error("Ошибка: одна или несколько моделей не были загружены.")
            return

        # Создаем интерфейс
        self.layout = QVBoxLayout()

        self.input_label = QLabel("Введите начальный текст:")
        self.layout.addWidget(self.input_label)

        self.input_text = QTextEdit()
        self.layout.addWidget(self.input_text)

        self.generate_button = QPushButton("Сгенерировать текст")
        self.generate_button.clicked.connect(self.generate_text)
        self.layout.addWidget(self.generate_button)

        self.output_labels = []
        self.output_texts = []
        self.time_labels = []

        for i in range(len(config_files)):
            output_label = QLabel(f"Ответ от модели {i + 1}:")
            self.output_labels.append(output_label)
            self.layout.addWidget(output_label)

            output_text = QTextEdit()
            output_text.setReadOnly(True)
            self.output_texts.append(output_text)
            self.layout.addWidget(output_text)

            time_label = QLabel("Время ответа: 0.0 секунд")
            self.time_labels.append(time_label)
            self.layout.addWidget(time_label)

        self.setLayout(self.layout)

    def display_error(self, message: str):
        for output_text in self.output_texts:
            output_text.setPlainText(message)

    def generate_text(self):
        input_text = self.input_text.toPlainText().strip()
        if not input_text:
            self.display_error("Введите текст для генерации.")
            return

        for i, (model, tokenizer) in enumerate(zip(self.models, self.tokenizers)):
            if model and tokenizer:
                try:
                    config = load_config(f"config{i + 1}.yaml")
                    generated_text, generation_time = generate_text(model, tokenizer, input_text, config)
                    self.output_texts[i].setPlainText(generated_text)
                    self.time_labels[i].setText(f"Время ответа: {generation_time:.2f} секунд")
                except Exception as e:
                    self.output_texts[i].setPlainText(f"Ошибка при генерации текста: {e}")
                    self.time_labels[i].setText("Время ответа: ошибка")
            else:
                self.output_texts[i].setPlainText("Модель не была загружена.")
                self.time_labels[i].setText("Время ответа: недоступно")
