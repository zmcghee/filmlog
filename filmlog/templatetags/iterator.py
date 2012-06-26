from django import template
from django.template.base import Node

register = template.Library()

@register.filter
def zeroes(value, arg):
	"""Adds leading zeroes to any integer
	e.g. 15|zeroes:5 renders as 00015"""
	return u'%0*d' % (int(arg), int(value))

class IteratorNode(Node):
    def __init__(self, var):
        self.var = int(var)

    def render(self, context):
        self.var = self.var + 1
        return u'%s' % self.var

@register.tag
def iterator(parser, token):
    """Creates an iterator with a base of your choice.
    Use in a for loop, like so:
    
    	{% for entry in entry_list %}
    	{% if somecondition %}
    	{% iterator 0 %}
    	{% else %}
    	Condition not met
    	{% endif %}
    	{% endfor %}
    
    ... could render:
    
    	1
    	2
    	Condition not met
    	3
    	Condition not met
    	4
    	5
    	6
    	Condition not met
    
    """
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise TemplateSyntaxError("'firstof' statement requires at least one argument")
    return IteratorNode(bits[0])
