# contains additional usefull functions


# needed to access the .cleaned_data[..] of a form
# since empty fields would otherwise return none,
# which can't be processed by the Querys
def get_value(form, key):
    value = form.cleaned_data[key]
    if value is None:
        value = ''

    return value
