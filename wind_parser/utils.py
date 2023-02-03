def remove_empty_strings(lst):
    """
    Remove empty strings in a list that can contains sublists and remove the sublists if they are empty
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.append(remove_empty_strings(item))
        elif item != "":
            result.append(item)
    return result
