from rest_framework import routers
from django.urls import include, path
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from account.api.views import (
    UserList,
    UserDetail,
)

router = routers.DefaultRouter()
# router.register(r'users', UserList)
# router.register(r'users', UserDetail)


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', get_schema_view(title='Tersecode API'), name='api_schema'),
    path('docs/', include_docs_urls(title='Tersecode API'), name='api_docs'),

    path('users/', include('account.api.urls')),
    path('problems/', include('problem.api.urls')),
    path('submissions/', include('submission.api.urls')),
]
