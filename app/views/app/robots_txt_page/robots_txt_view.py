from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.conf import settings


content = f"""
User-agent: *
Disallow:
Sitemap: {settings.BASE_SITE_URL}/sitemap.xml
""".strip() + "\n"


@require_GET
def robots_txt(request):
    return HttpResponse(content, content_type="text/plain")
