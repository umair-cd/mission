from django.core.management.base import BaseCommand
from apps.utils.sprinklr import SprinklrService
from apps.web.models import Recipe


class Command(BaseCommand):
    help = 'Adds recipes to Sprinklr'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pk',
            action='store',
            dest='pk',
            default='',
            help='Update recipe ratings.'
        )

    def handle(self, *args, **options):
        sprinklr = SprinklrService()
        if options['pk']:
            product_id = options['pk']
            recipe = Recipe.objects.get(pk=product_id)
            if recipe:
                self.add_recipe(recipe, sprinklr)
        else:
            recipes = Recipe.objects.all()
            for recipe in recipes:
                self.add_recipe(recipe, sprinklr)


    def add_recipe(self, recipe, sprinklr):
        payload = {
            "id": recipe.slug,
            "name": recipe.title,
            "url": "http://www.missionfoods.com/recipes/{0}/".format(recipe.slug),
            "description": recipe.description
        }
        sprinklr.create_recipe(payload)
        self.stdout.write('Finished adding recipe `{0}` to Sprinklr.'.format(recipe.title))
