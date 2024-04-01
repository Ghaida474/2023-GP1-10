from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''

@register.filter
def split(value, key):
    """
    Returns the value turned into a list.
    """
    return value.split(key)


@register.filter(name='get_dict_item')
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_list_item')
def get_list_item(list_, index):
    try:
        return list_[index]
    except (IndexError, TypeError):
        return None

 
@register.inclusion_tag('recurse_tree.html')
def recurse_tree(tasks, level=0):
    return {'tasks': tasks, 'level': level}

@register.filter
def append_to_list(list_, item):
    list_.append(item)
    return ''