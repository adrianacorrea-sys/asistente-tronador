#!/usr/bin/env python3
"""
Explorar todos los schemas y tablas disponibles en Tronador
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
    print(f"User: {os.getenv('ORACLE_USER')}")
    
    try:
        with conn.cursor() as cur:
            # Verificar el usuario actual
            cur.execute("SELECT USER FROM DUAL")
            user = cur.fetchone()
            print(f"\nUsuario actual: {user[0]}")
            
            # Verificar tablas accesibles
            print("\n" + "="*60)
            print("TABLAS EN ALL_TABLES (accesibles al usuario)")
            print("="*60)
            
            cur.execute("""
                SELECT DISTINCT owner, table_name 
                FROM all_tables 
                WHERE ROWNUM <= 100
                ORDER BY owner, table_name
            """)
            tablas = cur.fetchall()
            
            print(f"\nTotal de tablas accesibles: {len(tablas)}\n")
            
            owners = {}
            for owner, table_name in tablas:
                if owner not in owners:
                    owners[owner] = []
                owners[owner].append(table_name)
            
            for owner, tables in sorted(owners.items())[:20]:  # Mostrar primeros 20 owners
                print(f"\nOWNER: {owner} ({len(tables)} tablas)")
                for t in tables[:15]:  # Mostrar primeras 15 tablas por owner
                    print(f"  - {t}")
                if len(tables) > 15:
                    print(f"  ... y {len(tables) - 15} más")
            
            # Guardar en archivo
            with open('tronador_all_tables.txt', 'w', encoding='utf-8') as f:
                f.write("TODAS LAS TABLAS ACCESIBLES EN TRONADOR\n")
                f.write("="*60 + "\n\n")
                f.write(f"Total de tablas: {len(tablas)}\n\n")
                
                for owner, tables in sorted(owners.items()):
                    f.write(f"\nOWNER: {owner}\n")
                    f.write("-"*40 + "\n")
                    for t in tables:
                        f.write(f"  {t}\n")
            
            print("\n✅ Listado guardado en tronador_all_tables.txt")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
