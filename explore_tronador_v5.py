#!/usr/bin/env python3
"""
Explorar tablas específicas de interés para el sistema de soporte
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
    
    # Tablas de interés basadas en los resultados anteriores
    tablas_interes = [
        ('BEAN', 'AGREEMENTS'),
        ('BEAN', 'POLIZAS'),
        ('BEAN', 'ASEGURADOS'),
        ('BEAN', 'PRODUCTOS'),
        ('BEAN', 'SINIESTROS'),
        ('BEAN', 'PAGOS'),
        ('BEAN', 'CLIENTES'),
        ('BEAN', 'CONTRATOS'),
        ('BEAN', 'COBERTURAS'),
        ('BEAN', 'BENEFICIARIOS'),
        ('BEAN', 'PAGOS_TRABAJADORES'),
        ('BEAN', 'PAGOS_INDEPENDIENTES'),
        ('BEAN', 'EMPRESAS'),
        ('BEAN', 'TERCEROS'),
        ('BEAN', 'SUCURSALES'),
        ('BEAN', 'AGENTES'),
        ('BEAN', 'RAMOS'),
        ('BEAN', 'FORMAS_PAGO'),
        ('BEAN', 'ESTADOS'),
        ('BEAN', 'TIPOS_DOCUMENTO'),
    ]
    
    try:
        with conn.cursor() as cur:
            print("\n" + "="*80)
            print("TABLAS DE INTERÉS PARA EL SISTEMA DE SOPORTE")
            print("="*80)
            
            for owner, table_name in tablas_interes:
                print(f"\n{'─'*80}")
                print(f"OWNER: {owner} | TABLE: {table_name}")
                print(f"{'─'*80}")
                
                try:
                    # Verificar si la tabla existe
                    cur.execute("""
                        SELECT table_name FROM all_tables 
                        WHERE owner = :owner AND table_name = :table_name
                    """, owner=owner, table_name=table_name)
                    result = cur.fetchone()
                    
                    if not result:
                        print(f"  ⚠️  Tabla no encontrada")
                        continue
                    
                    # Obtener columnas
                    cur.execute("""
                        SELECT column_name, data_type, data_length, nullable, data_default
                        FROM all_tab_columns
                        WHERE owner = :owner AND table_name = :table_name
                        ORDER BY column_id
                    """, owner=owner, table_name=table_name)
                    columnas = cur.fetchall()
                    
                    print(f"\n  Columnas ({len(columnas)}):")
                    for col in columnas[:20]:  # Mostrar primeras 20
                        col_name, col_type, col_len, nullable, default = col
                        print(f"    {col_name:<30} {col_type:<20} len={col_len or 0:<5} null={nullable}")
                    
                    if len(columnas) > 20:
                        print(f"    ... y {len(columnas) - 20} más")
                    
                    # Obtener conteo de filas
                    try:
                        cur.execute(f"SELECT COUNT(*) FROM {owner}.{table_name}")
                        count = cur.fetchone()[0]
                        print(f"\n  Total de filas: {count:,}")
                    except Exception as e:
                        print(f"\n  Error contando filas: {e}")
                        
                except Exception as e:
                    print(f"  Error: {e}")
            
            # Guardar en archivo
            with open('tronador_tables_interes.txt', 'w', encoding='utf-8') as f:
                f.write("TABLAS DE INTERÉS PARA EL SISTEMA DE SOPORTE\n")
                f.write("="*80 + "\n\n")
                
                for owner, table_name in tablas_interes:
                    f.write(f"\nOWNER: {owner} | TABLE: {table_name}\n")
                    f.write("-"*60 + "\n")
                    
                    try:
                        cur.execute("""
                            SELECT column_name, data_type, data_length, nullable, data_default
                            FROM all_tab_columns
                            WHERE owner = :owner AND table_name = :table_name
                            ORDER BY column_id
                        """, owner=owner, table_name=table_name)
                        columnas = cur.fetchall()
                        
                        f.write(f"\nColumnas ({len(columnas)}):\n")
                        for col in columnas:
                            col_name, col_type, col_len, nullable, default = col
                            f.write(f"  {col_name} | {col_type} | len={col_len} | null={nullable} | default={default}\n")
                        
                        try:
                            cur.execute(f"SELECT COUNT(*) FROM {owner}.{table_name}")
                            count = cur.fetchone()[0]
                            f.write(f"\nTotal de filas: {count:,}\n")
                        except Exception as e:
                            f.write(f"\nError contando filas: {e}\n")
                            
                    except Exception as e:
                        f.write(f"Error: {e}\n")
            
            print("\n✅ Resultados guardados en tronador_tables_interes.txt")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
