from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import re
import math


def unit_converter(request):
    unit_string = request.GET.get('units', "")

    if not unit_string:
        return JsonResponse({'success': 'false', 'error':'no input detected'})

    # conversion tables
    unit_conversion_table = {
        'minute': 's',
        'min': 's',
        'hour': 's',
        'h':'s',
        'day': 's',
        'd': 's',
        'degree': 'rad',
        '°': 'rad',
        '\'': 'rad',
        'second': 'rad',
        '\"': 'rad',
        'hectare': "(m**2)",
        'ha': "(m**2)",
        'litre': "(m**3)",
        'L': "(m**3)",
        'tonne':"kg",
        'ton':"kg",
        't':"kg",
    }
    num_conversion_table = {
        'minute': '60.0',
        'min':' 60.0',
        'hour': '3600.0',
        'h':'3600.0',
        'day': '86400.0',
        'd': '86400.0',
        'degree': str(math.pi/180.0),
        '°': str(math.pi/180.0),
        '\'': str(math.pi/10800.0),
        'second': str(math.pi/648000.0),
        '"': str(math.pi/648000.0),
        'hectare': '10000.0',
        'ha': '10000.0',
        'litre': '0.001',
        'L': '0.001',
        'tonne': '1000.0',
        'ton': '1000.0',
        't': '1000.0',
    }

    #allowed math operators
    math_whitelist = ['*', '/', '(', ")"]

    #invalid math operators made up of valid ones
    math_blacklist = ['**', '//']

    #arbitrary value to limit input string
    max_input_length = 100

    # check for long input
    if len(unit_string) > max_input_length:
        return JsonResponse({
        'success': 'false',
        'error': 'input exceeds maximum input characters:' + str(max_input_length),
        })

    #elminatewhitespace <-- get it?
    unit_string = ''.join(unit_string.split()).lower()

    #split string into words and math operators
    string_elements = [word for word in re.split('(\*|/|\(|\))', unit_string) if word]
    unit_name = ""
    math_expression = ""

    # check string elements for valid input, SI conversion if valid input found
    for el in string_elements:
        if el in unit_conversion_table.keys():
            unit_name += unit_conversion_table[el]
            math_expression += num_conversion_table[el]
        elif el in math_whitelist:
            unit_name += el
            math_expression += el
        else:
            return JsonResponse({'success': 'false', 'error': 'invalid syntax'})

    # check for exponents or double division, white list filtering misses these
    for el in math_blacklist:
        if el in unit_string:
            return JsonResponse({'success': 'false', 'error': 'invalid math expression'})

    # evaluate the math_expression to calculate multiplication_factor.
    try:
        # using eval here is relatively safe at this point as the expression can now
        # only consist of valid inputs or math_whitelist symbols.
        multiplication_factor = round(eval(math_expression), 14)
    except:
        return JsonResponse({'success': 'false', 'error': 'invalid math expression'})

    return JsonResponse({'unit_name': unit_name, 'multiplication_factor': multiplication_factor})
