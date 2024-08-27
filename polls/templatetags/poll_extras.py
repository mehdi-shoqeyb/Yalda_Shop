from django import template
# from jalali_date import date2jalali

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

@register.filter(name='three_digits_currency')
def three_digits_currency(price):
    price = str(price)
    formatted_price = ""
    while price:
        formatted_price = price[-3:] + "," + formatted_price
        price = price[:-3]
    formatted_price = formatted_price[:-1]  # Remove the extra "/" at the end
    return formatted_price

@register.simple_tag
def multiply(quantity,price,*args,**kwargs):
    return three_digits_currency(price * quantity)


# Define the color mapping dictionary
PERSIAN_TO_ENGLISH = {
    'مشکی': 'black',
    'سفید': 'white',
    'قرمز': 'red',
    'آبی': 'blue',
    'سبز': 'green',
    'زرد':'yellow',
    'صورتی':'pink',
    # Add more colors as needed
}

@register.filter(name='color_to_english')
def color_to_english(color_name):
    """Return the hex code for a given Persian color name."""
    return PERSIAN_TO_ENGLISH.get(color_name,'')
  
@register.filter(name='convert_float_to_fraction')
def convert_rating_to_fraction(rating):
    if rating is None:
        return "0"
    
    rating = str(rating)
    if len(rating) == 3:
        first_digit = rating[0]
        secound_digit = rating[2]
        if int(secound_digit) == 0:
            rounded_rating=f'{first_digit}'
        elif int(secound_digit) > 3 and int(secound_digit) < 7 :
            rounded_rating=f'{first_digit}/5'
        elif int(secound_digit) >= 7 :
            first_digit = int(first_digit) + 1
            rounded_rating=f'{first_digit}'
        elif int(secound_digit) <= 3 :
            rounded_rating=f'{first_digit}'
            
    else:
        rounded_rating = round(rating)
    
    return f"{rounded_rating}"

@register.filter(name='first_two_digits')
def first_two_digits(max_price):
    max_price = str(max_price)
    if len(max_price) > 7:
        return max_price[:2]
    else:
        return max_price[:1]