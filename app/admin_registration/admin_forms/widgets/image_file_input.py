from django.forms.widgets import ClearableFileInput


class ImageFileInput(ClearableFileInput):
    clear_checkbox_label = None  # Убирает текст для чекбокса (на всякий случай)
    initial_text = "Current file"  # (не обязательно: кастомизируем текст для существующего файла)
    template_name = "app/admin/widgets/image_input_form.html"  # Если нужно кастомизировать HTML виджета

    def __init__(self, attrs=None):
        super().__init__(attrs)
