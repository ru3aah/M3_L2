from django.contrib.messages.context_processors import messages
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin


class MessageHandlerFormMixin:
    success_message = 'Success'
    error_message = 'Error'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class IsAuthorMixin(SingleObjectMixin):
        def dispatch(self, request, *args, **kwargs):
            object_to_handle=self.get_object()
            if object_to_handle.author != request.user:
                raise PermissionDenied
            return super().dispatch(request, *args, **kwargs)





