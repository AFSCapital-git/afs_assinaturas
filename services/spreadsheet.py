import difflib
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


def buscar_dados_pessoa(nome: str, pessoas: dict[str, dict]) -> dict:
    """Retorna os dados da pessoa com busca exata primeiro, depois aproximada."""
    if nome in pessoas:
        return pessoas[nome]
    # Busca aproximada ignorando maiúsculas/minúsculas e acentos
    nomes_planilha = list(pessoas.keys())
    matches = difflib.get_close_matches(nome, nomes_planilha, n=1, cutoff=0.6)
    if matches:
        return pessoas[matches[0]]
    # Fallback: comparação normalizada (sem case)
    nome_lower = nome.lower()
    for chave in nomes_planilha:
        if chave.lower() == nome_lower:
            return pessoas[chave]
    return {}
