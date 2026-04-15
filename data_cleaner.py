"""Limpieza y normalización de datos con Pandas."""

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata

import pandas as pd

from .constants import ARCHIVOS_LIMPIOS, ARCHIVOS_SUCIOS


def _normalize_slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", ".", text)
    return text.strip(".")


def _normalize_phone(value: object) -> str:
    if pd.isna(value):
        return "No Registra"
    as_text = str(value).strip()
    if as_text == "" or as_text.lower() == "nan":
        return "No Registra"
    return as_text.replace(".0", "")


@dataclass
class CafeteriaDataCleaner:
    """Carga, limpia y exporta los 3 datasets del parcial."""

    base_dir: Path

    def load_dirty_data(self) -> dict[str, pd.DataFrame]:
        return {
            nombre: pd.read_csv(self.base_dir / ruta)
            for nombre, ruta in ARCHIVOS_SUCIOS.items()
        }

    def clean_productos(self, df: pd.DataFrame) -> pd.DataFrame:
        clean = df.copy()

        split_cols = clean["producto_categoria"].str.split(" - ", n=1, expand=True)
        clean["producto"] = split_cols[0].str.strip().str.title()
        clean["categoria"] = split_cols[1].str.strip().str.title()
        clean["categoria"] = clean["categoria"].replace({"Panaderia": "Panadería"})

        clean["precio"] = (
            clean["precio"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        clean["precio"] = pd.to_numeric(clean["precio"], errors="coerce")

        stock_numeric = pd.to_numeric(clean["stock"], errors="coerce")
        stock_default = int(stock_numeric.median())
        clean["stock"] = stock_numeric.fillna(stock_default).astype(int)

        clean["fecha_vencimiento"] = pd.to_datetime(
            clean["fecha_vencimiento"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        clean["id_producto"] = pd.to_numeric(clean["id_producto"], errors="raise").astype(int)
        clean = clean[
            [
                "id_producto",
                "producto",
                "categoria",
                "precio",
                "stock",
                "fecha_vencimiento",
            ]
        ]
        return clean

    def clean_clientes(self, df: pd.DataFrame) -> pd.DataFrame:
        clean = df.copy()

        split_cols = clean["cliente_tipo"].str.split(" - ", n=1, expand=True)
        clean["nombre_cliente"] = split_cols[0].str.strip().str.title()
        clean["tipo_cliente"] = split_cols[1].str.strip().str.title()
        clean["tipo_cliente"] = clean["tipo_cliente"].replace(
            {
                "Profesor": "Profesor",
                "Estudiante": "Estudiante",
                "Externo": "Externo",
            }
        )

        clean["telefono"] = clean["telefono"].apply(_normalize_phone)

        clean["email"] = clean["email"].fillna("").astype(str).str.strip().str.lower()
        missing_email = clean["email"] == ""
        emails_existentes = set(clean.loc[~missing_email, "email"])
        for idx in clean.index[missing_email]:
            nombre = clean.at[idx, "nombre_cliente"]
            slug = _normalize_slug(nombre) or "cliente"
            email = f"{slug}@correo.com"
            contador = 1
            while email in emails_existentes:
                email = f"{slug}{contador}@correo.com"
                contador += 1
            clean.at[idx, "email"] = email
            emails_existentes.add(email)

        clean["fecha_nacimiento"] = pd.to_datetime(
            clean["fecha_nacimiento"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        clean["id_cliente"] = pd.to_numeric(clean["id_cliente"], errors="raise").astype(int)

        # 3NF: edad es derivada de fecha_nacimiento, se elimina.
        clean = clean.drop(columns=["cliente_tipo", "edad"])
        clean = clean[
            [
                "id_cliente",
                "nombre_cliente",
                "tipo_cliente",
                "email",
                "telefono",
                "fecha_nacimiento",
            ]
        ]
        return clean

    def clean_proveedores(self, df: pd.DataFrame) -> pd.DataFrame:
        clean = df.copy()

        split_cols = clean["empresa_ciudad"].str.split(" - ", n=1, expand=True)
        clean["empresa"] = split_cols[0].str.strip().str.title()
        clean["ciudad"] = split_cols[1].str.strip().str.title()
        clean["contacto"] = clean["contacto"].fillna("No Registra").replace("NaN", "No Registra")
        clean["contacto"] = clean["contacto"].astype(str).str.strip().str.title()

        clean["telefono"] = clean["telefono"].apply(_normalize_phone)

        clean["email"] = clean["email"].fillna("").astype(str).str.strip().str.lower()
        missing_email = clean["email"] == ""
        emails_existentes = set(clean.loc[~missing_email, "email"])
        for idx in clean.index[missing_email]:
            empresa = clean.at[idx, "empresa"]
            slug = _normalize_slug(empresa) or "proveedor"
            email = f"{slug}@proveedor.com"
            contador = 1
            while email in emails_existentes:
                email = f"{slug}{contador}@proveedor.com"
                contador += 1
            clean.at[idx, "email"] = email
            emails_existentes.add(email)

        clean["id_proveedor"] = pd.to_numeric(clean["nit_proveedor"], errors="raise").astype(int)
        clean = clean.drop(columns=["nit_proveedor", "empresa_ciudad"])
        clean = clean[
            [
                "id_proveedor",
                "empresa",
                "ciudad",
                "contacto",
                "telefono",
                "email",
            ]
        ]
        return clean

    def clean_all(self) -> dict[str, pd.DataFrame]:
        dirty = self.load_dirty_data()
        return {
            "productos": self.clean_productos(dirty["productos"]),
            "clientes": self.clean_clientes(dirty["clientes"]),
            "proveedores": self.clean_proveedores(dirty["proveedores"]),
        }

    def export_clean_data(self, datasets: dict[str, pd.DataFrame]) -> dict[str, Path]:
        rutas: dict[str, Path] = {}
        for nombre, df in datasets.items():
            ruta = self.base_dir / ARCHIVOS_LIMPIOS[nombre]
            df.to_csv(ruta, index=False, encoding="utf-8")
            rutas[nombre] = ruta
        return rutas
