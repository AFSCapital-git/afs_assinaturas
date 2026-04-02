import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import (
    ADDRESS,
    COLOR_HEX,
    COLOR_RGB,
    DISCLAIMER_AMAZONIA,
    DISCLAIMER_INVESTIMENTOS,
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

    def __init__(self, nome: str, cargo: str, empresa: str, telefone: str = "") -> None:
        self.nome = nome
        self.cargo = cargo
        self.empresa = empresa
        self.telefone = telefone

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
            .telefone{{ font-size: 12px; font-weight: 400; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; }}
            .endereco{{ font-size: 12px; font-weight: 400; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; }}
            .disclaimer{{ font-size: 10px; font-weight: 400; font-style: italic; color: {COLOR_HEX}; font-family: 'Elza', Arial, sans-serif; line-height: 1.4; }}
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
                        {f'<tr><td style="padding-bottom: 2px;"><span class="telefone">{self.telefone}</span></td></tr>' if self.telefone else ''}
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
            {f'<tr><td style="padding-top: 10px; max-width: 520px;"><span class="disclaimer">{DISCLAIMER_INVESTIMENTOS}</span></td></tr>' if self.empresa == 'AFBR Investimentos' else ''}
            {f'<tr><td style="padding-top: 10px; max-width: 520px;"><span class="disclaimer">{DISCLAIMER_AMAZONIA}</span></td></tr>' if self.empresa == 'Amazonia Innovation Funding' else ''}
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

    def __init__(self, nome: str, cargo: str, empresa: str, telefone: str = "") -> None:
        self.nome = nome
        self.cargo = cargo
        self.empresa = empresa
        self.telefone = telefone

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
        h_tel   = _th(self.telefone, font_sm) if self.telefone else 0
        h_addr  = _th(ADDRESS, font_sm)

        gap      = 3 * s
        gap_logo = 10 * s

        tel_height = (h_tel + gap) if self.telefone else 0
        total_w = logo_w
        total_h = pad_y + h_nome + gap + h_cargo + gap + tel_height + h_addr + gap_logo + logo_h + pad_y

        img  = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        y = pad_y
        draw.text((0, y), self.nome,  font=font_bold, fill=COLOR_RGB)
        y += h_nome + gap
        draw.text((0, y), self.cargo, font=font_reg,  fill=COLOR_RGB)
        y += h_cargo + gap
        if self.telefone:
            draw.text((0, y), self.telefone, font=font_sm, fill=COLOR_RGB)
            y += h_tel + gap
        draw.text((0, y), ADDRESS,    font=font_sm,   fill=COLOR_RGB)
        y += h_addr + gap_logo
        img.paste(logo, (0, y), logo)
        y += logo_h

        disclaimer_text = (
            DISCLAIMER_INVESTIMENTOS if self.empresa == "AFBR Investimentos"
            else DISCLAIMER_AMAZONIA if self.empresa == "Amazonia Innovation Funding"
            else None
        )
        if disclaimer_text:
            font_disc = ImageFont.truetype(str(FONT_FILES["regular"]), 10 * s)

            def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
                words = text.split()
                lines: list[str] = []
                current = ""
                for word in words:
                    candidate = (current + " " + word).strip()
                    bb = dummy.textbbox((0, 0), candidate, font=font)
                    if bb[2] - bb[0] <= max_w:
                        current = candidate
                    else:
                        if current:
                            lines.append(current)
                        current = word
                if current:
                    lines.append(current)
                return lines

            disc_lines = _wrap_text(disclaimer_text, font_disc, total_w)
            h_disc_line = dummy.textbbox((0, 0), "A", font=font_disc)[3] - dummy.textbbox((0, 0), "A", font=font_disc)[1]
            disc_gap = 2 * s
            disc_total_h = len(disc_lines) * (h_disc_line + disc_gap)

            new_h = y + gap_logo + disc_total_h + pad_y
            img_ext = Image.new("RGBA", (total_w, new_h), (255, 255, 255, 255))
            img_ext.paste(img, (0, 0))
            draw_ext = ImageDraw.Draw(img_ext)
            y += gap_logo
            for line in disc_lines:
                draw_ext.text((0, y), line, font=font_disc, fill=COLOR_RGB)
                y += h_disc_line + disc_gap
            img_ext = img_ext.resize((total_w // s, new_h // s), Image.LANCZOS)
            buf = io.BytesIO()
            img_ext.save(buf, format="PNG")
            return buf.getvalue()

        img = img.resize((total_w // s, total_h // s), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
