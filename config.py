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

# ── Disclaimer AFBR Investimentos ───────────────────────────────────
DISCLAIMER_INVESTIMENTOS = (
    "A Advance Assessor de Investimentos s/s Ltda. (“AFBR Investimentos”), inscrita sob o CNPJ nº "
    "41.564.752/0001-62 é uma empresa de assessoria de investimentos devidamente registrada na Comissão "
    "de Valores Mobíliários (CVM), na forma da Resolução CVM 178. Atuando no mercado financeiro como "
    "preposto do Banco BTG Pactual S/A, o que pode ser verificado através do site da ANCORD "
    "(https://www.ancord.org.br/certificacao-e-credenciamento/) ou através do site do próprio Banco BTG "
    "Pactual S/A (https://www.sejabtg.com/seja-btg). O Banco BTG Pactual S/A é instituição financeira "
    "integrante do sistema de distribuição de títulos e valores mobiliários, atuando como intermediário "
    "das operações de seus clientes. Na forma da legislação da CVM, o assessor de investimento não pode "
    "administrar ou gerir o patrimônio de investidores, pois é um preposto do intermediário e depende da "
    "autorização prévia do cliente para realizar operações no mercado financeiro. Na realização de "
    "operações com derivativos existe a possibilidade de significativas perdas patrimoniais, inclusive "
    "superiores aos valores investidos. A assessoria pode exercer outras atividades relacionadas ao "
    "mercado financeiro, de capitais, securitário e de previdência e capitalização, que podem ou não ser "
    "em parceria com o BTG Pactual ou demais instituições, e que podem ou não ser realizadas pela mesma "
    "pessoa jurídica da assessoria. Especificamente quanto a atividades de gestão, consultoria e análise "
    "de valores mobiliários, estas podem vir a ser desempenhadas por empresas do grupo e nunca pela "
    "própria assessoria de investimentos, considerando que são atividades conflitantes e que exigem "
    "segregação. O investimento em ações é um investimento de risco e rentabilidade passada não é "
    "garantia de rentabilidade futura. Para reclamações, favor contatar a Ouvidoria do Banco BTG Pactual "
    "S/A no telefone nº 0800-722-0048. Para acessar nossa lista de sócios clique aqui: "
    "https://www.sejabtg.com/escritórios."
)

# ── Imagem gerada ─────────────────────────────────────────────────────────────
IMAGE_SCALE = 2       # fator de supersampling (2× → downscale para nitidez)
LOGO_WIDTH_PX = 520   # largura final do logo em px (antes do scale)
