from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include('api.urls')),  
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
