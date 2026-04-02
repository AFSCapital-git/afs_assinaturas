import streamlit as st

from config import EMPRESAS
from services.signature import SignatureHTML, SignatureImage, SignatureSVG
from services.spreadsheet import buscar_dados_pessoa, carregar_pessoas

st.set_page_config(
    page_title="Gerador de Assinatura – AFBR",
    page_icon="✉️",
    layout="wide",
)

# ── Fonte global ──────────────────────────────────────────────────────────────
_dummy_sig = SignatureHTML("", "", EMPRESAS[0])
st.markdown(_dummy_sig.global_css(), unsafe_allow_html=True)

# ── Dados ─────────────────────────────────────────────────────────────────────
pessoas = carregar_pessoas()
nomes_lista = list(pessoas.keys())

# ── Layout ────────────────────────────────────────────────────────────────────
st.title("Gerador de Assinatura de E-mail")
st.markdown("---")

col_form, col_preview = st.columns([1, 2], gap="large")

with col_form:
    st.subheader("Dados")

    nome = st.selectbox(
        "Nome",
        nomes_lista,
        accept_new_options=True,
        help="Selecione seu nome na lista ou digite para reescrever conforme sua preferência.",
    )

    dados = buscar_dados_pessoa(nome, pessoas) if nome else {}
    cargo_default = dados.get("cargo", "") if isinstance(dados, dict) else dados
    telefone = "+55 " + dados.get("telefone", "") if isinstance(dados, dict) else ""

    is_alex = nome and nome.strip().lower() == "alex taira"
    cargo = st.text_input(
        "Cargo",
        value=cargo_default,
        disabled=not is_alex,
        help="Cargo editável." if is_alex else "Preenchido automaticamente com base na planilha. Entre em contato com o responsável para solicitar alterações.",
    )

    empresa = st.selectbox(
        "Empresa",
        EMPRESAS,
        help="Selecione a empresa para usar o logo correspondente na assinatura.",
    )
    telefone = telefone + "   |  +55 (11) 2189-0693" if empresa == "AFBR Investimentos" else telefone

    if nome:
        try:
            svg = SignatureSVG(nome, cargo, empresa, telefone).render()
            empresa_slug = empresa.lower().replace(' ', '_')
            filename = f"assinatura_{nome.lower().replace(' ', '_')}_{empresa_slug}.svg"
            st.download_button(
                label="⬇️ Baixar imagem",
                data=svg,
                file_name=filename,
                mime="image/svg+xml",
                type="primary",
                use_container_width=True,
                help="Baixa a imagem resultante e importe-a nas configurações de assinatura do seu e-mail.",
            )
        except Exception as e:
            st.error(f"Não foi possível gerar a imagem: {e}")

with col_preview:
    st.subheader("Prévia")

    if nome:
        html = SignatureHTML(nome, cargo, empresa, telefone).render()
        st.html(html)
    else:
        st.info("Selecione ou digite um nome para visualizar a assinatura.")

