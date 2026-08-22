from sqlalchemy import create_engine, inspect, text, MetaData, Table
from typing import Dict, Any, List


class DBDataInspector:
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        self.inspector = inspect(self.engine)

    def check_connection(self) -> bool:
        """Проверка доступности БД."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    def get_tables_overview(self) -> List[Dict[str, Any]]:
        """Собирает общую аналитику по всем таблицам базы данных."""
        tables_data = []
        table_names = self.inspector.get_table_names()

        with self.engine.connect() as conn:
            for table_name in table_names:
                # 1. Общее количество строк
                count_query = text(f'SELECT COUNT(*) FROM "{table_name}"')
                total_rows = conn.execute(count_query).scalar() or 0

                # 2. Анализ столбцов на NULL
                columns = self.inspector.get_columns(table_name)
                null_stats = {}
                total_nulls_in_table = 0

                for col in columns:
                    col_name = col['name']
                    null_query = text(
                        f'SELECT COUNT(*) FROM "{table_name}" WHERE "{col_name}" IS NULL'
                    )
                    null_count = conn.execute(null_query).scalar() or 0

                    if null_count > 0:
                        null_stats[col_name] = null_count
                        total_nulls_in_table += null_count

                # 3. Расчет % полноты данных (Completeness Metric)
                total_cells = total_rows * len(columns) if columns else 0
                completeness_score = (
                    round(((total_cells - total_nulls_in_table) / total_cells) * 100, 2)
                    if total_cells > 0 else 100.0
                )

                tables_data.append({
                    'table_name': table_name,
                    'total_rows': total_rows,
                    'columns_count': len(columns),
                    'null_stats': null_stats,
                    'total_nulls': total_nulls_in_table,
                    'completeness_pct': completeness_score,
                    'status': 'WARNING' if total_nulls_in_table > 0 else 'OK'
                })

        return tables_data