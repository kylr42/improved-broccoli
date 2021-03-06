from rest_framework import routers
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import TransactionListView, TransactionDetailView, TransactionAccountViewSet

router = routers.DefaultRouter()
router.register(r'accounts', TransactionAccountViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Transaction api docs",
   ),
   public=True,
)

urlpatterns = [
    path('transaction/', TransactionListView.as_view()),
    path('transaction/<int:pk>/', TransactionDetailView.as_view()),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
