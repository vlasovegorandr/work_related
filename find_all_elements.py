from pywinauto.findwindows import ElementAmbiguousError
import re


def find_all_elements(parent_element, **children_element_properties):
    '''children_element_properties: title_re, class_name_re, control_type, и т.д.'''
    try:
        element = parent_element.child_window(**children_element_properties)
        element.draw_outline()
        print('Должны были найти несколько элементов, а нашли один')
        return [element]
    except ElementAmbiguousError as e:
        ambiguous_error_description = str(e).split('{')[0]
        num_of_elements = int(re.search(r'\d+', ambiguous_error_description).group())
    all_elements = [parent_element.child_window(**children_element_properties, found_index=index) for index in range(num_of_elements)]
    return all_elements
