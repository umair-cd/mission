import decimal
from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from solo.models import SingletonModel
from apps.utils.sprinklr import SprinklrService
from optimized_image.fields import OptimizedImageField
from .fields import CharFieldWithTextarea


class HasMeta(models.Model):
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = CharFieldWithTextarea(max_length=320, blank=True)
    meta_keywords = CharFieldWithTextarea(max_length=320, blank=True)
    meta_og_image = OptimizedImageField(null=True, blank=True)
    meta_og_title = models.CharField(max_length=150, blank=True)
    meta_og_description = CharFieldWithTextarea(max_length=320, blank=True)

    class Meta:
        abstract = True


class SimpleHero(models.Model):
    eyebrow_title = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    hero_image = OptimizedImageField(null=True, blank=True)

    class Meta:
        abstract = True


class HasVideo(models.Model):
    video_id = models.CharField(
        max_length=255,
        null=True, blank=True,
        help_text="Video ID for video, e.g. https://www.youtube.com/watch?v=7NONdwbqRV8, id would be 7NONdwbqRV8")
    video_image = OptimizedImageField(null=True, blank=True, help_text="Poster image for video. If empty, you tube defaul image is used")

    class Meta:
        abstract = True


class HomeCarousel(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, help_text="First line of title")
    sub_title = models.CharField(max_length=200, null=True, blank=True, help_text="Second line of title")
    order = models.PositiveIntegerField(default=100)
    background_image = OptimizedImageField(null=True, blank=True, help_text="Background image of carousel slide")
    cta_text = models.CharField(max_length=200, null=True, blank=True, default="Explore Recipes")
    cta_url = models.CharField(max_length=200, null=True, blank=True, default="/recipes")

    def __str__(self):
        return "{} {}".format(self.title, self.sub_title)

    class Meta:
        verbose_name = "Home Carousel"
        verbose_name_plural = "Home Carousel Slides"

        ordering = ["order"]


class Category(HasMeta):
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=75)
    order = models.PositiveIntegerField(default=100)
    image = OptimizedImageField(null=True, blank=True, help_text="Image should be 210x256")
    marquee_image = OptimizedImageField(null=True, blank=True, help_text="Marquee Image for Category page")
    floodlight_cat = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

        ordering = ["order"]


class SubCategory(HasMeta):
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=75, null=True, blank=True)
    order = models.PositiveIntegerField(default=100)
    description = models.TextField(null=True, blank=True)
    list_image = OptimizedImageField(null=True, blank=True, help_text="Image used in product categories page")
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"

        ordering = ["order"]


class Product(HasMeta):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=75)
    upc_code = models.CharField(max_length=55, null=True, blank=True, help_text="UPC Code")
    image = OptimizedImageField(
        null=True, blank=True,
        help_text="Primary product image used on detail and landing pages")
    description = models.TextField(null=True, blank=True)
    availability_cta = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Availability Disclaimer",
        help_text="example: This product is available only in the US")
    is_featured_on_homepage = models.BooleanField(
        help_text="Check if this product should be featured on the product landing page")
    homepage_cta = models.CharField(
        max_length=150,
        blank=True,
        default="Learn More",
        verbose_name="Homepage Product CTA",
        help_text="'Learn More` CTA Use in featured recipes and featured products section of homepage")
    featured_order = models.SmallIntegerField(
        default=100,
        help_text="3rd product on homepage will be centered and highlighted")
    is_new = models.BooleanField(
        default=False,
        null=False)
    sub_category = models.ManyToManyField(SubCategory, related_name="product")
    featured_recipe = models.ForeignKey("Recipe", blank=True, null=True, related_name="featured_recipe")
    ingredients = models.TextField(blank=True, null=True)
    calories = models.CharField(max_length=55, null=True, blank=True, help_text="Ex. 130")
    fiber = models.CharField(max_length=55, null=True, blank=True, help_text="Ex. 5g")
    protein = models.CharField(max_length=55, null=True, blank=True, help_text="Ex. 3g")
    trans_fat = models.CharField(max_length=55, null=True, blank=True, help_text="Ex. 0g")
    carbs = models.CharField(max_length=55, null=True, blank=True, help_text="Ex. 24g")
    cholestrol = models.CharField(max_length=55, null=True, blank=True, help_text="Ex. 0mg")
    is_gluten_free = models.BooleanField(help_text="Show the GF logo", default=False)
    no_artificial_colors = models.BooleanField(help_text="Show no artificial colors logo", default=False)
    no_artificial_flavors = models.BooleanField(help_text="Show no artificial flavors logo", default=False)
    nutritional_facts = OptimizedImageField(null=True, blank=True, help_text="Used to display nutritional facts label")
    related_recipe_text = models.TextField(null=True, blank=True)
    related_recipes = models.ManyToManyField(
        "Recipe",
        through='ProductRelatedRecipe',
        related_name="product_related_recipes",
        verbose_name="Related Recipes")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    floodlight_cat = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['order']


class ProductRelatedRecipe(models.Model):
    recipe = models.ForeignKey("Recipe")
    product = models.ForeignKey(Product)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.recipe.title

    class Meta:
        unique_together = ("recipe", "product")
        ordering = ["order"]
        verbose_name = "Related Recipe"
        verbose_name = "Related Recipes"


class ProductDetailImage(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = OptimizedImageField()
    product = models.ForeignKey(Product, related_name="product_image")
    order = models.PositiveIntegerField(default=100)

    class Meta:
        verbose_name = "Product Detail Image"
        verbose_name_plural = "Product Detail Images"
        ordering = ["order"]


class Option(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, related_name="product_options")

    def __str__(self):
        return self.name


class Collection(HasMeta):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=75)
    description = models.TextField(null=True, blank=True)
    image = OptimizedImageField(null=True, blank=True, help_text="Marquee Image")
    order = models.IntegerField(default=100)
    floodlight_cat = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Recipe(HasVideo, HasMeta):
    MEAL_TYPES = (
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack")
    )
    RECIPE_TYPES = (
        ("gluten-free", "Gluten-free"),
        ("vegetarian", "Vegetarian"),
        ("popular", "Most Popular"),
        ("kid-friendly", "Kid Friendly")
    )
    COOK_TIMES = (
        ("<10", "< 10 Minutes"),
        ("<20", "< 20 Minutes"),
        ("<30", "< 30 Minutes"),
        (">30", "> 30 Minutes")
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=75)
    description = models.TextField(null=True, blank=True)
    image = OptimizedImageField(null=True, blank=True, help_text="Marquee Image")
    featured_product = models.ForeignKey("Product", blank=True, null=True)
    influencer = models.CharField(max_length=200, blank=True)
    influencer_image = OptimizedImageField(null=True, blank=True)
    meal_type = models.CharField(max_length=100, blank=True, choices=MEAL_TYPES)
    recipe_type = models.CharField(max_length=100, blank=True, choices=RECIPE_TYPES)
    prep_time = models.PositiveSmallIntegerField(default=0, help_text="Prep time in minutes")
    cook_time = models.PositiveSmallIntegerField(default=0, help_text="Cook time in minutes")
    makes = models.CharField(max_length=100)
    nutrition = models.CharField(max_length=100, blank=True)
    featured_collection = models.ForeignKey("Collection", blank=True, null=True, related_name="featured_collection")
    collections = models.ManyToManyField(Collection)
    is_featured_on_homepage = models.BooleanField(
        help_text="Check if this recipe should be featured on the homepage")
    homepage_featured_order = models.SmallIntegerField(default=100)
    nutritional_facts = OptimizedImageField(null=True, blank=True, help_text="Used to display nutritional facts label")
    average_rating = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="The average rating the Sprinklr Service returned for this recipe",
        default=decimal.Decimal(0.00)
    )

    @property
    def get_metric_count(self):
        metrics = [
            self.prep_time, self.cook_time, self.makes, self.nutrition
        ]
        return len([m for m in metrics if m])

    def __str__(self):
        return self.title

    def related_recipes(self):
        collections_id = self.collections.all().values_list('id', flat=True)
        return Recipe.objects.filter(collections__in=collections_id).exclude(id=self.id)[:4]

    def get_reviews(self):
        sprinklr = SprinklrService()
        reviews = sprinklr.recipe_reviews(recipe_id=self.slug)
        return reviews

    def get_average_rating(self):
        sprinklr = SprinklrService()
        return sprinklr.recipe_ratings(recipe_id=self.slug)


class Ingredient(models.Model):
    FRACTIONS = (
        ("eigth", "1/8"),
        ("quarter", "1/4"),
        ("third", "1/3"),
        ("half", "1/2"),
        ("two-thirds", "2/3"),
        ("three-quarters", "3/4")
    )
    amount = models.PositiveIntegerField(blank=True, null=True)
    fraction = models.CharField(max_length=100, blank=True, null=True, choices=FRACTIONS)
    name = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, related_name="recipe_ingredient")
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class InstructionStep(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = OptimizedImageField(null=True, blank=True, help_text="Marquee Image")
    recipe = models.ForeignKey(Recipe, related_name="recipe_instruction")
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class RecipeNavigation(SingletonModel):
    featured_collections = models.ManyToManyField(
        Collection,
        through='RecipeNavCollection',
        verbose_name="Recipe Nav Collections")
    featured_recipe_eyebrow = models.CharField(max_length=200, blank=True, default="Featured Recipe")
    featured_recipe = models.ForeignKey(Recipe, null=True, related_name="nav_recipe")
    featured_collection_eyebrow = models.CharField(max_length=200, blank=True, default="Featured Collection")
    featured_collection = models.ForeignKey(Collection, null=True, related_name="nav_collection")


class RecipeNavCollection(models.Model):
    recipe_nav = models.ForeignKey(RecipeNavigation)
    collection = models.ForeignKey(Collection)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.collection.title

    class Meta:
        unique_together = ("recipe_nav", "collection")
        ordering = ["order"]
        verbose_name = "Recipe Nav Collection"
        verbose_name = "Recipe Nav Collections"


class RecipeLandingPage(SingletonModel, HasMeta):
    hero_collections = models.ManyToManyField(
        Collection,
        through='RecipePageHeroCollection',
        related_name="recipe_page_hero_collections",
        verbose_name="Recipe Hero Collections")
    collections_title = models.CharField(max_length=200)
    collections = models.ManyToManyField(
        Collection,
        through='RecipePageCollection',
        related_name="recipe_page_collections",
        verbose_name="Recipe Collections")


class RecipePageCollection(models.Model):
    recipe_page = models.ForeignKey(RecipeLandingPage)
    collection = models.ForeignKey(Collection)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.collection.title

    class Meta:
        unique_together = ("recipe_page", "collection")
        ordering = ["order"]
        verbose_name = "Recipe Page Collection"
        verbose_name = "Recipe Page Collections"


class RecipePageHeroCollection(models.Model):
    recipe_page = models.ForeignKey(RecipeLandingPage)
    collection = models.ForeignKey(Collection)
    eyebrow_text = models.CharField(max_length=200, default="Featured Collection")
    cta_text = models.CharField(max_length=200, default="View Recipe Collection")
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.collection.title

    class Meta:
        unique_together = ("recipe_page", "collection")
        ordering = ["order"]
        verbose_name = "Recipe Page Hero Collection"
        verbose_name = "Recipe Page Hero Collections"


class Careers(SingletonModel, HasMeta):
    eyebrow_title = models.CharField(max_length=100, default="Careers", blank=True)
    header = models.CharField(max_length=200, help_text="The title careers page will have.")
    text = models.TextField(help_text="Description text about the careers page.")
    cta_text = models.CharField(max_length=32, help_text="Text on the button that will redirect user to open positions.")
    cta_url = models.URLField(help_text="Open positions url.")
    legal_header = models.CharField(max_length=200, blank="")
    legal_copy = models.TextField(help_text="Legal verbatim.")

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "Careers"
        verbose_name_plural = "Careers"


class FAQ(SingletonModel, HasMeta):
    title = models.CharField(
        max_length=200,
        help_text="Title for the FAQ section")
    description = models.TextField(
        null=True, blank=True,
        help_text="Small description of the FAQ section")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ Section"


class FAQCategory(models.Model):
    title = models.CharField(
        max_length=200, help_text="Categories that will appear on the FAQ section")
    description = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "FAQ Caregory"
        verbose_name_plural = "FAQ Categories"

        ordering = ["order"]


class Question(models.Model):
    category = models.ForeignKey(FAQCategory)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "FAQ Questions"

        ordering = ["category__title", "order"]


class GenericPage(HasMeta):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=75)
    subtitle = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class SprinklrUser(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.email

    def sprinklr_id(self):
        return "{0}-{1}".format(self.name, self.id).lower().replace(" ", "")


class HistoryHeader(SingletonModel, SimpleHero, HasMeta):
    intro_text = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Our History Pages"
        verbose_name = "Our History Page"


class HistoryPage(models.Model):
    CATEGORIES = (
        ('none', '-'),
        ('us', 'US'),
        ('world', 'World')
    )
    NO_DATE = 0
    JUST_YEAR = 1
    JUST_MONTH = 2
    MONTH_YEAR = 3
    FULL_DATE = 4
    DATES_FORMAT = (
        (JUST_YEAR, "Show just year i.e 2018"),
        (JUST_MONTH, "Show just month i.e January"),
        (MONTH_YEAR, "Show month and year i.e Jan, 2018"),
        (FULL_DATE, 'Show month, day, then year'),
        (NO_DATE, "Hide date and dot")
    )
    date = models.DateField()
    date_format = models.IntegerField(choices=DATES_FORMAT, default=JUST_YEAR)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=450, null=True, blank=True, help_text="Limit description to around 350 characters (including whitespace)")
    image = OptimizedImageField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, default="none", help_text="Set category to determine if the article belongs in US or Around the Globe carousel, leave default to populate article under Mission News")
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.date, self.title)

    def date_formatted(self):
        date_options = {
            1: self.date.strftime("%Y"),
            2: self.date.strftime("%b"),
            3: self.date.strftime("%b %Y"),
            4: self.date.strftime("%b %d %Y")
        }
        return date_options.get(self.date_format)

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Our History Events"
        verbose_name = "Our History Event"


class ContactUsPage(SingletonModel, SimpleHero, HasMeta):
    intro_text = models.TextField(blank=True)
    side_bar_title = models.CharField(max_length=100, blank=True)
    side_bar_text = models.TextField(blank=True)
    side_bar_cta = models.CharField(max_length=100, blank=True)
    side_bar_cta_link = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Contact Us Page"


class Homepage(SingletonModel, HasMeta):
    eyebrow_title_recipe = models.CharField(max_length=100, default='', verbose_name='Featured Recipe Eyebrow Title')
    featured_recipe_title = models.CharField(max_length=100)
    featured_recipe_description = models.TextField(null=True, blank=True)

    eyebrow_title_influencer = models.CharField(max_length=100, default='', verbose_name='Featured Influencer Eyebrow Title')
    featured_influencer_title = models.CharField(max_length=100)
    featured_influencer_description = models.TextField(null=True, blank=True)
    featured_influencer_image = OptimizedImageField(null=True, blank=True)

    eyebrow_title_product = models.CharField(max_length=100, default='', verbose_name='Featured Product Eyebrow Title')
    featured_product_title = models.CharField(max_length=100)
    featured_product_description = models.TextField(null=True, blank=True)

    social_headline = models.CharField(max_length=100, blank=True)
    social_intro_text = CharFieldWithTextarea(max_length=300, blank=True)

    here_to_make_text = models.CharField(max_length=100, default="I'm here to make ", blank=True)
    collections = models.ManyToManyField(Collection, through='HomepageCollection', verbose_name="Here to Make Collections")

    def __str__(self):
        return 'Homepage {0}'.format(self.id)


class HomepageCollection(models.Model):
    homepage = models.ForeignKey(Homepage)
    collection = models.ForeignKey(Collection)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.collection.title

    class Meta:
        unique_together = ("homepage", "collection")
        ordering = ["order"]
        verbose_name = "Ready for a quick snack"
        verbose_name_plural = "Ready for a quick snack"


class AboutUs(SingletonModel, HasMeta):
    eyebrow_hero = models.CharField(max_length=100, default='About Us', verbose_name='Hero Eyebrow Title')
    hero_title = models.CharField(max_length=100)
    hero_image = OptimizedImageField(blank=True, verbose_name="Hero Image")
    hero_subtitle = CharFieldWithTextarea(max_length=255, blank=True)
    main_copy = models.TextField(blank=True)
    tile_set1_eyebrow = models.CharField(
        max_length=100, default="Our History", verbose_name="Top Tile Set Eyebrow Title")
    tile_set1_title1 = models.CharField(
        max_length=100, verbose_name="Top Tile Set Title 1", help_text="First half of title in gray")
    tile_set1_title2 = models.CharField(
        max_length=100,
        verbose_name="Top Tile Set Title 2",
        help_text="2nd half of title in yellow")
    tile_set1_description = CharFieldWithTextarea(
        max_length=300, blank=True, verbose_name="Top Tile Set Description")
    tile_set1_cta_text = models.CharField(
        max_length=100, blank=True, verbose_name="Top Tile Set CTA Text")
    tile_set1_cta_link = models.CharField(
        max_length=255, blank=True, verbose_name="Top Tile Set CTA Link")
    tile_set1_image = OptimizedImageField(null=True, blank=True, verbose_name="Top Tile Set Image")

    tile_set2_eyebrow = models.CharField(
        max_length=100, default="Sustainability", verbose_name="Bottom Tile Set Eyebrow Title")
    tile_set2_title1 = models.CharField(
        max_length=100, verbose_name="Bottom Tile Set Title 1", help_text="First half of title in gray")
    tile_set2_title2 = models.CharField(
        max_length=100, verbose_name="Bottom Tile Set Title 2", help_text="2nd half of title in yellow")
    tile_set2_description = CharFieldWithTextarea(
        max_length=300,
        blank=True,
        verbose_name="Bottom Tile Set Description")
    tile_set2_cta_text = models.CharField(
        max_length=100, blank=True, verbose_name="Bottom Tile Set CTA Text")
    tile_set2_cta_link = models.CharField(
        max_length=255, blank=True, verbose_name="Bottom Tile Set CTA Link")
    tile_set2_image = OptimizedImageField(null=True, blank=True, verbose_name="Bottom Tile Set Image")

    def __str__(self):
        return 'About Us {0}'.format(self.id)

    class Meta:
        verbose_name = "About Us"


class AboutUsCards(models.Model):
    title = models.CharField(max_length=100)
    description = CharFieldWithTextarea(max_length=300, blank=True)
    cta_text = models.CharField(max_length=100, blank=True, verbose_name="CTA Text")
    link = models.CharField(max_length=255, blank=True)
    about_us = models.ForeignKey(AboutUs, related_name="about_us_cards")
    order = models.SmallIntegerField(default=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class ProductPage(SingletonModel, HasMeta):
    eyebrow_title = models.CharField(max_length=100, default='Our Products', verbose_name='Hero Eyebrow Title')
    title = models.CharField(max_length=100)
    sub_title = models.TextField(null=True, blank=True)
    product_category_headline = models.CharField(max_length=150)
    hero_image = OptimizedImageField(null=True, blank=True)

    featured_eyebrow_title = models.CharField(max_length=100, blank=True)
    featured_title1 = models.CharField(max_length=100, blank=True)
    featured_title2 = models.CharField(max_length=100, blank=True)
    featured_description = CharFieldWithTextarea(max_length=300, blank=True)
    featured_cta_text = models.CharField(max_length=100, blank=True, verbose_name="Featured CTA Text")
    featured_link = models.CharField(max_length=300, blank=True)
    featured_image = OptimizedImageField(null=True, blank=True)

    def __str__(self):
        return self.title

class CollectionLandingPage(SingletonModel, SimpleHero, HasMeta):
    hero_paragraph = models.TextField(blank=True)

    class Meta:
        verbose_name = "Collection Landing Page"


class SustainabilityPage(SingletonModel, SimpleHero, HasVideo, HasMeta):
    top_logo = OptimizedImageField(null=True, blank=True)
    top_paragraphs = models.TextField(blank=True)
    callout_text = CharFieldWithTextarea(max_length=300, blank=True, help_text="This is the text that is on the black background")
    first_header = models.CharField(max_length=200, blank=True)
    video_header = models.CharField(max_length=200, blank=True)
    recycyle_header = models.CharField(max_length=200, blank=True)
    recycyle_text = CharFieldWithTextarea(max_length=300, blank=True)
    source_title = models.CharField(max_length=100, blank=True, default="Information Source:")
    source_logo = OptimizedImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Sustainability Page"


class CommitmentListItem(models.Model):
    text = CharFieldWithTextarea(max_length=400, blank=True)
    sustainability_page = models.ForeignKey(SustainabilityPage, related_name="commitment_list")
    order = models.SmallIntegerField(default=100)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ["order"]


class EcoStat(models.Model):
    title = models.CharField(max_length=200)
    text = CharFieldWithTextarea(max_length=300, blank=True)
    sustainability_page = models.ForeignKey(SustainabilityPage, related_name="ecostat_list")
    order = models.SmallIntegerField(default=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class WhereToBuy(SingletonModel, SimpleHero, HasMeta):
    intro_text = models.TextField(blank=True)


class CampaignPage(HasMeta):
    title = models.CharField(max_length=200, help_text="Only used within Admin")
    slug = models.SlugField(max_length=75, help_text="the url of the page")
    head_content = models.TextField(blank=True)
    body_class = models.CharField(max_length=150, blank=True, help_text="set class of body tag")
    js_content = models.TextField(blank=True, help_text="added to end of page with other javascript content")
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

class DynamicCampaignPage(HasMeta, SingletonModel):
    title = models.CharField(max_length=200, help_text="Campaign title")
    slug = models.SlugField(max_length=75, help_text="Friendly campaign identifier in the url path")
    hero_section_is_visible = models.BooleanField(
        default = True,
        help_text = "Check if hero section should be visible in dynamic campaign page"
    )
    highlighted_products_section_is_visible = models.BooleanField(
        default = True,
        help_text = "Check if highlighted products section should be visible in dynamic campaign page"
    )
    highlighted_products_section_title = models.CharField(
        max_length = 200,
        help_text = "Highlighted products section title",
        default = 'Highlighted Products'
    )
    highlighted_products_section_description = models.CharField(
        max_length = 200,
        help_text = "Highlighted products section description",
        default = 'Highlighted Products'
    )
    additional_products_section_is_visible = models.BooleanField(
        default = True,
        help_text = "Check if additional products section should be visible in dynamic campaign page"
    )
    additional_products_section_title = models.CharField(
        max_length = 200,
        help_text = "Additional products section title",
        default = 'Additional Products'
    )
    find_a_store_section_is_visible = models.BooleanField(
        default = True,
        help_text = "Check if find a store section should be visible in dynamic campaign page"
    )
    influencers_section_is_visible = models.BooleanField(
        default = True,
        help_text = "Check if influencers section should be visible in dynamic campaign page"
    )
    influencers_section_title = models.CharField(
        max_length = 200,
        help_text = "Influencers section title",
        default = 'Influencers'
    )
    influencers_section_description = models.CharField(
        max_length = 200,
        help_text = "Influencers section description",
        default = 'Influencers'
    )
    recipes_section_is_visible = models.BooleanField(
        default = True,
        help_text = "Check if recipes section should be visible in dynamic campaign page"
    )
    recipes_section_title = models.CharField(
        max_length = 200,
        help_text = "Recipes section title",
        default = 'Recipes'
    )
    recipes_section_description = models.CharField(
        max_length = 200,
        help_text = "Recipes section description",
        default = 'Recipes'
    )
    recipes_section_button_label = models.CharField(
        max_length = 200,
        help_text = "Recipes section button label",
        default = 'Recipes'
    )
    recipes_section_button_link = models.CharField(
        max_length = 200,
        help_text = "Recipes section button link",
        default = 'Recipes'
    )


    def __str__(self):
        return self.title

    def as_context(self):
        hero_images = map(
            lambda hero_image: hero_image.as_context(),
            self.dynamiccampaignheroimage_set.all()
        )
        highlighted_products = map(
            lambda product: product.as_context(),
            self.dynamiccampaignhighlightedproduct_set.all()
        )
        additional_products = map(
            lambda additional_product: additional_product.as_context(),
            self.dynamiccampaignadditionalproduct_set.all()
        )
        influencers = map(
            lambda influencer: influencer.as_context(),
            self.dynamiccampaigninfluencer_set.all()
        )
        recipes = map(
            lambda recipe: recipe.recipe,
            self.dynamiccampaignrecipe_set.all()
        )

        return {
            'title': self.title,
            'slug': self.slug,
            'hero_section': {
                'visible' : self.hero_section_is_visible,
                'images' : list(hero_images),
            },
            'highlighted_products_section': {
                'visible': self.highlighted_products_section_is_visible,
                'title': self.highlighted_products_section_title,
                'description': self.highlighted_products_section_description,
                'products': list(highlighted_products)
            },
            'additional_products_section': {
                'visible': self.additional_products_section_is_visible,
                'title': self.additional_products_section_title,
                'products': list(additional_products)
            },
            'find_a_store_section':{
                'visible': self.find_a_store_section_is_visible
            },
            'influencers_section': {
                'visible': self.influencers_section_is_visible,
                'title': self.influencers_section_title,
                'description': self.influencers_section_description,
                'influencers': list(influencers)
            },
            'recipes_section': {
                'visible': self.recipes_section_is_visible,
                'title': self.recipes_section_title,
                'description': self.recipes_section_description,
                'button_label': self.recipes_section_button_label,
                'button_link': self.recipes_section_button_link,
                'recipes': list(recipes)
            }
	    }

class DynamicCampaignHeroImage(models.Model):
    dynamic_campaign_page = models.ForeignKey("DynamicCampaignPage")
    image = OptimizedImageField(null=True, blank=True, help_text="Background image of carousel slide")
    image_alt_text = models.CharField(max_length=200, help_text="Text to use when image is not loaded")
    cta_button_label = models.CharField(max_length=50, help_text="Text to use inside the CTA button")
    cta_button_link = models.CharField(max_length=200, help_text="Text to use as CTA button action")

    def as_context(self):
        return {
            'image_url': self.image.url,
            'image_alt_text': self.image_alt_text,
            'cta_button_label': self.cta_button_label,
            'cta_button_link': self.cta_button_link
	    }

class DynamicCampaignHighlightedProduct(models.Model):
    dynamic_campaign_page = models.ForeignKey("DynamicCampaignPage")
    product = models.ForeignKey("Product")
    link_label = models.CharField(
        max_length=50,
        help_text="Text to use for the link",
        default='Visit'
    )

    def as_context(self):
        return {
            'image_url': self.product.image.url,
            'image_alt_text': self.product.description,
            'title': self.product.title,
            'description': self.product.description,
            'link_label': self.link_label,
            'link': reverse('product-detail', args=[self.product.slug])
	    }

class DynamicCampaignAdditionalProduct(models.Model):
    dynamic_campaign_page = models.ForeignKey("DynamicCampaignPage")
    product = models.ForeignKey("Product")
    cta_label = models.CharField(
        max_length=50,
        help_text="Text to use in the CTA",
        default="Learn More"
    )

    def as_context(self):
        return {
            'image_url': self.product.image.url,
            'title': self.product.title,
            'cta_label': self.cta_label,
            'cta_link': reverse('product-detail', args=[self.product.slug])
	    }

class DynamicCampaignInfluencer(models.Model):
    dynamic_campaign_page = models.ForeignKey("DynamicCampaignPage")
    image = OptimizedImageField(null=True, blank=True, help_text="Influencer image")
    image_alt_text = models.CharField(max_length=200, help_text="Text to use when image is not loaded")
    blog_title = models.CharField(max_length=200, help_text="Blog title for the influencer")
    recipe_title = models.CharField(max_length=200, help_text="Recipe title for the influencer")
    button_label = models.CharField(max_length=50, help_text="Text to use in the button")
    button_link = models.CharField(max_length=200, help_text="Link to use in the button")

    def as_context(self):
        return {
            'image_url': self.image.url,
            'image_alt_text': self.image_alt_text,
            'blog_title': self.blog_title,
            'recipe_title': self.recipe_title,
            'button_label': self.button_label,
            'button_link': self.button_link
	    }

class DynamicCampaignRecipe(models.Model):
    dynamic_campaign_page = models.ForeignKey("DynamicCampaignPage")
    recipe = models.ForeignKey("Recipe")
