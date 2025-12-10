from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.conf import settings

def get_data_sitemap(domain):
    return f"""
        User-agent: *
        Disallow:
        Sitemap: {domain}/sitemap.xml
    """


@require_GET
def robots_txt(request):
    domain = request.build_absolute_uri('/')[:-1]  # Получаем текущий домен без слэша в конце
    content = get_data_sitemap(domain)
    # Убираем лишние пробелы и пустые строки
    content = '\n'.join([line.strip() for line in content.splitlines() if line.strip()])
    return HttpResponse(content, content_type="text/plain")
