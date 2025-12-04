import logging
import logfire

from django.http import HttpRequest, JsonResponse
from django.db.models import Q

from app.db_models import Coin
from app.views.app.api.tools import parse_request_data

# from django.template.loader import render_to_string


logger = logging.getLogger("app.views")


def search_coin_name_view(request: HttpRequest):
    if request.method == "GET":
        return JsonResponse(data={'error': 'Method Not Allowed' }, status=405)

    query: str = parse_request_data(request=request).get("query")
    logfire.info(f"[search_coin_name_view] / {request.method}", params=query)
    if not isinstance(query, str) or query in ["", "*", "select", "SELECT"]:
        return JsonResponse(data={'error': 'Query must be a string'}, status=400)

    qs_coins = (
        Coin.objects
        .filter(is_published=True)
        .filter(
            Q(name__icontains=query) |
            Q(symbol__icontains=query) |
            Q(chain__name__icontains=query) |
            Q(chain__symbol__icontains=query)
        )
        .distinct()
        .select_related("chain")
        .only(
            "id", "chain_id",
            "name", "symbol", "image",
            "chain__symbol", "chain__slug",
        )[:20]
    )

    coins_data = [{
        "id": coin_obj.pk,
        "name": coin_obj.name,
        "symbol": coin_obj.symbol,
        "url": coin_obj.get_site_url(is_relative_path=True),
        "img": coin_obj.image.url if coin_obj.image else "",
        "chain": coin_obj.chain.symbol.upper() if coin_obj.chain else "",
        "chain_slug": coin_obj.chain.slug if coin_obj.chain else "",
    } for coin_obj in qs_coins]

    data = {'coins': coins_data}

    return JsonResponse(data, status=200)

