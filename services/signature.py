import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import (
    ADDRESS,
    COLOR_HEX,
    COLOR_RGB,
    FONT_FILES,
    IMAGE_MAP,
    IMAGE_SCALE,
    LOGO_WIDTH_PX,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def _font_face_css() -> str:
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

    def __init__(self, nome: str, cargo: str, empresa: str) -> None:
        self.nome = nome
        self.cargo = cargo
        self.empresa = empresa

    def render(self) -> str:
        img_b64 = _b64(IMAGE_MAP[self.empresa])
        fonts = _font_face_css()

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
            .endereco{{ font-size: 12px; font-weight: 400; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; }}
        </style>
        """

        return f"""
        {style}
        <table class="assinatura" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td style="padding-bottom: 2px;">
                    <table cellpadding="0" cellspacing="0" border="0">
                        <tr><td style="padding-bottom: 2px;"><span class="nome">{self.nome}</span></td></tr>
                        <tr><td style="padding-bottom: 2px;"><span class="cargo">{self.cargo}</span></td></tr>
                        <tr><td style="padding-bottom: 2px;"><span class="endereco">{ADDRESS}</span></td></tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding-top: 8px; padding-left: 0; padding-right: 0;">
                    <img
                        src="data:image/png;base64,{img_b64}"
                        width="520"
                        alt="{self.empresa}"
                        style="display: block; margin: 0; max-width: 100%;"
                    />
                </td>
            </tr>
        </table>
        """

    def global_css(self) -> str:
        """CSS para aplicar a fonte Elza na interface do Streamlit."""
        return f"""
        <style>
            {_font_face_css()}
            html, body, [class*="css"] {{ font-family: 'Elza', sans-serif !important; }}
            h1, h2, h3 {{ color: {COLOR_HEX} !important; font-family: 'Elza', sans-serif !important; }}
        </style>
        """


class SignatureImage:
    """Gera a assinatura como imagem PNG via Pillow."""

    def __init__(self, nome: str, cargo: str, empresa: str) -> None:
        self.nome = nome
        self.cargo = cargo
        self.empresa = empresa

    def render(self) -> bytes:
        s = IMAGE_SCALE
        pad_y = 14 * s

        font_bold = ImageFont.truetype(str(FONT_FILES["bold"]), 17 * s)
        font_reg  = ImageFont.truetype(str(FONT_FILES["regular"]), 13 * s)
        font_sm   = ImageFont.truetype(str(FONT_FILES["regular"]), 12 * s)

        logo_orig = Image.open(IMAGE_MAP[self.empresa]).convert("RGBA")
        logo_w = LOGO_WIDTH_PX * s
        logo_h = int(logo_orig.height * logo_w / logo_orig.width)
        logo = logo_orig.resize((logo_w, logo_h), Image.LANCZOS)

        dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

        def _th(text: str, font: ImageFont.FreeTypeFont) -> int:
            bb = dummy.textbbox((0, 0), text, font=font)
            return bb[3] - bb[1]

        h_nome  = _th(self.nome, font_bold)
        h_cargo = _th(self.cargo, font_reg)
        h_addr  = _th(ADDRESS, font_sm)

        gap      = 3 * s
        gap_logo = 10 * s

        total_w = logo_w
        total_h = pad_y + h_nome + gap + h_cargo + gap + h_addr + gap_logo + logo_h + pad_y

        img  = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        y = pad_y
        draw.text((0, y), self.nome,  font=font_bold, fill=COLOR_RGB)
        y += h_nome + gap
        draw.text((0, y), self.cargo, font=font_reg,  fill=COLOR_RGB)
        y += h_cargo + gap
        draw.text((0, y), ADDRESS,    font=font_sm,   fill=COLOR_RGB)
        y += h_addr + gap_logo
        img.paste(logo, (0, y), logo)

        img = img.resize((total_w // s, total_h // s), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
