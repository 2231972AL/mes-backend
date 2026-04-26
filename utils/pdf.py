from fastapi.responses import FileResponse
from weasyprint import HTML
from jinja2 import Template

def render_pdf_from_html(template_str: str, context: dict, output_path: str) -> FileResponse:
    template = Template(template_str)
    html = template.render(**context)
    HTML(string=html).write_pdf(output_path)
    return FileResponse(output_path, media_type="application/pdf")
