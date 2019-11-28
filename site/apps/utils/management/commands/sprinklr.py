from django.core.management.base import BaseCommand
from apps.utils.sprinklr import SprinklrService
from apps.web.models import Recipe


class Command(BaseCommand):
    help = 'Calls the sprinklr service'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recipe_ratings',
            action='store',
            dest='recipe_ratings',
            default='',
            help='Update recipe ratings.'
        )

    def handle(self, *args, **options):
        sprinklr = SprinklrService()
        if options['recipe_ratings']:
            product_id = options['recipe_ratings']
            recipe = Recipe.objects.get(slug=product_id)
            if recipe:
                self.get_recipe_average(recipe, sprinklr)
        else:
            recipes = Recipe.objects.all()
            for recipe in recipes:
                self.get_recipe_average(recipe, sprinklr)


    def get_recipe_average(self, recipe, sprinklr):
        average_rating = sprinklr.recipe_ratings(recipe_id=recipe.slug)
        if average_rating:
            recipe.average_rating = average_rating
            recipe.save()
        self.stdout.write('Finished updating recipe `{0}` review.'.format(recipe.slug))
