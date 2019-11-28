from django.conf.urls import url
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    #ccpa-request-form
    url(r"^ccpa-request-form/$", views.CCPARequestFormView, name="ccpa-request-form"),
    #ccpa-request-email
    url(r"^ccpa-request-email/$", views.CCPARequestFormEmailView, name="ccpa-request-email"),

    url(r"^$", views.HomeView.as_view(), name="home"),
    url(r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    url(r"^search/$", views.NavigationBarSearchView.as_view(), name="nav-search"),

    #about-us page
    url(r"^about-us/$", views.AboutUsView.as_view(), name="about-us"),
    url(r"^sustainability/$", views.SustainabilityView.as_view(), name="sustainability"),

    # product pages

    # workaround for when product cat and sub-cat have the same name, redirect to main cat.
    url(r"^products/wraps/wraps/$", RedirectView.as_view(url='/products/wraps/', permanent=True)),

    url(r"^products/(?P<category>.*)/(?P<slug>.*)/$", views.SubCategoryDetailView.as_view(), name="sub-category-detail"),
    url(r"^products/search/$", views.ProductsSearchView.as_view(), name="products-search"),
    url(r"^products/$", views.ProductsView.as_view(), name="all-products"),
    # These look like duplicate urls, but keeping both so we can reference names separately
    # Allows changeing back to separate urls and unique views without have to update the url names accross the site
    url(r"^products/(?P<slug>.*)/$", views.ProductCategoryDetailView.as_view(), name="product-detail"),
    url(r"^products/(?P<slug>.*)/$", views.ProductCategoryDetailView.as_view(), name="category-detail"),
    # recipe pages
    url(r"^recipes/$", views.AllRecipesView.as_view(), name="all-recipes"),
    url(r"^recipes/collections/$", views.CollectionLandingView.as_view(), name="collection-landing"),
    url(r"^recipes/collections/(?P<slug>.*)/$", views.CollectionDetailPageView.as_view(), name="collection-detail"),
    url(r"^recipes/(?P<slug>.*)/$", views.RecipeDetailView.as_view(), name="recipe-detail"),
    # FAQ page
     url(r"^faq/$", views.FaqView.as_view(), name="faq"),
    #Careers page
    url(r"^careers/$", views.CareersDetailView.as_view(), name="careers"),
    # Our History Page
    url(r"^our-history/$", views.HistoryPageView.as_view(), name="our-history"),
    # Contact Us page
    url(r"^contact-us/$", views.ContactUsView.as_view(), name="contact-us"),
    # Where to Buy/Destini page
    url(r"^where-to-buy/$", views.WhereToBuyView.as_view(), name="where-to-buy"),
    # Generic Pages
    url(r"^supply-chain-transparency/$", views.GenericPageView.as_view(), { "slug": "supply-chain-transparency"}, name="supply-chain"),
    url(r"^privacy-policy/$", views.GenericPageView.as_view(), { "slug": "privacy-policy"}, name="privacy-policy"),
    # Campaigns
    url(r"^campaigns/(?P<slug>.*)/$", views.DynamicCampaignView.as_view(), name="campaign"),
    url(r"^(?P<slug>.*)/$", views.CampaignView.as_view(), name="campaigns"),


    # error states
    url(r"^400/$", default_views.bad_request,
        kwargs={"exception": Exception("Bad Request!")}),
    url(r"^403/$", default_views.permission_denied,
        kwargs={"exception": Exception("Permission Denied")}),
    url(r"^404/$", default_views.page_not_found,
        kwargs={"exception": Exception("Page not Found")}),
    url(r"^500/$", default_views.server_error),
]
