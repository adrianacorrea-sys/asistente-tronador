#!/usr/bin/env python3
"""
Script para explorar tablas reales de Tronador (no tablas del sistema)
"""
import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_oracle():
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
        print(f"❌ Error: {e}")
        raise

def main():
    conn = conectar_oracle()
    print("✅ Conectado a Tronador")
    
    try:
        with conn.cursor() as cur:
            # Buscar tablas que no sean del sistema (no empiezan con SYS, C__, UET$, etc.)
            cur.execute("""
                SELECT table_name 
                FROM all_tables 
                WHERE owner = 'DEV_1001118079'
                AND table_name NOT LIKE 'SYS%'
                AND table_name NOT LIKE 'C%'
                AND table_name NOT LIKE 'UET$'
                AND table_name NOT LIKE 'SEG$'
                AND table_name NOT LIKE 'TS$'
                AND table_name NOT LIKE 'FILE$'
                AND table_name NOT LIKE 'PROXY%'
                AND table_name NOT LIKE 'CDEF$'
                AND table_name NOT LIKE 'CCOL$'
                AND table_name NOT LIKE 'UGROUP$'
                AND table_name NOT LIKE 'SYN$'
                AND table_name NOT LIKE 'VIEW$'
                AND table_name NOT LIKE 'TYPED_VIEW$'
                AND table_name NOT LIKE 'SUPEROBJ$'
                AND table_name NOT LIKE 'SEQ$'
                AND table_name NOT LIKE 'PROCEDURE%'
                AND table_name NOT LIKE 'ARGUMENT$'
                AND table_name NOT LIKE 'SOURCE$'
                AND table_name NOT LIKE 'IDL_%'
                AND table_name NOT LIKE 'DIR$'
                AND table_name NOT LIKE 'ERROR$'
                AND table_name NOT LIKE 'SETTINGS$'
                AND table_name NOT LIKE 'RESOURCE%'
                AND table_name NOT LIKE 'TRIGGER%'
                AND table_name NOT LIKE 'REG$'
                AND table_name NOT LIKE 'LOC$'
                AND table_name NOT LIKE 'OBJ%'
                AND table_name NOT LIKE 'DEFROLE$'
                AND table_name NOT LIKE 'PROF%'
                AND table_name NOT LIKE 'DEPENDENCY$'
                AND table_name NOT LIKE 'ACCESS$'
                AND table_name NOT LIKE 'LINK$'
                AND table_name NOT LIKE 'TRUSTED_LIST$'
                AND table_name NOT LIKE 'PROPS$'
                AND table_name NOT LIKE 'COM$'
                ORDER BY table_name
            """)
            tablas = cur.fetchall()
            
            print(f"\n📊 Tablas reales encontradas: {len(tablas)}\n")
            
            for (table_name,) in tablas:
                print(f"📋 {table_name}")
                
                # Obtener columnas de cada tabla
                try:
                    cur.execute(f"""
                        SELECT column_name, data_type, data_length, nullable
                        FROM all_tab_columns
                        WHERE table_name = :table_name
                        AND owner = 'DEV_1001118079'
                        ORDER BY column_id
                    """, table_name=table_name)
                    columnas = cur.fetchall()
                    
                    if columnas:
                        print(f"   Columnas ({len(columnas)}):")
                        for col in columnas[:10]:  # Mostrar primeras 10
                            col_name, col_type, col_len, nullable = col
                            print(f"     - {col_name} ({col_type}, len={col_len})")
                        if len(columnas) > 10:
                            print(f"     ... y {len(columnas) - 10} más")
                except Exception as e:
                    print(f"   Error leyendo columnas: {e}")
                
                print()
            
            # Guardar en archivo
            with open('tronador_tables.txt', 'w', encoding='utf-8') as f:
                f.write("TABLAS DE TRONADOR (DEV_1001118079)\n")
                f.write("="*60 + "\n\n")
                f.write(f"Total de tablas: {len(tablas)}\n\n")
                
                for (table_name,) in tablas:
                    f.write(f"TABLE: {table_name}\n")
                    f.write("-"*40 + "\n")
                    
                    try:
                        cur.execute(f"""
                            SELECT column_name, data_type, data_length, nullable, data_default
                            FROM all_tab_columns
                            WHERE table_name = :table_name
                            AND owner = 'DEV_1001118079'
                            ORDER BY column_id
                        """, table_name=table_name)
                        columnas = cur.fetchall()
                        
                        for col in columnas:
                            col_name, col_type, col_len, nullable, default = col
                            f.write(f"  {col_name} | {col_type} | len={col_len} | null={nullable} | default={default}\n")
                    except Exception as e:
                        f.write(f"  Error: {e}\n")
                    
                    f.write("\n")
            
            print("\n✅ Esquema guardado en tronador_tables.txt")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
