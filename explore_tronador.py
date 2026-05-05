    #!/usr/bin/env python3
"""
Script para explorar la estructura real de Tronador (Oracle)
Obtiene tablas, columnas y relaciones reales
"""
import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_oracle():
    """Conexión a Tronador"""
    try:
        conn = oracledb.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=oracledb.makedsn(
                os.getenv("ORACLE_HOST"), 
                int(os.getenv("ORACLE_PORT")), 
                service_name=os.getenv("ORACLE_SERVICE_NAME")
            )
        )
        return conn
    except Exception as e:
        print(f"❌ Error conectando a Oracle: {e}")
        raise

def obtener_tablas(conn):
    """Obtiene todas las tablas accesibles"""
    query = """
        SELECT table_name, 
               CASE WHEN temporary = 'Y' THEN 'TEMP' ELSE 'PERM' END as tipo,
               num_rows
        FROM all_tables 
        WHERE owner = 'DEV_1001118079'
        ORDER BY table_name
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Error obteniendo tablas: {e}")
        return []

def obtener_columnas(conn, table_name):
    """Obtiene columnas de una tabla específica"""
    query = """
        SELECT column_name, 
               data_type, 
               data_length,
               nullable,
               data_default
        FROM all_cons_columns acc
        JOIN all_constraints ac ON acc.constraint_name = ac.constraint_name
        WHERE ac.table_name = :table_name
        AND ac.owner = 'DEV_1001118079'
        AND ac.constraint_type = 'P'
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, table_name=table_name)
            return cur.fetchall()
    except Exception as e:
        print(f"Error obteniendo columnas de {table_name}: {e}")
        return []

def obtener_esquema_completo(conn):
    """Obtiene el esquema completo de la base de datos"""
    print("\n" + "="*80)
    print("ESQUEMA DE TRONADOR (DEV_1001118079)")
    print("="*80 + "\n")
    
    tablas = obtener_tablas(conn)
    
    if not tablas:
        print("No se encontraron tablas. Intentando con all_tables sin filtro de owner...")
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT table_name FROM all_tables WHERE ROWNUM <= 50")
                tablas = cur.fetchall()
                print(f"\nTablas encontradas ({len(tablas)}):")
                for t in tablas:
                    print(f"  - {t[0]}")
                return
        except Exception as e:
            print(f"Error: {e}")
            return
    
    print(f"Total de tablas: {len(tablas)}\n")
    
    for table_name, tipo, num_rows in tablas[:30]:  # Mostrar primeras 30
        print(f"\n{'─'*60}")
        print(f"TABLE: {table_name}")
        print(f"Type: {tipo} | Rows: {num_rows}")
        print(f"{'─'*60}")
        
        # Obtener columnas
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT column_name, data_type, data_length, nullable, data_default
                    FROM all_tab_columns
                    WHERE table_name = :table_name
                    AND owner = 'DEV_1001118079'
                    ORDER BY column_id
                """, table_name=table_name)
                columnas = cur.fetchall()
                
                if columnas:
                    print(f"\n{'Column':<30} {'Type':<20} {'Len':<8} {'Null':<8} Default")
                    print("-"*80)
                    for col in columnas:
                        col_name, col_type, col_len, nullable, default = col
                        print(f"{col_name:<30} {col_type:<20} {col_len or 0:<8} {nullable:<8} {default or ''}")
        except Exception as e:
            print(f"Error leyendo columnas: {e}")

def main():
    print("🔍 Explorando Tronador (Oracle)...")
    conn = conectar_oracle()
    print("✅ Conectado a Tronador")
    
    try:
        obtener_esquema_completo(conn)
    finally:
        conn.close()
        print("\n✅ Conexión cerrada")

if __name__ == "__main__":
    main()
