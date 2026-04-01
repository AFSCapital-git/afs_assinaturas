import openpyxl
import streamlit as st

from config import PLANILHA


@st.cache_data
def carregar_pessoas() -> dict[str, str]:
    """Lê a planilha e retorna {nome: cargo}, ordenado pelo nome."""
    wb = openpyxl.load_workbook(PLANILHA, read_only=True, data_only=True)
    ws = wb.active
    pessoas: dict[str, str] = {}
    primeira = True
    for row in ws.iter_rows(values_only=True):
        nome_val, cargo_val = row[0], row[1]
        if primeira:
            primeira = False
            continue
        if nome_val and str(nome_val).strip():
            cargo = str(cargo_val).strip() if cargo_val else ""
            if cargo == "-":
                cargo = ""
            pessoas[str(nome_val).strip()] = cargo
    wb.close()
    return dict(sorted(pessoas.items(), key=lambda x: x[0]))
