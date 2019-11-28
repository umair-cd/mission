import factory

from ..models import Product, Recipe, DynamicCampaignPage, DynamicCampaignHeroImage, DynamicCampaignHighlightedProduct, DynamicCampaignAdditionalProduct, DynamicCampaignInfluencer, DynamicCampaignRecipe

class RecipeFactory(factory.Factory):
    class Meta:
        model = Recipe

    title = factory.Sequence(lambda n: 'Recipe %s' % n)
    slug = factory.Sequence(lambda n: 'recipe-%s' % n)
    description = factory.Faker('sentence')
    image = factory.django.ImageField(color='blue')
    influencer = factory.Faker('sentence')
    influencer_image = factory.django.ImageField(color='blue')
    makes = factory.Faker('sentence')
    nutrition = factory.Faker('sentence')
    is_featured_on_homepage = True
    homepage_featured_order = factory.Sequence(lambda n: n)
    nutritional_facts = factory.django.ImageField(color='blue')
    average_rating = 45

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    title = factory.Sequence(lambda n: 'Product %s' % n)
    slug = factory.Sequence(lambda n: 'product-%s' % n)
    upc_code = factory.Sequence(lambda n: 'upd-code-%s' % n)
    image = factory.django.ImageField(color='blue')
    description = factory.Faker('sentence')
    availability_cta = factory.Faker('sentence')
    is_featured_on_homepage = True
    homepage_cta = factory.Faker('sentence')
    featured_order = factory.Sequence(lambda n: n)
    is_new = True
    featured_recipe = factory.SubFactory(RecipeFactory)
    ingredients = factory.Faker('sentence')
    is_gluten_free = False
    no_artificial_colors = False
    no_artificial_flavors = False
    nutritional_facts = factory.django.ImageField(color='blue')

class DynamicCampaignPageFactory(factory.Factory):
    class Meta:
        model = DynamicCampaignPage

    title = factory.Sequence(lambda n: 'Dynamic Campaign %s' % n)
    slug = factory.Sequence(lambda n: 'dynamic-campaign-%s' % n)
    hero_section_is_visible = True
    additional_products_section_is_visible = True
    additional_products_section_title = factory.Faker('sentence')

class DynamicCampaignHeroImageFactory(factory.Factory):
    class Meta:
        model = DynamicCampaignHeroImage

    dynamic_campaign_page = factory.SubFactory(DynamicCampaignPageFactory)
    image =  factory.django.ImageField(color='blue')
    image_alt_text = factory.Faker('sentence')
    cta_button_label = factory.Faker('slug')
    cta_button_link = factory.Faker('uri')

class DynamicCampaignHighlightedProductFactory(factory.Factory):
    class Meta:
        model = DynamicCampaignHighlightedProduct

    dynamic_campaign_page = factory.SubFactory(DynamicCampaignPageFactory)
    product = factory.SubFactory(ProductFactory)
    link_label = factory.Faker('slug')

class DynamicCampaignAdditionalProductFactory(factory.Factory):
    class Meta:
        model = DynamicCampaignAdditionalProduct

    dynamic_campaign_page = factory.SubFactory(DynamicCampaignPageFactory)
    product = factory.SubFactory(ProductFactory)
    cta_label = factory.Faker('slug')

class DynamicCampaignInfluencerFactory(factory.Factory):
    class Meta:
        model = DynamicCampaignInfluencer

    dynamic_campaign_page = factory.SubFactory(DynamicCampaignPageFactory)
    image =  factory.django.ImageField(color='blue')
    image_alt_text = factory.Faker('sentence')
    blog_title = factory.Faker('sentence')
    recipe_title = factory.Faker('sentence')
    button_label = factory.Faker('slug')
    button_link = factory.Faker('uri')

class DynamicCampaignRecipeFactory(factory.Factory):
    class Meta:
        model = DynamicCampaignRecipe

    dynamic_campaign_page = factory.SubFactory(DynamicCampaignPageFactory)
    recipe = factory.SubFactory(RecipeFactory)
