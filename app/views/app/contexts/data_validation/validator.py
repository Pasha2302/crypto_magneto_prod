from django.db.models import QuerySet


class ValidationContextIndex:

    @classmethod
    def validate_image(cls, qs_coins):
        for q in qs_coins:
            if not q.image: q.image = 'default_placeholder.webp'
            if not q.chain.image:
                q.chain.image = 'default_placeholder.webp'
