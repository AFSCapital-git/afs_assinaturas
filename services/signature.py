import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from config import (
    ADDRESS,
    COLOR_HEX,
    COLOR_RGB,
    DISCLAIMER_AMAZONIA,
    DISCLAIMER_INVESTIMENTOS,
    FONT_FILES,
    IMAGE_MAP,
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
        # ── Constantes ────────────────────────────────────────────────────────
        # RETINA_SCALE: imagem final a 2× pixels para nitidez em telas HiDPI
        # SS: supersampling do texto *dentro* do espaço 2×  → total 8× native
        RETINA_SCALE = 2
        SS           = 4
        GAP          = 3    # px lógicos (1×)
        GAP_LOGO     = 10   # px lógicos (1×)
        PAD_Y        = 14   # px lógicos (1×)

        # ── Logo a 2× resolução nativa ────────────────────────────────────────
        logo_orig = Image.open(IMAGE_MAP[self.empresa]).convert("RGBA")
        W2        = logo_orig.width  * RETINA_SCALE   # largura do PNG final
        H2_logo   = logo_orig.height * RETINA_SCALE
        logo      = logo_orig.resize((W2, H2_logo), Image.LANCZOS)

        # ── Helpers de medição e downscale (espaço hi-res → espaço 2×) ────────
        dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        W_hi  = W2 * SS    # canvas de texto: 8× a largura nativa

        def _th(text: str, font: ImageFont.FreeTypeFont) -> int:
            bb = dummy.textbbox((0, 0), text, font=font)
            return bb[3] - bb[1]

        def _tw(text: str, font: ImageFont.FreeTypeFont) -> int:
            bb = dummy.textbbox((0, 0), text, font=font)
            return bb[2] - bb[0]

        def _downscale(canvas: Image.Image) -> Image.Image:
            """Reduz canvas 8×-hi-res para o espaço 2× (÷SS) com nitidez máxima."""
            out_h   = round(canvas.height / SS)
            reduced = canvas.resize((W2, out_h), Image.LANCZOS)
            return reduced.filter(ImageFilter.UnsharpMask(radius=1.2, percent=220, threshold=0))

        # ── Fontes: 2× (retina) × SS (supersampling) = 8× native ─────────────
        FS        = RETINA_SCALE * SS
        font_bold = ImageFont.truetype(str(FONT_FILES["bold"]),    17 * FS)
        font_reg  = ImageFont.truetype(str(FONT_FILES["regular"]), 13 * FS)
        font_sm   = ImageFont.truetype(str(FONT_FILES["regular"]), 12 * FS)

        # ── Medições no espaço hi-res (8×) ──────────────────────────────────
        pad_y_hi = PAD_Y * FS
        gap_hi   = GAP   * FS

        h_nome  = _th(self.nome,     font_bold)
        h_cargo = _th(self.cargo,    font_reg)
        h_tel   = _th(self.telefone, font_sm) if self.telefone else 0
        h_addr  = _th(ADDRESS,       font_sm)

        tel_h_hi  = (h_tel + gap_hi) if self.telefone else 0
        text_h_hi = pad_y_hi + h_nome + gap_hi + h_cargo + gap_hi + tel_h_hi + h_addr + (pad_y_hi // 2)

        # ── Canvas hi-res do bloco de texto ───────────────────────────────────
        txt_canvas = Image.new("RGBA", (W_hi, text_h_hi), (255, 255, 255, 255))
        draw       = ImageDraw.Draw(txt_canvas)

        y = pad_y_hi
        draw.text((0, y), self.nome,  font=font_bold, fill=COLOR_RGB)
        y += h_nome + gap_hi
        draw.text((0, y), self.cargo, font=font_reg,  fill=COLOR_RGB)
        y += h_cargo + gap_hi
        if self.telefone:
            draw.text((0, y), self.telefone, font=font_sm, fill=COLOR_RGB)
            y += h_tel + gap_hi
        draw.text((0, y), ADDRESS, font=font_sm, fill=COLOR_RGB)

        # ── Downscale do bloco de texto para espaço 2× ──────────────────────
        txt_lo = _downscale(txt_canvas)

        # ── Composição final (espaço 2×) ──────────────────────────────────────
        gap_logo_2x = GAP_LOGO * RETINA_SCALE
        total_h     = txt_lo.height + gap_logo_2x + logo.height

        final = Image.new("RGBA", (W2, total_h), (255, 255, 255, 255))
        final.paste(txt_lo, (0, 0))
        y_f = txt_lo.height + gap_logo_2x
        final.paste(logo, (0, y_f), logo)

        # Entrega final em 50% da largura/altura atual, mantendo proporção.
        final = final.resize((final.width // 2, final.height // 2), Image.LANCZOS)

        buf = io.BytesIO()
        # DPI=72 para manter o tamanho lógico esperado após reduzir a imagem pela metade.
        final.convert("RGB").save(buf, format="PNG", dpi=(72, 72))
        return buf.getvalue()
