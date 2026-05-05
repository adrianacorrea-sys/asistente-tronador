import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()

def test_db():
    try:
        # Aquí Kiro debe poner tus credenciales reales del .env
        conn = cx_Oracle.connect(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_DSN")
        )
        print(" CONEXIÓN EXITOSA A ORACLE")
        cursor = conn.cursor()
        print("Simulando ejecución de SQL dinámico...")
        print(f"Fecha servidor Oracle: {cursor.fetchone()}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(" ERROR DE CONEXIÓN:")
        print(e)

if __name__ == "__main__":
    test_db()