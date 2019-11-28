from adminsortable2.admin import SortableAdminMixin
from apps.utils.sprinklr import SprinklrService
from django.contrib import admin, messages
from solo.admin import SingletonModelAdmin

from . import models, forms


@admin.register(models.HomeCarousel)
class HomeCarouselAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["title", "order"]


@admin.register(models.Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "order"]


@admin.register(models.SubCategory)
class SubCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "order"]
    ordering = ["order"]
    filter_horizontal = ["category"]
    search_fields = ["title"]


class ProductOptionAdmin(admin.TabularInline):
    model = models.Option
    extra = 1


class ProductRelatedRecipeInline(admin.TabularInline):
    model = models.ProductRelatedRecipe
    max_num = 4


class ProductDetailImageAdmin(admin.TabularInline):
    model = models.ProductDetailImage
    ordering = ["order"]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    def get_sub_categories(self, obj):
        return ", ".join([p.title for p in obj.sub_category.all()])

    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "get_sub_categories", "order"]
    filter_horizontal = ["sub_category"]
    search_fields = ["title"]
    inlines = [ProductOptionAdmin, ProductDetailImageAdmin, ProductRelatedRecipeInline]

    class Media:
        js = (
            'admin/js/tinymce/tinymce/tinymce.min.js',
            'admin/js/tinymce/configure.js',
        )


class RecipeInstructionAdmin(admin.TabularInline):
    model = models.InstructionStep
    extra = 1


class IngredientAdmin(admin.TabularInline):
    model = models.Ingredient
    extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    filter_horizontal = ["collections"]
    search_fields = ["title"]
    inlines = [RecipeInstructionAdmin, IngredientAdmin]

    def save_model(self, request, obj, form, change):
        sprinklr = SprinklrService()
        payload = {
            "id": obj.slug,
            "name": obj.title,
            "url": "http://{0}/recipes/{1}/".format(request.get_host(), obj.slug),
            "description": obj.description
        }

        if not change:
            sprinklr.create_recipe(payload)
            messages.add_message(request, messages.INFO, 'Recipe created in Sprinklr Service')
        else:
            sprinklr.update_recipe(obj.slug, payload)
            messages.add_message(request, messages.INFO, 'Recipe updated in Sprinklr Service')

        super().save_model(request, obj, form, change)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    search_fields = ["title"]


class CareersAdmin(SingletonModelAdmin):
    pass


class FAQAdmin(SingletonModelAdmin):
    pass


@admin.register(models.FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", ]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "answer"]
    search_fields = ["question"]


@admin.register(models.GenericPage)
class GenericPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = (
            'admin/js/tinymce/tinymce/tinymce.min.js',
            'admin/js/tinymce/configure.js',
        )


class CampaignPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["slug", "title"]


@admin.register(models.SprinklrUser)
class SprinklrUserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", ]


@admin.register(models.HistoryPage)
class HistoryPageAdmin(admin.ModelAdmin):
    list_display = ["date", "title", ]
    search_fields = ["title"]

    class Media:
        js = (
            'admin/js/tinymce/tinymce/tinymce.min.js',
            'admin/js/tinymce/configure.js',
        )


class HistoryHeaderAdmin(SingletonModelAdmin):
    pass


class HomepageCollectionInline(admin.TabularInline):
    model = models.HomepageCollection
    max_num = 8


class HomepageAdmin(SingletonModelAdmin):
    inlines = [HomepageCollectionInline, ]


class AboutUsCardsInline(admin.StackedInline):
    model = models.AboutUsCards
    max_num = 3


class AboutUsAdmin(SingletonModelAdmin):
    inlines = [AboutUsCardsInline, ]

    class Media:
        js = (
            'admin/js/tinymce/tinymce/tinymce.min.js',
            'admin/js/tinymce/configure.js',
        )


class ContactUsPageAdmin(SingletonModelAdmin):
    pass


class WhereToBuyAdmin(SingletonModelAdmin):
    pass


class ProductPageAdmin(SingletonModelAdmin):
    pass


class CollectionLandingPageAdmin(SingletonModelAdmin):
    pass


class RecipePageCollectionInline(admin.TabularInline):
    model = models.RecipePageCollection
    max_num = 3


class RecipePageHeroCollectionInline(admin.TabularInline):
    model = models.RecipePageHeroCollection
    max_num = 4


class RecipeLandingPageAdmin(SingletonModelAdmin):
    inlines = [RecipePageHeroCollectionInline, RecipePageCollectionInline]


class RecipeNavCollectionInline(admin.TabularInline):
    model = models.RecipeNavCollection
    max_num = 6


class RecipeNavAdmin(SingletonModelAdmin):
    inlines = [RecipeNavCollectionInline, ]


class CommitmentListInline(admin.StackedInline):
    model = models.CommitmentListItem


class EcoStatInline(admin.StackedInline):
    model = models.EcoStat


class SustainabilityPageAdmin(SingletonModelAdmin):
    inlines = [CommitmentListInline, EcoStatInline]

    class Media:
        js = (
            'admin/js/tinymce/tinymce/tinymce.min.js',
            'admin/js/tinymce/configure.js',
        )


class DynamicCampaignHeroImageInline(admin.TabularInline):
    form = forms.DynamicCampaignHeroImageForm
    model = models.DynamicCampaignHeroImage
    can_delete = True
    extra = 0


class DynamicCampaignHighlightedProductInline(admin.TabularInline):
    form = forms.DynamicCampaignHighlightedProductForm
    model = models.DynamicCampaignHighlightedProduct
    can_delete = True
    extra = 0
    max_num = 3


class DynamicCampaignAdditionalProductInline(admin.TabularInline):
    form = forms.DynamicCampaignAdditionalProductForm
    model = models.DynamicCampaignAdditionalProduct
    can_delete = True
    extra = 0


class DynamicCampaignInfluencerInline(admin.TabularInline):
    form = forms.DynamicCampaignInfluencerForm
    model = models.DynamicCampaignInfluencer
    can_delete = True
    extra = 0


class DynamicCampaignRecipeInline(admin.TabularInline):
    model = models.DynamicCampaignRecipe
    can_delete = True
    extra = 0


class DynamicCampaignPageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'title', 'meta_title', 'meta_description', 'meta_keywords', 'meta_og_image', 'meta_og_title',
                'meta_og_description', 'slug', 'hero_section_is_visible',
                'highlighted_products_section_is_visible', 'highlighted_products_section_title',
                'highlighted_products_section_description', 'additional_products_section_is_visible',
                'additional_products_section_title', 'find_a_store_section_is_visible',
                'influencers_section_is_visible', 'influencers_section_title', 'influencers_section_description',
                'recipes_section_is_visible', 'recipes_section_title', 'recipes_section_description',
                'recipes_section_button_label', 'recipes_section_button_link']
        })
    ]

    model = models.DynamicCampaignPage
    form = forms.DynamicCampaignPageForm
    inlines = [
        DynamicCampaignHeroImageInline,
        DynamicCampaignHighlightedProductInline,
        DynamicCampaignAdditionalProductInline,
        DynamicCampaignInfluencerInline,
        DynamicCampaignRecipeInline
    ]


admin.site.register(models.AboutUs, AboutUsAdmin)
admin.site.register(models.Homepage, HomepageAdmin)
admin.site.register(models.Careers, CareersAdmin)
admin.site.register(models.FAQ, FAQAdmin)
admin.site.register(models.ProductPage, ProductPageAdmin)
admin.site.register(models.CollectionLandingPage, CollectionLandingPageAdmin)
admin.site.register(models.RecipeLandingPage, RecipeLandingPageAdmin)
admin.site.register(models.RecipeNavigation, RecipeNavAdmin)
admin.site.register(models.HistoryHeader, HistoryHeaderAdmin)
admin.site.register(models.ContactUsPage, ContactUsPageAdmin)
admin.site.register(models.SustainabilityPage, SustainabilityPageAdmin)
admin.site.register(models.WhereToBuy, WhereToBuyAdmin)
admin.site.register(models.CampaignPage, CampaignPageAdmin)
admin.site.register(models.DynamicCampaignPage, DynamicCampaignPageAdmin)
