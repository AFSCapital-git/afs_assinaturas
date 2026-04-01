from pathlib import Path

# ── Identidade visual ─────────────────────────────────────────────────────────
COLOR_HEX = "#153e36"
COLOR_RGB = (21, 62, 54)
ADDRESS = "R. Arizona, 1426, cj 32, Cidade Monções, São Paulo – SP, 04567-003"

# ── Empresas ──────────────────────────────────────────────────────────────────
EMPRESAS = ["AFBR", "AFBR Investimentos"]

IMAGE_MAP: dict[str, Path] = {
    "AFBR": Path("imagens/afbr.png"),
    "AFBR Investimentos": Path("imagens/afbr_investimentos.png"),
}

# ── Fontes ────────────────────────────────────────────────────────────────────
# Caminhos relativos ao projeto — funcionam local e em servidor (Streamlit Cloud)
FONT_FILES: dict[str, Path] = {
    "regular": Path("fonts/Elza-Regular.otf"),
    "bold": Path("fonts/Elza-Bold.otf"),
}

# ── Planilha ──────────────────────────────────────────────────────────────────
PLANILHA = Path("cargos.xlsx")

# ── Imagem gerada ─────────────────────────────────────────────────────────────
IMAGE_SCALE = 2       # fator de supersampling (2× → downscale para nitidez)
LOGO_WIDTH_PX = 520   # largura final do logo em px (antes do scale)
