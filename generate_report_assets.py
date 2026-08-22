import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.inspector import DBDataInspector

OUTPUT_DIR = "presentation_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

db_path = os.path.abspath("instance/test_data.db")
db_uri = f"sqlite:///{db_path}"

print("1. Анализ базы данных и генерация метрик...")
inspector = DBDataInspector(db_uri)
data = inspector.get_tables_overview()

df = pd.DataFrame(data)
df['total_cells'] = df['total_rows'] * df['columns_count']

report_df = df[['table_name', 'total_rows', 'columns_count', 'total_nulls', 'completeness_pct', 'status']]
report_df.columns = ['Таблица', 'Всего строк', 'Колонок', 'Всего NULL', 'Полнота (%)', 'Статус']

report_df.to_csv(f"{OUTPUT_DIR}/data_quality_metrics.csv", index=False)
report_df.to_markdown(f"{OUTPUT_DIR}/data_quality_metrics.md", index=False)
print(f"Таблица сохранена в `{OUTPUT_DIR}/data_quality_metrics.md`")

print("2. Генерация диаграммы полноты данных (Chart 1)...")
plt.figure(figsize=(8, 5))
colors = {'OK': '#2ecc71', 'WARNING': '#f39c12'}

ax = sns.barplot(
    x='Таблица', y='Полнота (%)', hue='Статус', data=report_df,
    palette=colors, dodge=False
)
plt.title('Метрика Completeness Score (%) по таблицам БД', fontsize=14, fontweight='bold', pad=15)
plt.ylim(0, 110)
plt.axhline(90, color='red', linestyle='--', label='Порог аномалии (90%)')

for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f'{height:.1f}%',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=11, fontweight='bold', xytext=(0, 3),
                    textcoords='offset points')

plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/completeness_chart.png", dpi=300)
plt.close()
print(f"График сохранен в `{OUTPUT_DIR}/completeness_chart.png`")

print("3. Генерация диаграммы времени обнаружения ошибок (Chart 2)...")
mttd_data = pd.DataFrame({
    'Метод': ['Ручной контроль\n(Василий)', 'Автоматический DQM\n(Flask App)'],
    'Время обнаружения (секунды)': [86400, 0.3]
})

plt.figure(figsize=(7, 5))
ax2 = sns.barplot(
    x='Метод', y='Время обнаружения (секунды)', hue='Метод', data=mttd_data,
    palette=['#e74c3c', '#2ecc71'], legend=False
)
plt.yscale('log')
plt.ylim(0.01, 5000000)  # Увеличен верхний предел, чтобы надпись не заезжала за рамки
plt.title('Сравнение времени обнаружения аномалий (MTTD)', fontsize=13, fontweight='bold', pad=15)
plt.ylabel('Время в секундах (лог. шкала)')

for p in ax2.patches:
    height = p.get_height()
    label = "~24 часа" if height > 100 else "< 0.3 сек"
    ax2.annotate(label,
                 (p.get_x() + p.get_width() / 2., height),
                 ha='center', va='bottom', fontsize=11, fontweight='bold', xytext=(0, 5),
                 textcoords='offset points')

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/mttd_comparison.png", dpi=300)
plt.close()
print(f"График сохранен в `{OUTPUT_DIR}/mttd_comparison.png`")

print("4. Запуск юнит-тестов и фиксация отчета...")
test_output = subprocess.check_output(["pytest", "tests/test_inspector.py"], text=True)

with open(f"{OUTPUT_DIR}/pytest_report.txt", "w", encoding="utf-8") as f:
    f.write(test_output)

print(f"Отчет Pytest сохранен в `{OUTPUT_DIR}/pytest_report.txt`!")
print(f"\nВсе материалы успешно сгенерированы без ошибок и предупреждений!")