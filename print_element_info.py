

def print_parents(control):
    print(control.get_properties())
    parent = control.parent()
    while parent:
        parent.draw_outline()
        print(parent.get_properties())
        parent = parent.parent()


def print_children(control, current_depth=0, max_depth=100):
    if current_depth < max_depth:
        children = control.children()
        colours = [111111, 22222, 3333333]
        current_colour = colours[current_depth % len(colours)]
        indent = current_depth*'   | '
        for child in children:
            child.draw_outline(colour=current_colour)
            properties = child.get_properties()
            try:
                del properties['rectangle']
            except KeyError:
                pass
            for prop, value in properties.items():
                print(indent, f'{prop}: {value}')
            print()
            print_children(child, current_depth=current_depth+1, max_depth=max_depth)
