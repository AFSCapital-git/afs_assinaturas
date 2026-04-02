import openpyxl
import streamlit as st

from config import PLANILHA


@st.cache_data
def carregar_pessoas() -> dict[str, dict]:
    """Lê a planilha e retorna {nome: {cargo, telefone}}, ordenado pelo nome."""
    wb = openpyxl.load_workbook(PLANILHA, read_only=True, data_only=True)
    ws = wb.active
    pessoas: dict[str, dict] = {}
    primeira = True
    for row in ws.iter_rows(values_only=True):
        nome_val, cargo_val = row[0], row[1]
        telefone_val = row[2] if len(row) > 2 else None
        if primeira:
            primeira = False
            continue
        if nome_val and str(nome_val).strip():
            cargo = str(cargo_val).strip() if cargo_val else ""
            if cargo == "-":
                cargo = ""
            telefone = str(telefone_val).strip() if telefone_val else ""
            if telefone == "-":
                telefone = ""
            pessoas[str(nome_val).strip()] = {"cargo": cargo, "telefone": telefone}
    wb.close()
    return dict(sorted(pessoas.items(), key=lambda x: x[0]))
