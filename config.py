from pathlib import Path

# ── Identidade visual ─────────────────────────────────────────────────────────
COLOR_HEX = "#153e36"
COLOR_RGB = (21, 62, 54)
ADDRESS = "R. Arizona, 1426, cj 32, Cidade Monções, São Paulo – SP, 04567-003"

# ── Empresas ──────────────────────────────────────────────────────────────────
EMPRESAS = ["AFBR", "AFBR Investimentos", "Guatã", "Amazonia Innovation Funding"]

IMAGE_MAP: dict[str, Path] = {
    "AFBR": Path("imagens/afbr.png"),
    "AFBR Investimentos": Path("imagens/afbr_investimentos.png"),
    "Guatã": Path("imagens/guata.png"),
    "Amazonia Innovation Funding": Path("imagens/amazonia_innovation_funding.png"),
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

# ── Disclaimer Amazonia Innovation Funding ──────────────────────────────────────
DISCLAIMER_AMAZONIA = (
    "Esta mensagem, incluindo seus anexos, contém informações protegidas por lei, privilegiadas e/ou "
    "confidenciais, não podendo ser retransmitida, arquivada, divulgada ou copiada sem a autorização "
    "do remetente. Caso tenha recebido esta mensagem por engano, por favor informe ao remetente "
    "respondendo imediatamente este e-mail e, em seguida, apague-a do seu computador. "
    "This e-mail and attachments contain information protected by law, privileged and/or confidential, "
    "and cannot be retransmitted, filed, divulged or copied without authorization from the sender. "
    "If you have received this message by mistake, please inform the sender immediately by replying "
    "to this e-mail. After that, please delete this e-mail from your computer."
)

# ── Imagem gerada ─────────────────────────────────────────────────────────────
IMAGE_SCALE = 1       # fator de supersampling (3× → downscale para nitidez)
LOGO_WIDTH_PX = 520   # largura final do logo em px (antes do scale)
