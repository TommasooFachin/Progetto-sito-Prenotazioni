from django import template
register = template.Library()

@register.filter
def dict_get(d, k):    #utilizzato nei template per ottenere un 
                        #valore da un dizionario
    return d.get(k, None)