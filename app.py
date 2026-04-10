import base64
import io
import re

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image as PILImage

from config import DISCLAIMER_AMAZONIA, DISCLAIMER_INVESTIMENTOS, EMPRESAS
from services.signature import SignatureHTML, SignatureImage
from services.spreadsheet import buscar_dados_pessoa, carregar_pessoas


URL_PATTERN = re.compile(r'https?://[^\s<>")]+')


def _linkify_text(text: str) -> str:
    """Converte URLs em links HTML clicáveis mantendo pontuação final."""

    def _repl(match: re.Match[str]) -> str:
        raw_url = match.group(0)
        clean_url = raw_url.rstrip(".,;)")
        suffix = raw_url[len(clean_url):]
        return (
            f'<a href="{clean_url}" target="_blank" rel="noopener noreferrer">'
            f"{clean_url}"
            f"</a>{suffix}"
        )

    return URL_PATTERN.sub(_repl, text)

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
png: bytes | None = None
png_size: tuple[int, int] | None = None

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
            png = SignatureImage(nome, cargo, empresa, telefone).render()
            with PILImage.open(io.BytesIO(png)) as preview_img:
                png_size = preview_img.size
        except Exception as e:
            st.error(f"Não foi possível gerar a imagem: {e}")

with col_preview:
    st.subheader("Prévia")

    if nome and png and png_size:
        # Exibe um bloco único com imagem + disclaimer para facilitar a seleção completa.
        logical_w = png_size[0]
        st.caption(f"Resolução: {png_size[0]}×{png_size[1]} px")
        img_b64 = base64.b64encode(png).decode("utf-8")

        disclaimer_text = (
            DISCLAIMER_INVESTIMENTOS if empresa == "AFBR Investimentos"
            else DISCLAIMER_AMAZONIA if empresa == "Amazonia Innovation Funding"
            else None
        )
        disclaimer_html = _linkify_text(disclaimer_text) if disclaimer_text else ""

        disclaimer_section = ""
        if disclaimer_html:
            disclaimer_section = (
                '<div style="margin-top:10px; font-size:10px; line-height:1.4; '
                'font-style:italic; font-family:Calibri, Arial, sans-serif; color:#153e36; '
                'text-align:justify;">'
                '<br />'
                f"{disclaimer_html}"
                "</div>"
            )

        signature_html = f"""
        <div style="margin-bottom:8px;">
            <button
                type="button"
                onclick="selectSignatureContent()"
                style="background:#153e36; color:#fff; border:none; border-radius:6px; padding:8px 12px; cursor:pointer; font-size:13px; font-family:Arial, sans-serif;"
            >
                Selecionar assinatura (imagem + disclaimer)
            </button>
        </div>

        <div id="signature-selection-block" style="max-width:100%;">
            <img src="data:image/png;base64,{img_b64}" style="width:{logical_w}px; max-width:100%; display:block;" />
            {disclaimer_section}
        </div>

        <script>
            function selectSignatureContent() {{
                const el = document.getElementById('signature-selection-block');
                if (!el) return;

                const selection = window.getSelection();
                const range = document.createRange();
                range.selectNodeContents(el);
                selection.removeAllRanges();
                selection.addRange(range);
            }}
        </script>
        """

        preview_height = 720 if disclaimer_html else 300
        components.html(signature_html, height=preview_height, scrolling=True)
    else:
        st.info("Selecione ou digite um nome para visualizar a assinatura.")

