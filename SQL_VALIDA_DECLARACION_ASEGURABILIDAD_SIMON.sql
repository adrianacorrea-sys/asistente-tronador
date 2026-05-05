-- SQL para validar pólizas emitidas desde Simón Cotizador sin declaración de asegurabilidad
-- Caso: GD923-1404

-- Consulta para identificar pólizas sin declaración de asegurabilidad
SELECT 
    p.NUM_POL1,
    p.NUM_SECU_POL,
    p.COD_RAMO,
    p.COD_PROD,
    p.FECHA_EMI,
    p.SIM_SISTEMA_ORIGEN,
    e.EXC_DECLARACION_ASEGURABILIDAD,
    CASE 
        WHEN e.EXC_NUM_SECU_POL_H IS NULL THEN 'SIN DECLARACIÓN'
        ELSE 'CON DECLARACIÓN'
    END AS ESTADO_DECLARACION
FROM 
    OPS$PUMA.A2000030 p
LEFT JOIN 
    OPS$PUMA.SIM_EXCLUSIONES e ON p.NUM_SECU_POL = e.EXC_NUM_SECU_POL_H
WHERE 
    p.SIM_SISTEMA_ORIGEN IS NOT NULL  -- Pólizas emitidas desde Simón
    AND e.EXC_NUM_SECU_POL_H IS NULL  -- Sin declaración de asegurabilidad
    AND p.MCA_ANU_POL = 'N'           -- No anuladas
ORDER BY 
    p.FECHA_EMI DESC
FETCH FIRST 100 ROWS ONLY;

-- Consulta para contar pólizas sin declaración por fecha
SELECT 
    TRUNC(p.FECHA_EMI) AS FECHA_EMISION,
    COUNT(*) AS CANTIDAD_SIN_DECLARACION
FROM 
    OPS$PUMA.A2000030 p
LEFT JOIN 
    OPS$PUMA.SIM_EXCLUSIONES e ON p.NUM_SECU_POL = e.EXC_NUM_SECU_POL_H
WHERE 
    p.SIM_SISTEMA_ORIGEN IS NOT NULL
    AND e.EXC_NUM_SECU_POL_H IS NULL
    AND p.MCA_ANU_POL = 'N'
GROUP BY 
    TRUNC(p.FECHA_EMI)
ORDER BY 
    FECHA_EMISION DESC
FETCH FIRST 30 ROWS ONLY;

-- Consulta para ver la estructura de la tabla SIM_EXCLUSIONES
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    DATA_LENGTH,
    NULLABLE
FROM 
    ALL_TAB_COLUMNS
WHERE 
    OWNER = 'OPS$PUMA'
    AND TABLE_NAME = 'SIM_EXCLUSIONES'
ORDER BY 
    COLUMN_ID;

-- Consulta para ver la estructura de la tabla A2000030
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    DATA_LENGTH,
    NULLABLE
FROM 
    ALL_TAB_COLUMNS
WHERE 
    OWNER = 'OPS$PUMA'
    AND TABLE_NAME = 'A2000030'
ORDER BY 
    COLUMN_ID;
