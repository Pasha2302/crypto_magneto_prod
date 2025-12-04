pass
# from django.db import models
# from django.core.exceptions import ValidationError


# class ChartDescription(models.Model):
#     CHAT_TYPE_CHOICES = (
#         ('', '-----'),
#         ('prices', 'Latest Price'),
#         ('volume', 'Transactions'),
#         ('average_buy_price', 'Avg Buy Price'),
#         ('potential_profit', 'Potential Profit'),
#         ('realized_profit', 'Realized Profit'),
#         ('hodl', 'HODL Days'),
#     )
#
#     type_chart = models.CharField(max_length=255, choices=CHAT_TYPE_CHOICES, default='', db_index=True, unique=True)
#     desc = models.TextField(blank=True, default='', verbose_name='Description')
#
#     class Meta:
#         verbose_name = 'Chart Description'
#         verbose_name_plural = 'Chart Descriptions'
#
#     def __str__(self):
#         return self.get_type_chart_display()


# class FooterDescription(models.Model):
#     title = models.CharField(max_length=255)
#     desc = models.TextField(blank=True, default='', verbose_name='Description')
#     signature = models.CharField(max_length=150)
#
#     class Meta:
#         verbose_name = 'Footer Description'
#
#     def __str__(self):
#         return self.title
#
#     def save(self, *args, **kwargs):
#         if not self.pk and FooterDescription.objects.exists():
#             raise ValidationError('Можно создать только одну запись Footer Description')
#         return super().save(*args, **kwargs)
