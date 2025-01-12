import sys
from PyQt5.QtWidgets import QApplication
from interface import TextGeneratorApp

if __name__ == "__main__":
    config_files = ["/Users/jayanne/Desktop/Projects/AI/LR2/config1.yaml", "/Users/jayanne/Desktop/Projects/AI/LR2/config2.yaml", "/Users/jayanne/Desktop/Projects/AI/LR2/config3.yaml"]

    app = QApplication(sys.argv)
    try:
        window = TextGeneratorApp(config_files)
        window.show()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
    sys.exit(app.exec_())
