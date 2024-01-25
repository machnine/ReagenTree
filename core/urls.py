"""
URL configuration for the whole project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from category import urls as category_urls
from company import urls as company_urls
from item.urls import inhouse_urls, item_urls, stock_urls, usage_urls, validation_urls, watchlist_urls
from location import urls as location_urls
from user import urls as user_urls

from .views import SiteWideSearchView, index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("search/", SiteWideSearchView.as_view(), name="site_search"),
    path("", include(user_urls)),
    path("category/", include(category_urls)),
    path("company/", include(company_urls)),
    path("inhouse/", include(inhouse_urls)),
    path("item/", include(item_urls)),
    path("location/", include(location_urls)),
    path("stock/", include(stock_urls)),
    path("usage/", include(usage_urls)),
    path("validation/", include(validation_urls)),
    path("watchlist/", include(watchlist_urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
