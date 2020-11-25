from django import template

from discussion.models import Theme


register = template.Library()

@register.filter
def themes_queryset_to_dict(themes):

    themes_dict = {}
    for theme in themes:
        themes_dict.update({str(theme.pk): {'author': theme.author.username}})

    return themes_dict
