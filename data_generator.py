"""Generación de archivos CSV sucios a partir del enunciado."""

from dataclasses import dataclass
from pathlib import Path

from .constants import (
    ARCHIVOS_SUCIOS,
    CLIENTES_SUCIOS,
    PRODUCTOS_SUCIOS,
    PROVEEDORES_SUCIOS,
)


@dataclass
class DirtyCSVGenerator:
    """Crea los tres datasets sucios exigidos por la rúbrica."""

    output_dir: Path

    def generate(self) -> dict[str, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        contenido = {
            "productos": PRODUCTOS_SUCIOS,
            "clientes": CLIENTES_SUCIOS,
            "proveedores": PROVEEDORES_SUCIOS,
        }

        rutas: dict[str, Path] = {}
        for nombre, texto_csv in contenido.items():
            ruta = self.output_dir / ARCHIVOS_SUCIOS[nombre]
            ruta.write_text(f"{texto_csv}\n", encoding="utf-8")
            rutas[nombre] = ruta

        return rutas
