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
        try:
        	self.var = int(var)
        except ValueError:
        	self.var = -1

    def render(self, context):
        if context['order_by'] == 'reverse':
        	if self.var < 0:
        		self.var = context['total'] + 1
        	self.var = self.var - 1
        else:
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
