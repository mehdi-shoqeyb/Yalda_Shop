import json
def group_list(custom_list,size=4):
    grouped_list = []
    for i in range(0,len(custom_list),size):
        grouped_list.append(custom_list[i:i +size])
    return grouped_list

def extract_values_to_string(json_string):
    """
    Extracts the 'value' fields from a JSON string containing a list of dictionaries
    and returns them as a comma-separated string.
    
    Args:
        json_string (str): A JSON string representing a list of dictionaries.
    
    Returns:
        str: A comma-separated string of values.
    """
    try:
        # Parse the JSON string into a list of dictionaries
        dict_list = json.loads(json_string)
        
        # Extract 'value' fields from the list of dictionaries
        values = [d['value'] for d in dict_list]
        
        # Join the values into a comma-separated string
        return ', '.join(values)
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        # Handle possible errors (e.g., invalid JSON format, missing 'value' key)
        print(f"Error extracting values: {e}")
        return ""
    
def comment_rates(comments):
    rates = {
        '1_star': 0,
        '2_star': 0,
        '3_star': 0,
        '4_star': 0,
        '5_star': 0
        }
    
    for comment in comments:
        key = f'{comment.rate}_star'
        if key in rates:
            rates[key] += 1
    
    return rates

def comment_rates_percentages(rates):
    total_ratings = sum(rates.values())

    # Calculate and round percentages to the nearest integer
    percentages = {
        key: round((value / total_ratings * 100) if total_ratings > 0 else 0)
        for key, value in rates.items()
    }
    
    return percentages
