from django import template
from idna import unicode

register = template.Library()
import re
from django.utils.safestring import mark_safe

# @register.filter(name='add_class')
# def add_class(field, css):
#     return field.as_widget(attrs={"class":css})
#
#
# @register.filter(name='form')
# def create_custom_form(form):
#     for field in form:
#         print(field.html_name)


class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')


@register.filter
def add_class(value, css_class):
    string = unicode(value)
    match = class_re.search(string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
                                                    css_class, css_class), match.group(1))
        print(match.group(1))
        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class,
                                          string))
    else:
        return mark_safe(string.replace('>', ' class="%s">' % css_class))
    return value
