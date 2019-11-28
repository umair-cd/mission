from django.test import TestCase
from django.urls import reverse

from ..models import DynamicCampaignPage, DynamicCampaignHeroImage, DynamicCampaignAdditionalProduct
from .factories import *

class DynamicCampaignPageTests(TestCase):
    def test_as_context_returns_the_required_keys(self):
        """
        Dynamic campaigns has the required entries
        when transformed to be used as context without child objects
        """
        dynamic_campaign = DynamicCampaignPageFactory()
        context = dynamic_campaign.as_context()
        self.assertListEqual(
            list(context.keys()),
            [
                'title',
                'slug',
                'hero_section',
                'highlighted_products_section',
                'additional_products_section',
                'find_a_store_section',
                'influencers_section',
                'recipes_section'
            ]
        )
        self.assertListEqual(
            list(context['hero_section'].keys()),
            ['visible', 'images']
        )
        self.assertListEqual(
            list(context['highlighted_products_section'].keys()),
            ['visible', 'title', 'description', 'products']
        )
        self.assertListEqual(
            list(context['additional_products_section'].keys()),
            ['visible', 'title', 'products']
        )
        self.assertListEqual(
            list(context['find_a_store_section'].keys()),
            ['visible']
        )
        self.assertListEqual(
            list(context['influencers_section'].keys()),
            ['visible', 'title', 'description', 'influencers']
        )
        self.assertListEqual(
            list(context['recipes_section'].keys()),
            ['visible', 'title', 'description', 'button_label', 'button_link', 'recipes']
        )
        self.assertListEqual(context['hero_section']['images'], [])
        self.assertListEqual(context['highlighted_products_section']['products'], [])
        self.assertListEqual(context['additional_products_section']['products'], [])
        self.assertListEqual(context['recipes_section']['recipes'], [])

    def test_dynamic_campaign_as_context_with_hero_images(self):
        """
        Dynamic campaigns include context ready hero images
        """
        dynamic_campaign = DynamicCampaignPageFactory()
        dynamic_campaign.save()

        image1 = DynamicCampaignHeroImageFactory(dynamic_campaign_page = dynamic_campaign)
        image2 = DynamicCampaignHeroImageFactory(dynamic_campaign_page = dynamic_campaign)

        image1.save()
        image2.save()

        dynamic_campaign.refresh_from_db()
        context = dynamic_campaign.as_context()
        self.assertEqual(len(context['hero_section']['images']), 2)
        self.assertEqual(
            [*context['hero_section']['images'][0]],
            ['image_url', 'image_alt_text', 'cta_button_label', 'cta_button_link']
        )

    def test_as_context_with_highlighted_products(self):
        """
        Dynamic campaigns include context ready highlighted products
        """
        dynamic_campaign = DynamicCampaignPageFactory()
        dynamic_campaign.save()

        product1 = ProductFactory()
        product2 = ProductFactory()

        product1.featured_recipe.save()
        product2.featured_recipe.save()
        product1.save()
        product2.save()

        hl_product1 = DynamicCampaignHighlightedProductFactory(
            dynamic_campaign_page = dynamic_campaign,
            product = product1
        )
        hl_product2 = DynamicCampaignHighlightedProductFactory(
            dynamic_campaign_page = dynamic_campaign,
            product = product2
        )
        hl_product1.save()
        hl_product2.save()

        dynamic_campaign.refresh_from_db()
        context = dynamic_campaign.as_context()
        self.assertEqual(len(context['highlighted_products_section']['products']), 2)
        self.assertEqual(
            [*context['highlighted_products_section']['products'][0]],
            ['image_url', 'image_alt_text', 'title', 'description', 'link_label', 'link']
        )

    def test_as_context_with_additional_products(self):
        """
        Dynamic campaigns include context ready additional products
        """
        dynamic_campaign = DynamicCampaignPageFactory()
        dynamic_campaign.save()

        product1 = ProductFactory()
        product2 = ProductFactory()

        product1.featured_recipe.save()
        product2.featured_recipe.save()
        product1.save()
        product2.save()

        ad_product1 = DynamicCampaignAdditionalProductFactory(
            dynamic_campaign_page = dynamic_campaign,
            product = product1
        )
        ad_product2 = DynamicCampaignAdditionalProductFactory(
            dynamic_campaign_page = dynamic_campaign,
            product = product2
        )
        ad_product1.save()
        ad_product2.save()

        dynamic_campaign.refresh_from_db()
        context = dynamic_campaign.as_context()
        self.assertEqual(len(context['additional_products_section']['products']), 2)
        self.assertEqual(
            [*context['additional_products_section']['products'][0]],
            ['image_url', 'title', 'cta_label', 'cta_link']
        )

    def test_as_context_with_influencers(self):
        """
        Dynamic campaigns include context ready additional influencers
        """
        dynamic_campaign = DynamicCampaignPageFactory()
        dynamic_campaign.save()

        influencer1 = DynamicCampaignInfluencerFactory(dynamic_campaign_page = dynamic_campaign)
        influencer2 = DynamicCampaignInfluencerFactory(dynamic_campaign_page = dynamic_campaign)
        influencer1.save()
        influencer2.save()

        dynamic_campaign.refresh_from_db()
        context = dynamic_campaign.as_context()
        self.assertEqual(len(context['influencers_section']['influencers']), 2)
        self.assertEqual(
            [*context['influencers_section']['influencers'][0]],
            ['image_url', 'image_alt_text', 'blog_title', 'recipe_title', 'button_label', 'button_link']
        )

    def test_as_context_with_recipes(self):
        """
        Dynamic campaigns include context ready additional recipes
        """
        dynamic_campaign = DynamicCampaignPageFactory()
        dynamic_campaign.save()

        recipe1 = RecipeFactory()
        recipe2 = RecipeFactory()

        recipe1.save()
        recipe2.save()

        dc_recipe1 = DynamicCampaignRecipeFactory(
            dynamic_campaign_page = dynamic_campaign,
            recipe = recipe1
        )
        dc_recipe2 = DynamicCampaignRecipeFactory(
            dynamic_campaign_page = dynamic_campaign,
            recipe = recipe2
        )
        dc_recipe1.save()
        dc_recipe2.save()

        dynamic_campaign.refresh_from_db()
        context = dynamic_campaign.as_context()
        self.assertEqual(context['recipes_section']['recipes'], [recipe1, recipe2])

class DynamicCampaignHeroImageTests(TestCase):
    def test_as_context_returns_the_required_keys(self):
        """
        Dynamic campaign hero image has the required entries
        when transformed to be used as context
        """
        hero_image = DynamicCampaignHeroImageFactory()
        self.assertDictEqual(
            hero_image.as_context(),
            {
                'image_url': hero_image.image.url,
                'image_alt_text': hero_image.image_alt_text,
                'cta_button_label': hero_image.cta_button_label,
                'cta_button_link': hero_image.cta_button_link
            }
        )

class DynamicCampaignHighlightedProductTests(TestCase):
    def test_as_context_returns_the_required_keys(self):
        """
        Dynamic campaign highlighted product has the required entries
        when transformed to be used as context
        """
        highlighted_product = DynamicCampaignHighlightedProductFactory()
        product = highlighted_product.product

        self.assertDictEqual(
            highlighted_product.as_context(),
            {
                'image_url': product.image.url,
                'image_alt_text': product.description,
                'title': product.title,
                'description': product.description,
                'link_label': highlighted_product.link_label,
                'link': ("/products/%s/" %(product.slug))
            }
        )

class DynamicCampaignAdditionalProductTests(TestCase):
    def test_as_context_returns_the_required_keys(self):
        """
        Dynamic additional product has the required entries
        when transformed to be used as context
        """
        additional_product = DynamicCampaignAdditionalProductFactory()
        product = additional_product.product

        self.assertDictEqual(
            additional_product.as_context(),
            {
                'image_url': product.image.url,
                'title': product.title,
                'cta_label': additional_product.cta_label,
                'cta_link': ("/products/%s/" %(product.slug))
            }
        )

class DynamicCampaignInfluencerTests(TestCase):
    def test_as_context_returns_the_required_keys(self):
        """
        Dynamic campaign influencer has the required entries
        when transformed to be used as context
        """
        influencer = DynamicCampaignInfluencerFactory()
        self.assertDictEqual(
            influencer.as_context(),
            {
                'image_url': influencer.image.url,
                'image_alt_text': influencer.image_alt_text,
                'blog_title': influencer.blog_title,
                'recipe_title': influencer.recipe_title,
                'button_label': influencer.button_label,
                'button_link': influencer.button_link
            }
        )
