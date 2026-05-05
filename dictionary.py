# src/db/dictionary.py

TRONADOR_SCHEMA = "TRONADOR"

# Mapeo oficial de tablas y sus columnas reales
TABLE_MAP = {
    "CONTROL_TECNICO": {
        "table_name": "G2000200",
        "columns": {
            "regla": "COD_REGLA",
            "estado": "MCA_INACTIVA",
            "fecha": "FECHA_VAL",
            "id": "ID_REGISTRO"
        }
    },
    "POLIZAS": {
        "table_name": "A2000030",
        "columns": {
            "numero": "NUM_POL1",
            "secuencia": "NUM_SECU_POL",
            "anulacion": "MCA_ANU_POL",
            "ramo": "COD_RAMO"
        }
    }
}

def get_sql_verificar_regla(cod_regla: str):
    """Genera el SQL perfecto para Oracle sin errores"""
    t = TABLE_MAP["CONTROL_TECNICO"]
    sql = (
        f"SELECT {t['columns']['id']}, {t['columns']['regla']}, {t['columns']['estado']} "
        f"FROM {TRONADOR_SCHEMA}.{t['table_name']} "
        f"WHERE {t['columns']['regla']} = '{cod_regla}' "
        f"ORDER BY {t['columns']['fecha']} DESC "
        f"FETCH FIRST 10 ROWS ONLY"
    )
    return sql