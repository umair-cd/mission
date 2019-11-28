from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_sprinklr_date(value):
    """Gets Sprinklr date and returns a python date"""
    date_obj = datetime.strptime(value.split('T')[0], '%Y-%m-%d')
    return date_obj.strftime('%Y / %m / %d')


@register.filter
def rate_to_stars(number):
    full_star = '<i class="fa fa-star"></i>'
    empty_star = '<i class="fa fa-star empty"></i>'

    stars_html = [full_star for _ in range(number)]
    stars_html += [empty_star for _ in range(5-number)]
    return "".join(stars_html)