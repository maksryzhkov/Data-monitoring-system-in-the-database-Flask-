import subprocess
from flask import Blueprint, render_template, jsonify, current_app
from app.inspector import DBDataInspector
from app.alerts import TelegramNotifier

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    inspector = DBDataInspector(db_uri)
    tables_data = inspector.get_tables_overview()
    return render_template('dashboard.html', tables=tables_data)


@main_bp.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    inspector = DBDataInspector(db_uri)
    is_alive = inspector.check_connection()
    status = "OK" if is_alive else "CRITICAL"
    return jsonify({"status": status, "db_connected": is_alive}), 200 if is_alive else 500


@main_bp.route('/api/v1/run-tests', methods=['GET'])
def run_tests_api():
    """Эндпоинт для запуска юнит-тестов (pytest) прямо из приложения."""
    try:
        result = subprocess.run(["pytest", "tests/test_inspector.py"], capture_output=True, text=True)
        success = result.returncode == 0
        return jsonify({
            "status": "SUCCESS" if success else "FAILED",
            "exit_code": result.returncode,
            "output": result.stdout
        }), 200
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500


@main_bp.route('/api/v1/scan', methods=['POST', 'GET'])
def run_scan():
    db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    inspector = DBDataInspector(db_uri)
    tables_data = inspector.get_tables_overview()

    threshold = 90.0
    anomalies = [t for t in tables_data if t['completeness_pct'] < threshold]

    if anomalies:
        notifier = TelegramNotifier()
        alert_msg = "<b>Внимание! Обнаружены аномалии в БД:</b>\n\n"
        for a in anomalies:
            alert_msg += f"• Таблица <b>{a['table_name']}</b>: Полнота {a['completeness_pct']}% (NULLs: {a['total_nulls']})\n"
        notifier.send_alert(alert_msg)

    return jsonify({
        "status": "SUCCESS",
        "scanned_tables": len(tables_data),
        "anomalies_found": len(anomalies),
        "details": anomalies
    }), 200