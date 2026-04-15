"""Migración de DataFrames a SQLite y operaciones CRUD."""

from dataclasses import dataclass
from pathlib import Path
import sqlite3

import pandas as pd


@dataclass
class CafeteriaDBManager:
    """Gestiona la base de datos del parcial y las operaciones SQL."""

    db_path: Path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    def load_dimension_tables(
        self,
        productos: pd.DataFrame,
        clientes: pd.DataFrame,
        proveedores: pd.DataFrame,
    ) -> None:
        with self._connect() as conn:
            productos.to_sql("productos", conn, if_exists="replace", index=False)
            clientes.to_sql("clientes", conn, if_exists="replace", index=False)
            proveedores.to_sql("proveedores", conn, if_exists="replace", index=False)

            conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_productos_id ON productos(id_producto)")
            conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_clientes_id ON clientes(id_cliente)")
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS ux_proveedores_id ON proveedores(id_proveedor)"
            )

    def create_ventas_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            id_proveedor INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK (cantidad > 0),
            total_venta REAL NOT NULL CHECK (total_venta >= 0),
            fecha_venta TEXT NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
        );
        """
        with self._connect() as conn:
            conn.execute("DROP TABLE IF EXISTS ventas")
            conn.execute(sql)

    def run_crud(self, precios: dict[int, float]) -> pd.DataFrame:
        ventas_iniciales = [
            (101, 1, 900111, 2, "2026-04-15"),
            (106, 7, 600444, 1, "2026-04-15"),
            (120, 19, 200888, 3, "2026-04-15"),
            (114, 16, 999000, 2, "2026-04-16"),
            (102, 10, 800222, 4, "2026-04-16"),
        ]

        with self._connect() as conn:
            for id_cliente, id_producto, id_proveedor, cantidad, fecha in ventas_iniciales:
                total = float(precios[id_producto]) * cantidad
                conn.execute(
                    """
                    INSERT INTO ventas (id_cliente, id_producto, id_proveedor, cantidad, total_venta, fecha_venta)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (id_cliente, id_producto, id_proveedor, cantidad, total, fecha),
                )

            # UPDATE solicitado por la rúbrica.
            nuevo_total = float(precios[1]) * 3
            conn.execute(
                "UPDATE ventas SET cantidad = ?, total_venta = ? WHERE id_venta = 1",
                (3, nuevo_total),
            )

            # DELETE solicitado por la rúbrica.
            conn.execute("DELETE FROM ventas WHERE id_venta = 3")

            # READ solicitado por la rúbrica (JOIN cliente-producto-total).
            query = """
                SELECT
                    v.id_venta,
                    c.nombre_cliente,
                    p.producto,
                    v.total_venta,
                    v.fecha_venta
                FROM ventas AS v
                INNER JOIN clientes AS c ON c.id_cliente = v.id_cliente
                INNER JOIN productos AS p ON p.id_producto = v.id_producto
                ORDER BY v.id_venta;
            """
            resultado = pd.read_sql_query(query, conn)

        return resultado
