#!/usr/bin/env python3
"""
Explorar sinónimos y tablas reales en Tronador
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
            # Verificar sinónimos
            print("\n" + "="*60)
            print("SINÓNIMOS DISPONIBLES")
            print("="*60)
            
            cur.execute("""
                SELECT synonym_name, table_owner, table_name
                FROM all_synonyms
                WHERE owner = 'PUBLIC' OR owner = 'DEV_1001118079'
                ORDER BY synonym_name
            """)
            sinonimos = cur.fetchall()
            
            print(f"\nTotal de sinónimos: {len(sinonimos)}\n")
            
            for syn_name, table_owner, table_name in sinonimos[:50]:
                print(f"  {syn_name} -> {table_owner}.{table_name}")
            
            # Verificar tablas en el owner actual
            print("\n" + "="*60)
            print("TABLAS EN USER_TABLES (owner actual)")
            print("="*60)
            
            cur.execute("""
                SELECT table_name FROM user_tables ORDER BY table_name
            """)
            user_tables = cur.fetchall()
            
            print(f"\nTablas en user_tables: {len(user_tables)}\n")
            for (table_name,) in user_tables:
                print(f"  - {table_name}")
            
            # Verificar tablas con owner diferente
            print("\n" + "="*60)
            print("TABLAS EN ALL_TABLES (con owner diferente)")
            print("="*60)
            
            cur.execute("""
                SELECT DISTINCT owner, table_name
                FROM all_tables
                WHERE owner != 'SYS'
                AND owner != 'DEV_1001118079'
                AND table_name NOT LIKE 'BIN$%'
                ORDER BY owner, table_name
            """)
            other_tables = cur.fetchall()
            
            print(f"\nTablas con owner diferente: {len(other_tables)}\n")
            
            owners = {}
            for owner, table_name in other_tables:
                if owner not in owners:
                    owners[owner] = []
                owners[owner].append(table_name)
            
            for owner, tables in sorted(owners.items())[:30]:
                print(f"\nOWNER: {owner} ({len(tables)} tablas)")
                for t in tables[:20]:
                    print(f"  - {t}")
                if len(tables) > 20:
                    print(f"  ... y {len(tables) - 20} más")
            
            # Guardar
            with open('tronador_synonyms_and_tables.txt', 'w', encoding='utf-8') as f:
                f.write("SINÓNIMOS Y TABLAS EN TRONADOR\n")
                f.write("="*60 + "\n\n")
                
                f.write(f"Total de sinónimos: {len(sinonimos)}\n\n")
                for syn_name, table_owner, table_name in sinonimos:
                    f.write(f"{syn_name} -> {table_owner}.{table_name}\n")
                
                f.write("\n\nTABLAS EN USER_TABLES: " + str(len(user_tables)) + "\n")
                for (table_name,) in user_tables:
                    f.write(f"  - {table_name}\n")
                
                f.write("\n\nTABLAS CON OWNER DIFERENTE: " + str(len(other_tables)) + "\n")
                for owner, tables in sorted(owners.items()):
                    f.write(f"\nOWNER: {owner}\n")
                    for t in tables:
                        f.write(f"  - {t}\n")
            
            print("\n✅ Resultados guardados en tronador_synonyms_and_tables.txt")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
