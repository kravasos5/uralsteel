from django.middleware.csrf import get_token


class CsrfMixin:
    """Миксин, добавляющий в контекст csrf_token"""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        csrf_token = get_token(self.request)
        context['csrf_token'] = csrf_token
        return context
