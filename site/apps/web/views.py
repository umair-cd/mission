from django.http import Http404
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from . import models
from . import forms
from django.http import HttpResponse
from apps.utils.sprinklr import SprinklrService
import json;
import logging
logger = logging.getLogger('mission')


@method_decorator(cache_page(60 * 5), name='dispatch')
class HomeView(DetailView):
    template_name = "web/index.html"
    context_object_name = "homepage"
    model = models.Homepage

    def get_object(self, *args, **kwargs):
        try:
            homepage = self.model.objects.order_by('id').get()
        except self.model.DoesNotExist:
            raise Http404
        return homepage

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        recipes = models.Recipe.objects.filter(
            is_featured_on_homepage=True).order_by("homepage_featured_order")[:3]
        products = models.Product.objects.filter(
            is_featured_on_homepage=True).order_by("featured_order")
        collections = models.HomepageCollection.objects.filter(homepage=context["homepage"]).only("collection")

        featured_recipe_images = [
            "imgs/Mission-Carb-Balance-Soft-Taco-Flour-Tortilla-1-125x135-transparent.png",
            "imgs/Mission-Fajita-Flour-Tortilla-1-125x135-transparent.png",
            "imgs/Mission-Strips-Tortilla-Chips-1-125x135-transparent.png"

        ]

        # Must be done here to make link absolute
        search_uri = self.request.build_absolute_uri(reverse('products-search'))

        context.update({
            'search_uri': search_uri,
            "home_carousel": models.HomeCarousel.objects.all(),
            "featured_recipes": recipes,
            "featured_products": products,
            "collections": collections,
            "featured_recipe_images": featured_recipe_images
        })
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductsView(ListView):
    template_name = "web/product-categories.html"
    model = models.Category
    context_object_name = 'categories'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            page_info = models.ProductPage.objects.order_by('id').get()
        except self.model.DoesNotExist:
            raise Http404
        context['page_info'] = page_info
        context['object'] = page_info
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class NavigationBarSearchView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        st = self.request.GET.get('st', '')
        q = self.request.GET.get('q', '')
        redirect_options = {
            'products': reverse('products-search'),
            'recipes': reverse('all-recipes'),
            'faq': reverse('faq')
        }
        return '{0}?q={1}'.format(redirect_options[st], q)


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductsSearchView(ListView):
    template_name = "web/products-search.html"
    model = models.Category
    context_object_name = 'categories'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        q = self.request.GET.get("q", "")
        category = self.request.GET.get("category", None)
        subcategory = self.request.GET.get("type", None)
        size = self.request.GET.get("size", None)
        page_info = models.ProductPage.objects.first()

        results = models.Product.objects.all()

        if q:
            results = results.filter(title__icontains=q)
        if category:
            results = results.filter(sub_category__category__title=category)
        if subcategory:
            results = results.filter(sub_category__title=subcategory)
        if size:
            results = results.filter(product_options__name=size)

        context.update({
            "products": results,
            "types": models.SubCategory.objects.all(),
            "options": models.Option.objects.distinct("name"),
            "search": q,
            "active_category": category,
            "active_type": subcategory,
            "active_option": size,
            "page_info": page_info
        })

        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductCategoryDetailView(DetailView):
    """
        Created this combination view to allow products and categories to have the same route
        We use get_object to determine which model/template combination to use
        It looks for a matching category first and then falls back to product
        There will be fewer categories than products to match against
        There is a performance hit doing it this way, should be minor
    """

    def get_object(self, queryset=None):
        # overriding this method to use as a switch between loading category vs product detail

        slug = self.kwargs.get(self.slug_url_kwarg)

        if slug is not None:
            # Check category first
            queryset = models.Category.objects.filter(**{"slug": slug})

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            # successfully got an object.
            # now set the correct template
            self.template_name = "web/category-detail.html"
            self.context_object_name = "category"

        except queryset.model.DoesNotExist:
            # instead of 404ing here. Look in Products next
            queryset = models.Product.objects.filter(**{"slug": slug})
            try:
                obj = queryset.get()
                self.template_name = "web/product-detail.html"
            except queryset.model.DoesNotExist:
                # Raise 404 if not found in products either
                raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if isinstance(context["object"], models.Product):
            # convert the queryset into a list
            images = list(context["object"].product_image.all())
            # now that it's a list we can add primary image to the start
            images.insert(0, context["object"])
            context["product_images"] = images

            # we want 4 related recipes and have 2 ways to get them
            # Either related recipes set on product model
            # Or reverse lookup featured products on recipes
            product_recipes = context["object"].related_recipes.all()[:4]
            diff = 4 - product_recipes.count()
            related_recipes = list(product_recipes)
            if diff > 0:
                more_recipes = list(context["object"].recipe_set.all()[:diff])
                related_recipes = set(related_recipes + more_recipes)
            context["related_recipes"] = related_recipes

        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class SubCategoryDetailView(DetailView):
    template_name = "web/subcategory-detail.html"
    model = models.SubCategory
    context_object_name = 'subcategory'


@method_decorator(cache_page(60 * 5), name='dispatch')
class AllRecipesView(ListView):
    model = models.Recipe
    paginate_by = 12
    context_object_name = 'recipes'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search = self.request.GET.get('q')
        meal_type = self.request.GET.get('meal_type')
        recipe_type = self.request.GET.get('recipe_type')
        cook_time = self.request.GET.get('cook_time')

        if search:
            qs = qs.filter(title__icontains=search)

        if meal_type in dict(models.Recipe.MEAL_TYPES).keys():
            qs = qs.filter(meal_type=meal_type)

        if recipe_type in dict(models.Recipe.RECIPE_TYPES).keys():
            qs = qs.filter(recipe_type=recipe_type)

        if cook_time == "<10":
            qs = qs.filter(cook_time__lte=10)
        if cook_time == "<20":
            qs = qs.filter(cook_time__lte=20)
        if cook_time == "<30":
            qs = qs.filter(cook_time__lte=30)
        if cook_time == ">30":
            qs = qs.filter(cook_time__gte=30)

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page = models.RecipeLandingPage.objects.first()

        search = self.request.GET.get('q')
        meal_type = self.request.GET.get('meal_type')
        recipe_type = self.request.GET.get('recipe_type')
        cook_time = self.request.GET.get('cook_time')

        if not search:
            search = ""

        context.update({
            "page": page,
            "meal_types": models.Recipe.MEAL_TYPES,
            "recipe_types": models.Recipe.RECIPE_TYPES,
            "cook_times": models.Recipe.COOK_TIMES,
            "search": search,
            "active_meal_type": meal_type,
            "active_recipe_type": recipe_type,
            "active_cook_time": cook_time,
            "is_filtered": search or meal_type or recipe_type or cook_time,
            "meta_og_description": page.meta_og_description,
            "meta_og_title": page.meta_og_title
        })
        context['object'] = page
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class RecipeDetailView(FormMixin, DetailView):
    template_name = "web/recipe_detail.html"
    model = models.Recipe
    context_object_name = 'recipe'
    form_class = forms.ReviewForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["reviews"] = context["recipe"].get_reviews()

        system_messages = messages.get_messages(self.request)
        logger.info('RecipeDetailView:get_context_data, messages: {}'.format(len(system_messages)))

        return context

    def send_sprinklr_review(self, title, rate, review, user):
        logger.info('RecipeDetailView:send_sprinklr_review')
        sprinklr = SprinklrService(user_id=user.sprinklr_id())
        payload = {
            'rating': {
                'value': rate
            },
            'title': title,
            'body': review,
            'isBodyHTML': False,
            'productId': self.object.slug
        }

        sprinklr.create_review(payload)

    def create_srinklr_user(self, user):
        logger.info('RecipeDetailView:send_sprinklr_review')
        sprinklr = SprinklrService()
        payload = {
            "id": user.sprinklr_id(),
            "firstName": user.name,
            "displayName": user.name,
            "admin": False,
            "verified": True,
            "trusted": True,
            "anonymous": False,
            "email": user.email
        }
        sprinklr.create_user(payload)

    def prepare_sprinklr_review(self, form_data):
        logger.info('RecipeDetailView:prepare_sprinklr_review')
        user_name = form_data.get('name')
        user_email = form_data.get('email')
        title = form_data.get('title')
        rate = form_data.get('rate')
        review = form_data.get('review')

        try:
            user = models.SprinklrUser.objects.get(email=user_email)
        except models.SprinklrUser.DoesNotExist:
            # No user was found by email, so lets create it our DB and Sprinklr
            user = models.SprinklrUser.objects.create(
                email=user_email,
                name=user_name
            )
            self.create_srinklr_user(user)
        # Create the review with a valid user
        self.send_sprinklr_review(title, rate, review, user)

    def post(self, request, *args, **kwargs):
        logger.info('RecipeDetailView:post')
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.prepare_sprinklr_review(form.cleaned_data)
            return self.form_valid(form)
        else:
            logger.info('RecipeDetailView:post - invalid form')
            return self.form_invalid(form)

    def get_success_url(self):
        logger.info('RecipeDetailView:get_success_url')
        messages.success(self.request, 'Thanks for the review.')
        return reverse('recipe-detail', args=(self.object.slug, ))


@method_decorator(cache_page(60 * 5), name='dispatch')
class CollectionLandingView(ListView):
    model = models.Collection
    context_object_name = 'collections'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["page"] = models.CollectionLandingPage.objects.first()
        context['object'] = context['page']
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class CollectionDetailPageView(DetailView):
    template_name = "web/collection_detail.html"
    model = models.Collection
    context_object_name = "collection"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        collections = models.Collection.objects.all()[:3]
        context["collections"] = collections
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class AboutUsView(DetailView):
    template_name = "web/about-us.html"
    model = models.AboutUs
    context_object_name = "about_us"

    def get_object(self, *args, **kwargs):
        try:
            aboutus = self.model.objects.first()
        except self.model.DoesNotExist:
            raise Http404
        return aboutus

def CCPARequestFormView(request):
    return render(request, 'web/ccpa-request-form.html')

def CCPARequestFormEmailView(request):   
    message ="Type of Request"+"\n"
    requests_type = json.loads(request.POST.get("requests_type"))
    personal_informations = json.loads(request.POST.get("personal_informations"))
    contact_informations = json.loads(request.POST.get("contact_informations"))

    for r in requests_type:
        refine_request = ""
        refine_request_lines =r['request_type'].splitlines()
        for line in refine_request_lines:
            refine_request = refine_request + line.strip()+" "
        refine_request = refine_request+" "+r['status']
        message = message + refine_request + "\n"

    message = message + "What I would like to know about the personal information Mission Foods has on file for me:"+ "\n"

    for info in personal_informations:
        refine_personal_information = ""
        personal_information_lines =info["personal_information"].splitlines()
        for line in personal_information_lines:
            refine_personal_information = refine_personal_information + line.strip()+" "
        refine_personal_information = refine_personal_information + " " + info["status"]
        message = message +refine_personal_information + "\n"

 
    message =message + "Requestor’s Contact Information" + "\n"

    form_type = request.POST.get("form_type")

    if form_type == "form1":
        firstname = request.POST.get("firstname")
        message = message + "First Name " + firstname + "\n" 
        
        lastname = request.POST.get("lastname")
        message = message + "Last Name " + lastname + "\n"
        
        address = request.POST.get("address")
        message = message + "Address " + address + "\n"
        
        city = request.POST.get("city")
        message = message + "City " + city + "\n"

        state = request.POST.get("state")
        message = message + "State " + state + "\n"

        zipcode = request.POST.get("zipcode")
        message = message + "Zip Code " + zipcode + "\n"

        talephone_number = request.POST.get("talephone_number")
        message = message + "Telephone number " + talephone_number + "\n"

        email = request.POST.get("email")
        message = message + "Email " + email + "\n"
    
    if form_type == "form2":
        print("helooo")
        firstname = request.POST.get("firstname")
        message = message + "First Name " + firstname + "\n" 
        
        lastname = request.POST.get("lastname")
        message = message + "Last Name " + lastname + "\n"
        
        business_entity_name = request.POST.get("business_entity_name")
        message = message + "Business Entity Name  " + business_entity_name + "\n"

        relationship_to_consumer = request.POST.get("relationship_to_consumer")
        message = message + "Relationship to Consumer " + relationship_to_consumer + "\n"

        address = request.POST.get("address")
        message = message + "Address " + address + "\n"
        
        city = request.POST.get("city")
        message = message + "City " + city + "\n"

        state = request.POST.get("state")
        message = message + "State " + state + "\n"

        zipcode = request.POST.get("zipcode")
        message = message + "Zip Code " + zipcode + "\n"

        talephone_number = request.POST.get("talephone_number")
        message = message + "Telephone number " + talephone_number + "\n"

        email = request.POST.get("email")
        message = message + "Email " + email + "\n"


    message  = message + "Requestor’s Contact Information"+"\n"

    for contact in contact_informations:
        refine_contact_information = ""
        contact_information_lines = contact["contact"].splitlines()
        for line in contact_information_lines:
            refine_contact_information = refine_contact_information + line.strip() + " "
        refine_contact_information = refine_contact_information +" "+ contact["status"]
        message = message +refine_contact_information + "\n"


    # print(message)
    send_mail(
        'CCPA Request Form',
         message,
        'paswordresetter@gmail.com',
        ['umair.farrukh@gems.techverx.com'],
        fail_silently=False,
    )
    return HttpResponse("yo")#render(request, 'web/ccpa-request-form.html')


@method_decorator(cache_page(60 * 5), name='dispatch')
class SustainabilityView(DetailView):
    template_name = "web/sustainability.html"
    model = models.SustainabilityPage
    context_object_name = "page"

    def get_object(self, *args, **kwargs):
        try:
            page = self.model.objects.first()
        except self.model.DoesNotExist:
            raise Http404
        return page


@method_decorator(cache_page(60 * 5), name='dispatch')
class GenericPageView(DetailView):
    template_name = "web/generic_page_view.html"
    model = models.GenericPage
    context_object_name = "page_info"


@method_decorator(cache_page(60 * 5), name='dispatch')
class CampaignView(DetailView):
    template_name = "web/campaign_view.html"
    model = models.CampaignPage
    context_object_name = "campaign"

@method_decorator(cache_page(60 * 5), name='dispatch')
class DynamicCampaignView(DetailView):
    template_name = "web/dynamic_campaign_view.html"
    context_object_name = "dynamic_campaign"
    model = models.DynamicCampaignPage

    def get_context_data(self, *args, **kwargs):
        context = self.object.as_context()

        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class FaqView(DetailView):
    template_name = "web/faq.html"
    context_object_name = "faq"
    model = models.FAQ

    def get_object(self, *args, **kwargs):
        try:
            faq = models.FAQ.objects.get()
            self.object = faq
        except models.FAQ.DoesNotExist:
            raise Http404
        return faq

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["faq_categories"] = models.FAQCategory.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = self.get_context_data(*args, **kwargs)
        keyword = request.GET.get("q", "")
        context["search_results"] = models.Question.objects.filter(
            question__icontains=keyword)
        context["keyword"] = keyword
        return render(request, self.template_name, context=context)


@method_decorator(cache_page(60 * 5), name='dispatch')
class CareersDetailView(DetailView):
    template_name = "web/careers.html"
    model = models.Careers
    context_object_name = 'careers'

    def get_object(self, *args, **kwargs):
        try:
            careers = models.Careers.objects.get()
        except models.Careers.DoesNotExist:
            raise Http404
        return careers


@method_decorator(cache_page(60 * 5), name='dispatch')
class HistoryPageView(ListView):
    template_name = "web/our-history.html"
    model = models.HistoryPage
    context_object_name = "timeline"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["header"] = models.HistoryHeader.objects.first()
        context["timeline"] = models.HistoryPage.objects.filter(category = 'none')[:4]
        context["timeline_world"] = models.HistoryPage.objects.filter(category = 'world')
        context["timeline_us"] = models.HistoryPage.objects.filter(category = 'us')
        context['object'] = context['header']
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class ContactUsView(DetailView):
    template_name = "web/contact-us.html"
    context_object_name = "contactus"
    model = models.ContactUsPage

    def get_object(self, *args, **kwargs):
        try:
            contactus = self.model.objects.first()
        except self.model.DoesNotExist:
            raise Http404
        return contactus


@method_decorator(cache_page(60 * 5), name='dispatch')
class WhereToBuyView(DetailView):
    template_name = "web/where-to-buy.html"
    context_object_name = "page"

    def get_object(self):
            return get_object_or_404(models.WhereToBuy)

    def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(*args, **kwargs)
            context.update({
                "upc": self.request.GET.get("UPC", "")
            })
            return context


