from datetime import date

from django.utils.safestring import mark_safe
from django.core.cache import cache

from app.db_models import Chain, ImageSocial


def format_value_number(value_int):
    """
        Преобразует числовое значение в компактный формат с суффиксами
        (T — триллионы, B — миллиарды, M — миллионы). Возвращает строку.

        Правила:
        - Если значение None или не может быть преобразовано в число — возвращает "-".
        - Значения ≥ 1e12 форматируются как "<число> T".
        - Значения ≥ 1e9 форматируются как "<число> B".
        - Значения ≥ 1e6 форматируются как "<число> M".
        - Меньшие значения выводятся с разделением тысяч, без дробной части.

        Примеры:
        - 1_500_000      → "1.5 M"
        - 2_300_000_000  → "2.3 B"
        - 800            → "800"
        - None           → "-"
    """
    if value_int is None:
        return "-"
    try:
        num = float(str(value_int).replace(",", ""))
    except ValueError:
        return "-"

    if num >= 1e12:
        return f"{num / 1e12:.1f} T"
    if num >= 1e9:
        return f"{num / 1e9:.1f} B"
    if num >= 1e6:
        return f"{num / 1e6:.1f} M"
    return f"{num:,.0f}"


def render_format_price(format_price: str) -> str:
    """
       Форматирует строку с ценой токена и возвращает готовую HTML-разметку.

       Правила:
       - Если значение пустое или None — возвращает тире в виде
         безопасного HTML: <span class="none">—</span>.
       - Если строка содержит три секции, разделённые символом "|",
         форматируется как: <b>$ {price}</b> (0x{hex}) <b>{usd}</b>.
       - В остальных случаях:
           - если значение содержит более одной точки (например, "0.0001.000"),
             обрезаются завершающие нули;
           - результат выводится в виде <b>${value}</b>.
       - Возвращает безопасную HTML-строку через mark_safe.
   """
    if not format_price:
        return mark_safe('<span class="none">—</span>')

    split_list = format_price.split('|')
    if len(split_list) > 2:
        return mark_safe(
            f'<b>$ {split_list[0]}</b> (0x{split_list[1]}) <b>{split_list[2]}</b>'
        )

    check_len_price_str = len(format_price.split('.'))
    # print(f"\n\n!!! Checking Len price STR: {check_len_price_str}")
    format_price = format_price.rstrip('0') if check_len_price_str > 2 else format_price
    return mark_safe(f'<b>${format_price}</b>')


def formatted_launch_date(date_type: date) -> str:
    """
        Форматирует дату в строку вида: "20 June 2023".

        Правила:
        - Если дата отсутствует (None), возвращает строку "--".
        - Если дата присутствует, преобразует её через strftime("%d %B %Y").
          Формат:
            %d — день
            %B — полное название месяца на текущем языке локали
            %Y — год
        - Ожидает объект datetime.date.
    """
    if not date_type:
        return "--"
    return date_type.strftime("%d %B %Y")


def get_used_chains() -> list[dict[str, str]]:
    cache_key = f"used_chains"
    cache_ttl = 600  # время жизни кеша в секундах (например, 10 минут)
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        # logfire.info("Кэш-попадание для get_used_chains")
        return cached_result

    qs = Chain.objects.filter(coin__is_published=True).distinct()
    used_chains = [{
        'slug': obj.slug,
        'name': obj.name,
        'symbol': obj.symbol.upper(),
        } for obj in qs]

    # Сохраняем результат в кеш
    cache.set(cache_key, used_chains, cache_ttl)
    # logfire.info("Кэш установлен для get_used_chains", ttl=cache_ttl)

    return used_chains


def get_socials_data():
    cache_key = f"socials_data"
    cache_ttl = 600  # время жизни кеша в секундах (например, 10 минут)
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        # logfire.info("Кэш-попадание для get_used_chains")
        return cached_result

    SOCIAL_VALUES = (
        'facebook', 'whitepaper', 'reddit',
        'twitter', 'gecko', 'discord',
        'market', 'website', 'github',
        'youtube', 'tiktok', 'medium',
        'instagram', 'telegram',
    )

    socials = ImageSocial.objects.filter(slug__in=SOCIAL_VALUES)
    socials_data = []
    if socials.exists():
        for social in socials:
            socials_data.append({
                'name': social.name,
                'slug': social.slug,
                'img': social.image.url if social.image else '',
            })

    # Сохраняем результат в кеш
    cache.set(cache_key, socials_data, cache_ttl)
    return socials_data

