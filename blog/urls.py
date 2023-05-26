from django.urls import path, include
from django.contrib import admin
from home.views import home_view, data_table, ItemListView

from support.views import support12
from django.conf.urls.static import static
from django.conf import settings
from home.views import ExportExcelView

urlpatterns = [
    path("", home_view, name='home'),

    path('api/', include('post.api.urls')),

    path("support", support12, name='support'),

    path('examples/', include('examples.urls')),

    path('post/', include('post.urls')),

    path("accounts/", include("allauth.urls")),

    path("admin/", admin.site.urls),

    path('data_table/', data_table, name='data_table'),

    path('data_table/data/', ItemListView),

    path('export/excel/', ExportExcelView.as_view(), name='export-excel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
