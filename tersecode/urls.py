from django.urls import include, get_resolver
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, 'base.html')


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('problem/', include('problem.urls')),
    path('account/', include('account.urls')),
    path('submission/', include('submission.urls')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
