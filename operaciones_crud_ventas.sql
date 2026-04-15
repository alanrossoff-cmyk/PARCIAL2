PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ventas;

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

INSERT INTO ventas (id_cliente, id_producto, id_proveedor, cantidad, total_venta, fecha_venta) VALUES
    (101, 1, 900111, 2, 10000, '2026-04-15'),
    (106, 7, 600444, 1, 7500, '2026-04-15'),
    (120, 19, 200888, 3, 4500, '2026-04-15'),
    (114, 16, 999000, 2, 11000, '2026-04-16'),
    (102, 10, 800222, 4, 8800, '2026-04-16');

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

UPDATE ventas
SET cantidad = 3, total_venta = 15000
WHERE id_venta = 1;

DELETE FROM ventas
WHERE id_venta = 3;
