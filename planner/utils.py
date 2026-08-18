import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_path, context):
    template = get_template(template_path)
    html = template.render(context)

    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return None
    return result.getvalue()