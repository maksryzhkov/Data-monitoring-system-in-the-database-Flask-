import os
import sys
import subprocess
import json
from datetime import datetime

LOG_FILE = "project_audit.log"


def write_header(f, title):
    f.write(f"\n{'=' * 70}\n")
    f.write(f" {title.upper()}\n")
    f.write(f"{'=' * 70}\n")


def run_audit():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"Data Quality Monitor (DQM) - Full System Audit\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Python Executable: {sys.executable}\n")
        f.write(f"Python Version: {sys.version}\n")

        # 1. Проверка директорий и файлов
        write_header(f, "1. File System Structure")
        expected_files = [
            "app/__init__.py",
            "app/config.py",
            "app/inspector.py",
            "app/alerts.py",
            "app/bot_setup.py",
            "app/routes.py",
            "app/templates/dashboard.html",
            "app/static/style.css",
            "tests/test_inspector.py",
            "instance/test_data.db",
            "create_test_db.py",
            "generate_report_assets.py",
            "main.py",
            "requirements.txt",
            "README.md",
            ".env"
        ]

        for filepath in expected_files:
            exists = os.path.exists(filepath)
            status = "EXISTS" if exists else "MISSING"
            size = f"({os.path.getsize(filepath)} bytes)" if exists else ""
            f.write(f"[{status:<7}] {filepath} {size}\n")

        # 2. Проверка зависимостей (requirements.txt)
        write_header(f, "2. Python Packages Audit")
        try:
            installed = subprocess.check_output([sys.executable, "-m", "pip", "list"], text=True)
            f.write("Installed Packages:\n")
            f.write(installed)
        except Exception as e:
            f.write(f"Error checking pip list: {e}\n")

        # 3. Импорт ключевых моделей
        write_header(f, "3. Module Import Test")
        modules_to_test = [
            "flask", "sqlalchemy", "requests", "pytest",
            "matplotlib", "seaborn", "pandas", "dotenv"
        ]
        for mod in modules_to_test:
            try:
                __import__(mod)
                f.write(f"[SUCCESS] Import '{mod}'\n")
            except ImportError as ie:
                f.write(f"[FAILED]  Import '{mod}': {ie}\n")

        # 4. Проверка соединений с базой данных
        write_header(f, "4. Database Connection & Schema Test")
        try:
            from app.inspector import DBDataInspector
            db_path = os.path.abspath("instance/test_data.db")
            inspector = DBDataInspector(f"sqlite:///{db_path}")
            tables = inspector.get_tables_overview()
            f.write(f"Connected to DB successfully.\n")
            f.write(f"Scanned Tables Count: {len(tables)}\n")
            f.write(json.dumps(tables, indent=2, ensure_ascii=False))
            f.write("\n")
        except Exception as e:
            f.write(f"[ERROR] DB Inspection Failed: {e}\n")

        # 5. Запуск PYTEST
        write_header(f, "5. Pytest Execution Output")
        try:
            test_res = subprocess.run([sys.executable, "-m", "pytest", "tests/test_inspector.py"], capture_output=True,
                                      text=True)
            f.write(f"Pytest Return Code: {test_res.returncode}\n")
            f.write("STDOUT:\n" + test_res.stdout + "\n")
            if test_res.stderr:
                f.write("STDERR:\n" + test_res.stderr + "\n")
        except Exception as e:
            f.write(f"[ERROR] Pytest execution failed: {e}\n")

        # 6. Проверка сегнерированных ассетов
        write_header(f, "6. Presentation Assets Inspection")
        assets_dir = "presentation_assets"
        if os.path.exists(assets_dir):
            for file in os.listdir(assets_dir):
                f.write(f"Asset File: {file} ({os.path.getsize(os.path.join(assets_dir, file))} bytes)\n")
        else:
            f.write("Folder 'presentation_assets' does not exist yet. Run generate_report_assets.py.\n")

    print(f"Полная проверка завершена! Лог сохранен в файл: {LOG_FILE}")


if __name__ == "__main__":
    run_audit()