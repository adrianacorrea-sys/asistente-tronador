#!/usr/bin/env python3
"""
Explorar más tablas de BEAN y otros schemas
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
            # Buscar tablas que contengan palabras clave relevantes
            print("\n" + "="*80)
            print("TABLAS RELACIONADAS CON SOPORTE TÉCNICO")
            print("="*80)
            
            # Buscar tablas con nombres que sugieran contenido técnico
            keywords = ['ERROR', 'LOG', 'AUDIT', 'SOPORTE', 'INCIDENTE', 'TICKET', 
                       'SOLICITUD', 'AYUDA', 'HELP', 'SISTEMA', 'TECNICO', 'PROBLEMA',
                       'EXCEPTION', 'TRACE', 'DEBUG', 'REPORT', 'STATS']
            
            for keyword in keywords:
                try:
                    cur.execute(f"""
                        SELECT DISTINCT owner, table_name 
                        FROM all_tables 
                        WHERE table_name LIKE '%{keyword}%'
                        AND owner != 'SYS'
                        AND owner != 'DEV_1001118079'
                        ORDER BY owner, table_name
                    """)
                    results = cur.fetchall()
                    
                    if results:
                        print(f"\n🔍 KEYWORD: {keyword}")
                        for owner, table_name in results[:10]:
                            print(f"  {owner}.{table_name}")
                except Exception as e:
                    pass
            
            # Buscar tablas con columnas que sugieran contenido técnico
            print("\n" + "="*80)
            print("TABLAS CON COLUMNAS DE SOPORTE")
            print("="*80)
            
            column_keywords = ['ERROR', 'EXCEPTION', 'LOG', 'AUDIT', 'INCIDENT', 
                             'SOLICITUD', 'TICKET', 'PROBLEMA', 'AYUDA']
            
            for col_keyword in column_keywords:
                try:
                    cur.execute(f"""
                        SELECT DISTINCT tc.owner, tc.table_name, tc.column_name
                        FROM all_tab_columns tc
                        JOIN all_tables t ON tc.owner = t.owner AND tc.table_name = t.table_name
                        WHERE tc.column_name LIKE '%{col_keyword}%'
                        AND tc.owner != 'SYS'
                        AND tc.owner != 'DEV_1001118079'
                        ORDER BY tc.owner, tc.table_name
                    """)
                    results = cur.fetchall()
                    
                    if results:
                        print(f"\n🔍 COLUMN KEYWORD: {col_keyword}")
                        for owner, table_name, col_name in results[:15]:
                            print(f"  {owner}.{table_name}.{col_name}")
                except Exception as e:
                    pass
            
            # Explorar tablas específicas de BEAN que sí existen
            print("\n" + "="*80)
            print("TABLAS DE BEAN - ESTRUCTURA DETALLADA")
            print("="*80)
            
            bean_tables = ['ASEGURADOS', 'PRODUCTOS', 'CONTRATOS', 'POLIZAS', 'SINIESTROS', 
                          'PAGOS', 'CLIENTES', 'COBERTURAS', 'BENEFICIARIOS', 'EMPRESAS',
                          'TERCEROS', 'SUCURSALES', 'AGENTES', 'RAMOS', 'FORMAS_PAGO',
                          'ESTADOS', 'TIPOS_DOCUMENTO', 'TIPOS_SANGUINEO', 'TIPOS_VIVIENDA',
                          'TIPOS_OCUPACION', 'TIPOS_NIVEL_EDUCATIVO']
            
            for table_name in bean_tables:
                try:
                    cur.execute("""
                        SELECT table_name FROM all_tables 
                        WHERE owner = 'BEAN' AND table_name = :table_name
                    """, table_name=table_name)
                    result = cur.fetchone()
                    
                    if result:
                        print(f"\n{'─'*60}")
                        print(f"TABLE: BEAN.{table_name}")
                        print(f"{'─'*60}")
                        
                        cur.execute("""
                            SELECT column_name, data_type, data_length, nullable, data_default
                            FROM all_tab_columns
                            WHERE owner = 'BEAN' AND table_name = :table_name
                            ORDER BY column_id
                        """, table_name=table_name)
                        columnas = cur.fetchall()
                        
                        print(f"\nColumnas ({len(columnas)}):")
                        for col in columnas[:30]:
                            col_name, col_type, col_len, nullable, default = col
                            print(f"  {col_name:<30} {col_type:<20} len={col_len or 0:<5} null={nullable}")
                        
                        if len(columnas) > 30:
                            print(f"  ... y {len(columnas) - 30} más")
                        
                        try:
                            cur.execute(f"SELECT COUNT(*) FROM BEAN.{table_name}")
                            count = cur.fetchone()[0]
                            print(f"\nTotal de filas: {count:,}")
                        except Exception as e:
                            print(f"\nError contando filas: {e}")
                            
                except Exception as e:
                    pass
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
