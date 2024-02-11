from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('back_end/', include('back_end.urls')),
    path('Wallet/', include('Wallet.urls')),
    path('News/', include('News.urls')),
    path('', include('Dashboard.urls')),
    path('', RedirectView.as_view(url='News/news/')),
]
