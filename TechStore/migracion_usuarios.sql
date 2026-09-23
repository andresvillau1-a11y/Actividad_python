-- ============================================================
-- MIGRACIÓN: Modificación de la tabla usuarios (Parte 2)
-- Agrega el campo telefono y el rol 'Cliente'
-- Ejecutar UNA sola vez en la base de datos techstore
-- ============================================================

USE techstore;

-- 1. Agregar el campo telefono después de correo (si no existe)
-- MySQL no soporta "ADD COLUMN IF NOT EXISTS" en todas las versiones,
-- por eso se verifica primero en information_schema.
SET @existe_telefono = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = 'techstore'
      AND TABLE_NAME = 'usuarios'
      AND COLUMN_NAME = 'telefono'
);

SET @sql = IF(@existe_telefono = 0,
    'ALTER TABLE usuarios ADD COLUMN telefono VARCHAR(20) NULL AFTER correo',
    'SELECT "El campo telefono ya existe, no se duplica" AS aviso'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 2. Agregar el rol 'Cliente' al ENUM (sin quitar 'Administrador')
SET @enum_actual = (
    SELECT COLUMN_TYPE
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = 'techstore'
      AND TABLE_NAME = 'usuarios'
      AND COLUMN_NAME = 'rol'
);

SET @sql = IF(@enum_actual NOT LIKE '%Cliente%',
    CONCAT('ALTER TABLE usuarios MODIFY rol ENUM(''Administrador'', ''Cliente'') DEFAULT ''Administrador'''),
    'SELECT "El rol Cliente ya existe, no se duplica" AS aviso'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificación
DESCRIBE usuarios;
