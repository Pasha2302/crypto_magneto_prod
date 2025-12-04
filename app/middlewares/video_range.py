import os
from django.conf import settings
from django.http import StreamingHttpResponse


class VideoRangeMiddleware:
    """Поддержка HTTP Range для /media/*.mp4 (перемотка в Chrome)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Обрабатываем только .mp4 в MEDIA_URL
        if (
            # URL начинается с /media/ (или что у тебя задано в settings.MEDIA_URL)
            request.path.startswith(settings.MEDIA_URL)
            and request.path.endswith(".mp4")  # запрошенный файл с расширением .mp4
            and response.status_code == 200  # обычный ответ Django (полный файл, без Range)
            and "Range" in request.headers  # браузер запросил диапазон (например: Range: bytes=1000-2000)
        ):
            file_path = os.path.join(settings.MEDIA_ROOT, request.path.replace(settings.MEDIA_URL, "").lstrip("/"))

            if not os.path.exists(file_path):
                return response  # отдадим как есть

            file_size = os.path.getsize(file_path)
            range_header = request.headers["Range"]
            start, end = range_header.replace("bytes=", "").split("-")
            start = int(start) if start else 0
            end = int(end) if end else file_size - 1
            length = end - start + 1

            def file_iterator(path, start, length, chunk_size=8192):
                with open(path, "rb") as f:
                    f.seek(start)  # перемещаемся в файле на стартовую позицию
                    remaining = length  # сколько ещё байт осталось отправить
                    while remaining > 0:
                        chunk = f.read(min(chunk_size, remaining))  # читаем кусок, не больше чем осталось
                        if not chunk:
                            break
                        yield chunk  # отдаем кусок браузеру
                        remaining -= len(chunk)  # уменьшаем количество оставшихся байт

            resp = StreamingHttpResponse(
                file_iterator(file_path, start, length),
                status=206,
                content_type="video/mp4"
            )
            resp["Content-Length"] = str(length)
            resp["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            resp["Accept-Ranges"] = "bytes"

            return resp

        return response
