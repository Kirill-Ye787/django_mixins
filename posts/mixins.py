from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
import json
class TitleContextMixin:
    page_title = ''
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = getattr(self, 'page_title', '') or self.__class__.__name__
        return ctx
class PaginationMixin:
    paginate_by = 5
    def get_paginate_by(self, queryset):
        return getattr(self, 'paginate_by', self.paginate_by)
class CachePageMixin:
    cache_timeout = 30
    @method_decorator(cache_page(cache_timeout))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = getattr(self, 'get_object', lambda: None)()
        return (self.request.user.is_authenticated and obj is not None and getattr(obj, 'author_id', None) == self.request.user.id)
class JsonRequestBodyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.method in ('POST', 'PUT', 'PATCH') and request.body:
            try:
                self.json_data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return HttpResponseBadRequest('Invalid JSON')
        return super().dispatch(request, *args, **kwargs)
class SuccessMessageMixin:
    success_message = 'Успешно сохранено.'
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, getattr(self, 'success_message', 'Успешно сохранено.'))
        return response
class RequireQueryParamsMixin:
    required_params = []
    def dispatch(self, request, *args, **kwargs):
        missing = [p for p in self.required_params if p not in request.GET]
        if missing:
            return HttpResponseBadRequest(f'Missing query params: {", ".join(missing)}')
        return super().dispatch(request, *args, **kwargs)
class AjaxRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseBadRequest('AJAX only')
        return super().dispatch(request, *args, **kwargs)
class ReadOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            return HttpResponseNotAllowed(['GET', 'HEAD', 'OPTIONS'])
        return super().dispatch(request, *args, **kwargs)
