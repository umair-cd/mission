from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve
# from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


# -------------------------------------
# PROJECT URLS
# -------------------------------------
# See: https://docs.djangoproject.com/en/dev/topics/http/urls/#example

urlpatterns = [
    url(
        r'^uploads/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
    ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include("apps.api.v1.urls")),
    url(r'^', include("apps.web.urls")),
    url(r'^ui-kit', include("apps.ui_kit.urls"))
]

if settings.AUTO_ENABLE_I18N:
    urlpatterns = i18n_patterns(*urlpatterns)

    urlpatterns += [
        url(r'^jsi18n/$',
            JavaScriptCatalog.as_view(packages=['apps.web']),
            name='javascript-catalog'),
    ]


# Non-Localized Urls
# =====================================

urlpatterns += [
]

# -------------------------------------
# DEBUG URLS
# -------------------------------------

if settings.DEBUG:
    # Per latest django debug toolbar
    # See:
    # http://django-debug-toolbar.readthedocs.io/en/stable/installation.html
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Serve media files when DEBUG=True
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
