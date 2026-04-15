"""Ejecución completa del parcial 2 - Cafetería U. Sabana."""

from pathlib import Path

from cafeteria_etl import CafeteriaDBManager, CafeteriaDataCleaner, DirtyCSVGenerator


def run_pipeline(base_dir: Path) -> None:
    print("1) Generando CSV sucios...")
    generator = DirtyCSVGenerator(output_dir=base_dir)
    dirty_paths = generator.generate()

    print("2) Limpiando y normalizando DataFrames (1NF, 2NF, 3NF)...")
    cleaner = CafeteriaDataCleaner(base_dir=base_dir)
    datasets = cleaner.clean_all()
    clean_paths = cleaner.export_clean_data(datasets)

    print("3) Migrando a SQLite y construyendo arquitectura SQL...")
    db_manager = CafeteriaDBManager(db_path=base_dir / "parcial_2_cafeteria.db")
    db_manager.load_dimension_tables(
        productos=datasets["productos"],
        clientes=datasets["clientes"],
        proveedores=datasets["proveedores"],
    )
    db_manager.create_ventas_table()

    precios = datasets["productos"].set_index("id_producto")["precio"].to_dict()
    resultado_join = db_manager.run_crud(precios=precios)

    print("4) Resultado del SELECT con JOIN:")
    print(resultado_join.to_string(index=False))

    print("\nArchivos sucios generados:")
    for nombre, ruta in dirty_paths.items():
        print(f"- {nombre}: {ruta.name}")

    print("\nArchivos limpios exportados:")
    for nombre, ruta in clean_paths.items():
        print(f"- {nombre}: {ruta.name}")

    print("\nBase de datos final: parcial_2_cafeteria.db")
    print("Pipeline completado con éxito.")


if __name__ == "__main__":
    run_pipeline(Path(__file__).resolve().parent)
