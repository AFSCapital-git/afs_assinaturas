import base64
import io
from pathlib import Path

from PIL import Image

from config import (
    ADDRESS,
    COLOR_HEX,
    DISCLAIMER_AMAZONIA,
    DISCLAIMER_INVESTIMENTOS,
    FONT_FILES,
    IMAGE_MAP,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def font_face_css() -> str:
    """Gera blocos @font-face com a fonte Elza embutida em base64."""
    css = ""
    regular = FONT_FILES["regular"]
    bold = FONT_FILES["bold"]
    if regular.exists():
        css += f"""
        @font-face {{
            font-family: 'Elza';
            font-weight: 400;
            src: url('data:font/otf;base64,{_b64(regular)}') format('opentype'),
                 local('Elza-Regular'), local('Elza Regular');
        }}"""
    if bold.exists():
        css += f"""
        @font-face {{
            font-family: 'Elza';
            font-weight: 700;
            src: url('data:font/otf;base64,{_b64(bold)}') format('opentype'),
                 local('Elza-Bold'), local('Elza Bold');
        }}"""
    return css


# ── Classes públicas ──────────────────────────────────────────────────────────

class SignatureHTML:
    """Gera o HTML da assinatura para exibição na prévia do Streamlit."""

    def __init__(self, nome: str, cargo: str, empresa: str, telefone: str = "") -> None:
        self.nome = nome
        self.cargo = cargo
        self.empresa = empresa
        self.telefone = telefone

    def render(self) -> str:
        img_b64 = _b64(IMAGE_MAP[self.empresa])
        fonts = font_face_css()

        style = f"""
        <style>
            {fonts}
            .assinatura {{
                font-family: 'Elza', Arial, sans-serif;
                color: {COLOR_HEX};
                line-height: 1.1;
                border-collapse: collapse;
            }}
            .nome    {{ font-size: 16px; font-weight: 700; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; }}
            .cargo   {{ font-size: 13px; font-weight: 400; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; }}
            .telefone{{ font-size: 12px; font-weight: 400; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; }}
            .endereco{{ font-size: 12px; font-weight: 400; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; }}
            .disclaimer{{ font-size: 10px; font-weight: 400; font-style: italic; color: {COLOR_HEX}; font-family: Calibri, Arial, sans-serif; line-height: 1.4; }}
        </style>
        """

        return f"""
        {style}
        <table class="assinatura" cellpadding="0" cellspacing="0" border="0" width="676" style="width: 676px;">
            <tr>
                <td style="padding-bottom: 2px;">
                    <table cellpadding="0" cellspacing="0" border="0">
                        <tr><td style="padding-bottom: 2px;"><span class="nome">{self.nome}</span></td></tr>
                        <tr><td style="padding-bottom: 2px;"><span class="cargo">{self.cargo}</span></td></tr>
                        {f'<tr><td style="padding-bottom: 2px;"><span class="telefone">{self.telefone}</span></td></tr>' if self.telefone else ''}
                        <tr><td style="padding-bottom: 2px;"><span class="endereco">{ADDRESS}</span></td></tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding-top: 8px; padding-left: 0; padding-right: 0;">
                    <img
                        src="data:image/png;base64,{img_b64}"
                        width="676"
                        alt="{self.empresa}"
                        style="display: block; margin: 0; width: 676px; height: auto; min-width: 676px;"
                    />
                </td>
            </tr>
            {f'<tr><td style="padding-top: 10px; width: 676px; text-align: justify;"><span class="disclaimer">{DISCLAIMER_INVESTIMENTOS}</span></td></tr>' if self.empresa == 'AFBR Investimentos' else ''}
            {f'<tr><td style="padding-top: 10px; width: 676px; text-align: justify;"><span class="disclaimer">{DISCLAIMER_AMAZONIA}</span></td></tr>' if self.empresa == 'Amazonia Innovation Funding' else ''}
        </table>
        """

    def global_css(self) -> str:
        """CSS para aplicar a fonte Elza na interface do Streamlit."""
        return f"""
        <style>
            {font_face_css()}
            html, body, [class*="css"] {{ font-family: 'Elza', sans-serif !important; }}
            h1, h2, h3 {{ color: {COLOR_HEX} !important; font-family: 'Elza', sans-serif !important; }}
        </style>
        """


class SignatureImage:
    """Gera a assinatura como imagem PNG via Pillow."""

    def __init__(self, nome: str, cargo: str, empresa: str, telefone: str = "") -> None:
        self.nome = nome
        self.cargo = cargo
        self.empresa = empresa
        self.telefone = telefone

    def render(self) -> bytes:
        """Retorna apenas o logo como PNG — o texto fica fora da imagem."""
        logo = Image.open(IMAGE_MAP[self.empresa]).convert("RGBA")
        buf  = io.BytesIO()
        logo.convert("RGB").save(buf, format="PNG", dpi=(96, 96))
        return buf.getvalue()
