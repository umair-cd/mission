from django import template

register = template.Library()

@register.filter(name='cut_last')
def cut_last(value):
    """
    This method will return a array with two items
    being the last item the last word of the text.
    i.e: 'The taco salad' = ['The taco', 'salad]
    """
    values = value.split(' ')
    if len(values) < 2:
        return ['', value]
    return [' '.join(values[:-1]), values[-1]]

@register.filter()
def is_selected(value, active_value):
    if value == active_value:
        return "selected"
    else:
        return ""

@register.filter()
def display_fraction(value):
    fraction_map = {
        "eigth": "⅛",
        "quarter": "¼",
        "third": "⅓",
        "half": "½",
        "two-thirds": "⅔",
        "three-quarters": "¾"
    }
    return fraction_map[value]

@register.filter
def return_item(indexed_item, key):
    try:
        return indexed_item[key]
    except:
        return None

@register.filter()
def in_percent(rating):
    return "{}%".format(round(rating/5 * 100))

@register.filter()
def get_recipe_metric_container_class(recipe):
    metric_count = recipe.get_metric_count

    container_class = "col-xs-6 col-sm-{cols}"

    cols = int(12/metric_count)

    return container_class.format(cols=cols)
