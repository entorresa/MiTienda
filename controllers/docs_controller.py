from odoo import http
from odoo.http import request
from odoo.modules.module import get_module_path
from weasyprint import HTML
import re
import os
import markdown


class DocsController(http.Controller):

    def _reemplazar_imagen_markdown(self, contenido, ruta_modulo):
        patron = r'!\[(.*?)\]\((.*?)\)'

        def reemplazar(match):
            texto_alt = match.group(1)
            ruta_imagen = match.group(2)
            if ruta_imagen.startswith('/docs/'):
                ruta_absoluta = os.path.join(
                    ruta_modulo,
                    ruta_imagen.lstrip('/')
                )
                url_archivo = f'file://{ruta_absoluta}'
                return f'![{texto_alt}]({url_archivo})'
            return match.group(0)

        return re.sub(patron, reemplazar, contenido)

    def _generar_manual(self, ruta_manual, modulo='api_mitienda_peru'):
        try:
            ruta_modulo = get_module_path(modulo)
            ruta_docs = os.path.join(ruta_modulo, 'docs/' + ruta_manual)
            manuales = []

            if os.path.exists(ruta_docs):
                for root, dirs, files in os.walk(ruta_docs):
                    ruta_relativa = os.path.relpath(root, ruta_docs)
                    if ruta_relativa == '.':
                        depth = 0
                    else:
                        depth = ruta_relativa.count(os.sep) + 1
                    if depth > 3:
                        dirs[:] = []
                        continue
                    dirs.sort()
                    files.sort()
                    for file_name in files:
                        if file_name.lower().endswith('.md'):
                            ruta_archivo = os.path.join(root, file_name)
                            manuales.append(ruta_archivo)

            contenido = ''
            for manual in manuales:
                ruta = os.path.join(ruta_modulo, manual)
                if os.path.exists(ruta):
                    with open(ruta, 'r', encoding='utf-8') as f:
                        contenido_manual = f.read()
                        contenido_manual = self._reemplazar_imagen_markdown(
                            contenido_manual,
                            ruta_modulo,
                        )
                    contenido += '\n\n'
                    contenido += contenido_manual
                    contenido += '\n\n'

            html_cuerpo = markdown.markdown(
                contenido,
                extensions=[
                    'tables',
                    'fenced_code',
                    'toc',
                ]
            )

            html = f"""
            <html>
            <head>
                <meta charset="utf-8" />
                <style>
                    @page {{
                        size: Letter portrait;
                        margin: 1.5cm;
                    }}
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 12px;
                        line-height: 1.4;
                    }}
                    h1, h2, h3 {{
                        color: #2c3e50;
                    }}
                    code, pre {{
                        background: #f4f4f4;
                        padding: 2px 4px;
                        font-size: 10px;
                        font-family: Consolas, "Courier New", monospace;
                        overflow-x: break-word;
                        white-space: pre-wrap;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        page-break-inside: avoid;
                    }}
                    table, th, td {{
                        border; 1px solid #ccc;
                    }}
                    th, td {{
                        padding: 8px;
                    }}
                    img {{
                        max-width: 100%;
                        page-break-inside: avoid;
                    }}
                </style>
            </head>
            <body>
                {html_cuerpo}
            </body>
            </html>
            """

            pdf = HTML(
                string=html,
                base_url=ruta_modulo,
            ).write_pdf()
        except Exception as e:
            pdf = str(e)
        return pdf

    @http.route(
        '/api_mitienda_peru/docs/manual_usuario',
        type='http',
        auth='none',
        website=False,
    )
    def manual_usuario_pdf(self, **kwargs):
        pdf = self._generar_manual('manual_usuario')
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', f'inline; filename="manual_usuario.pdf"'),
        ]
        return request.make_response(pdf, headers=headers)

    @http.route(
        '/api_mitienda_peru/docs/manual_tecnico',
        type='http',
        auth='none',
        website=False,
    )
    def manual_tecnico_pdf(self, **kwargs):
        pdf = self._generar_manual('manual_tecnico')
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', f'inline; filename="manual_tecnico.pdf"'),
        ]
        return request.make_response(pdf, headers=headers)
