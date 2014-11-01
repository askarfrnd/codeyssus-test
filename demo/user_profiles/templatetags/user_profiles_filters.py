from django import template

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})


def htmlattributes(value, arg):
    attrs = value.field.widget.attrs


    # data = arg.replace(' ', '')

    kvs = arg.split(',')

    for string in kvs:
        print "string is ",string
        kv = string.split(':')
        attrs[kv[0]] = kv[1]

    rendered = str(value)

    return rendered

register.filter('htmlattributes', htmlattributes)
