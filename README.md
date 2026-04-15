# PARCIAL FINAL CORTE 2 - CAFETERÍA U. SABANA

**Estudiante:** Lukas Blanco

## Descripción general
Este repositorio implementa el flujo completo solicitado en la rúbrica:

1. Generación de los 3 CSV sucios.
2. Carga de CSV en Pandas.
3. Limpieza, estandarización y normalización (1NF, 2NF, 3NF).
4. Exportación de los 3 CSV limpios.
5. Migración a SQLite.
6. Creación de tabla `ventas` con PK/FK.
7. Ejecución de operaciones CRUD (`INSERT`, `SELECT + JOIN`, `UPDATE`, `DELETE`).

Además, se aplicó el **BONO de arquitectura**, usando modularización en varios archivos `.py` y Programación Orientada a Objetos.

## Estructura del proyecto
- `main.py`: ejecuta todo el pipeline de extremo a extremo.
- `cafeteria_etl/data_generator.py`: crea los CSV sucios a partir de los datos del enunciado.
- `cafeteria_etl/data_cleaner.py`: aplica limpieza y normalización en Pandas.
- `cafeteria_etl/database_manager.py`: crea la arquitectura SQL y ejecuta CRUD.
- `operaciones_crud_ventas.sql`: script SQL de referencia para la fase de ventas.
- `parcial_2_*.csv`: datasets sucios y limpios.
- `parcial_2_cafeteria.db`: base de datos final con 4 tablas (`productos`, `clientes`, `proveedores`, `ventas`).

## Reglas de limpieza y normalización aplicadas

### Productos
- Separación de `producto_categoria` en `producto` y `categoria` (1NF).
- Estandarización de texto en formato título.
- Limpieza de `$` en precios y conversión a numérico.
- Imputación de `stock` nulo con mediana.
- Fecha de vencimiento en formato `YYYY-MM-DD`.

### Clientes
- Separación de `cliente_tipo` en `nombre_cliente` y `tipo_cliente` (1NF).
- Estandarización de mayúsculas/minúsculas.
- Corrección de `telefono` nulo a `"No Registra"`.
- Imputación de `email` faltante con valor lógico derivado del nombre.
- Eliminación de `edad` por ser dato derivado de `fecha_nacimiento` (3NF).

### Proveedores
- Separación de `empresa_ciudad` en `empresa` y `ciudad` (1NF).
- Estandarización de `contacto`, `empresa` y `ciudad`.
- Manejo de nulos en `contacto`, `telefono` y `email`.
- Renombrado de `nit_proveedor` a `id_proveedor` para integridad referencial.

## Ejecución
Desde la raíz del proyecto:

```bash
python3 main.py
```

Esto genera automáticamente todos los entregables solicitados.

## Evidencia de cumplimiento de rúbrica
- **Carga y exportación (0.5):** se generan 3 CSV sucios y 3 CSV limpios.
- **Limpieza y normalización Pandas (1.5):** manejo de nulos, tipos y normalización de columnas combinadas.
- **Migración a SQLite (1.0):** creación y carga de `parcial_2_cafeteria.db`.
- **Arquitectura y CRUD SQL (1.5):** tabla `ventas` con PK/FK + `INSERT`, `SELECT` con `JOIN`, `UPDATE`, `DELETE`.
- **Autogestión GitHub (0.5):** estructura documentada y trazable.
- **BONO (+1.0):** solución modular en `.py` usando POO.
