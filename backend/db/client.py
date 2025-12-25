"""
Tinybird/ClickHouse database client.
"""
import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()


class DatabaseClient:
    """
    Client for executing queries against Tinybird/ClickHouse.
    """
    
    def __init__(self):
        host = os.environ["TB_CLICKHOUSE_HOST"]
        token = os.environ["TINYBIRD_TOKEN"]

        self.client = clickhouse_connect.get_client(
            host=host,
            port=443,
            username="default",
            password=token,
            secure=True,
            connect_timeout=10,
            send_receive_timeout=30,
        )

    def query(self, sql: str) -> dict:
        """
        Execute a SQL query and return results.
        
        Args:
            sql: SQL query string
            
        Returns:
            Dictionary with 'columns' and 'rows' keys
            
        Raises:
            Exception: If query execution fails
        """
        result = self.client.query(sql)
        return {
            "columns": result.column_names,
            "rows": result.result_rows,
        }

