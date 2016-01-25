from django import template
import math
import dateutil.parser as date_parser

register = template.Library()

@register.filter(name='get')
def get(d, k):
    return d.get(k, None)

def flatten_dict(data, path=tuple()):
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    yield from flatten_dict(item, path + (key,))
        elif isinstance(value, dict):
            yield from flatten_dict(value, path + (key,))
        else:
            yield ": ".join(path + (key,)), value

@register.filter(name='flatten')
def flatten(d):
    return {key: value for key, value in flatten_dict(d) 
            if key not in ["id", "title", "description"]}

@register.filter(name='half_sorted_items')
def half_grant(grant, half):
    sorted_list = sorted(grant.items(), key=lambda a: a[0].lower()) 
    if half == 1:
        return sorted_list[:math.floor(len(grant)/2)]
    else:
        return sorted_list[math.floor(len(grant)/2):]

@register.filter(name='get_title')
def get_title(d):
    title = d.get('title')
    if title:
        return title
    else:
        return d.get('id')

@register.filter(name='get_name')
def get_name(d):
    name = d.get('name')
    if name: 
        return name
    else:
        return d.get('id')

@register.filter(name='get_currency')
def get_currency(d):
    currency = d.get('currency')
    if not currency:
        return ''
    if currency.lower() == 'gbp':
        return '£'
    else:
        return currency + ' '

@register.filter(name='get_amount')
def get_amount(amount):
    try:
       return "{:,.0f}".format(amount)
    except ValueError:
       return amount
    
@register.filter(name='get_date')
def get_date(date):
    try:
        return date_parser.parse(date, dayfirst=True).strftime("%d %b %Y")
    except ValueError:
        return date
