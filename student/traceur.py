"""Decorator to debug python programs.

Decorate any function with @trace to display arguments
and results in terminology or to generate an image at
each call. You can also use "display_instance"
and "display_vars" directly in your code to
draw the variables and instances of your choice.
"""
from tempfile import NamedTemporaryFile
import os
import time
import collections
import typing
import inspect
import shutil

VARIABLE_BACKGROUND = "chartreuse"
OBJECT_BACKGROUND = "gray"
NONE_BACKGROUND = "deeppink"
Variable = collections.namedtuple("Variable", "name value")

def _draw_none(obj, dot_file):
    """Draw the None node"""
    dot_name = f'struct_{id(obj)}'
    print(f'  {dot_name} [label=<', file=dot_file)
    print(f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{NONE_BACKGROUND}">',
          file=dot_file)
    print(f'<TR><TD>None</TD></TR>', file=dot_file)
    print('</TABLE>>];', file=dot_file)
    return dot_name

def _draw_callable(obj, dot_file):
    """Draw the given callable"""
    dot_name = f'struct_{id(obj)}'
    print(f'  {dot_name} [label=<', file=dot_file)
    print(f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{OBJECT_BACKGROUND}">',
          file=dot_file)
    print(f'<TR><TD><u>{type(obj).__name__}</u></TD></TR>', file=dot_file)
    obj_str = f'{obj.__name__}'
    print(f'<TR><TD>{obj_str}</TD></TR>', file=dot_file)
    print('</TABLE>>];', file=dot_file)
    return dot_name

def _is_primitive(obj):
    """Is the given object primitive"""
    return isinstance(obj, (int, float, str)) or obj is None

def _draw_primitive(obj, dot_file):
    """Draw a primitive object"""
    dot_name = f'struct_{id(obj)}'
    print(f'  {dot_name} [label=<', file=dot_file)
    print(f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{OBJECT_BACKGROUND}">',
          file=dot_file)
    print(f'<TR><TD><u>{type(obj).__name__}</u></TD></TR>', file=dot_file)
    obj_str = f'"{obj}"' if isinstance(obj, str) else f'{obj}'
    print(f'<TR><TD>{obj_str}</TD></TR>', file=dot_file)
    print('</TABLE>>];', file=dot_file)
    return dot_name

def _draw_sequence(obj, dot_file, deeply, seen_objs):
    """Draw a list or tuple object"""
    dot_name = f'struct_{id(obj)}'
    seen_objs[id(obj)] = dot_name
    print(f'  {dot_name} [label=<', file=dot_file)
    print(f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{OBJECT_BACKGROUND}">',
          file=dot_file)

    # Si la séquence n'est pas vide
    if obj:
        print(f'<TR><TD COLSPAN="{len(obj)}"><u>{type(obj).__name__}</u></TD></TR>', file=dot_file)
        print(f'<TR>', end='', file=dot_file)
        child_to_be_drawn = []
        child_count = 0
        for elem in obj:
            if not deeply and _is_primitive(elem):
                elem_str = f'"{elem}"' if isinstance(elem, str) else f'{elem}'
                print(f'<TD>{elem_str}</TD>', end='', file=dot_file)
            else:
                print(f'<TD PORT="port_child{child_count}">⏺</TD>', end='', file=dot_file)
                child_to_be_drawn.append(elem)
                child_count += 1
        print(f'</TR>', file=dot_file)
        print('</TABLE>>];', file=dot_file)
        for i, child in enumerate(child_to_be_drawn):
            sub_dot_name = _draw_object(deeply=deeply, obj=child,
                                        dot_file=dot_file, seen_objs=seen_objs)
            print(f'{dot_name}:port_child{i} -> {sub_dot_name};', file=dot_file)

    # Sinon elle est vide
    else:
        print(f'<TR><TD><u>{type(obj).__name__}</u></TD></TR>', file=dot_file)
        print(f'<TR>', end='', file=dot_file)
        print(f'<TD>vide</TD>', end='', file=dot_file)
        print(f'</TR>', file=dot_file)
        print('</TABLE>>];', file=dot_file)

    return dot_name

def _draw_dict(obj, dot_file, deeply, seen_objs):
    """Draw a dict object"""
    dot_name = f'struct_{id(obj)}'
    seen_objs[id(obj)] = dot_name
    print(f'  {dot_name} [label=<', file=dot_file)
    print(f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{OBJECT_BACKGROUND}">',
          file=dot_file)
    print(f'<TR><TD COLSPAN="{len(obj)*2}"><u>{type(obj).__name__}</u></TD></TR>',
          file=dot_file)
    child_to_be_drawn = []
    child_count = 0
    print(f'<TR>', file=dot_file)
    for i in range(1, len(obj) + 1):
        print(f'<TD COLSPAN="2">item{i}</TD>', file=dot_file)
    print(f'</TR>', file=dot_file)
    print(f'<TR>', end='', file=dot_file)
    for key, value in obj.items():
        for elem, elem_name in ((key, "key"), (value, "value")):
            if not deeply and isinstance(elem, (int, float, str)):
                elem_str = f'"{elem}"' if isinstance(elem, str) else f'{elem}'
                print(f'<TD>{elem_name} {elem_str}</TD>',
                      end='', file=dot_file)
            else:
                print(f'<TD PORT="port_child{child_count}">{elem_name} ⏺</TD>',
                      end='', file=dot_file)
                child_to_be_drawn.append(elem)
                child_count += 1
    print(f'</TR>', file=dot_file)
    print('</TABLE>>];', file=dot_file)
    for i, child in enumerate(child_to_be_drawn):
        sub_dot_name = _draw_object(deeply=deeply, obj=child,
                                    dot_file=dot_file, seen_objs=seen_objs)
        print(f'{dot_name}:port_child{i} -> {sub_dot_name};', file=dot_file)
    return dot_name

def _draw_other(obj, dot_file, deeply, seen_objs):
    """Draw an object using its attributes"""
    dot_name = f'struct_{id(obj)}'
    seen_objs[id(obj)] = dot_name
    print(f'  {dot_name} [label=<', file=dot_file)
    print(f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{OBJECT_BACKGROUND}">',
          file=dot_file)
    print(f'<TR><TD COLSPAN="{len(vars(obj))}"><u>{type(obj).__name__}</u></TD></TR>',
          file=dot_file)
    child_to_be_drawn = []
    child_count = 0
    print(f'<TR>', file=dot_file)
    for field_name in vars(obj):
        print(f'<TD>{field_name}</TD>', file=dot_file)
    print(f'</TR>', file=dot_file)
    print(f'<TR>', end='', file=dot_file)
    for field_name in vars(obj):
        field_obj = getattr(obj, field_name)
        if not deeply and _is_primitive(field_obj):
            elem_str = f'"{field_obj}"' if isinstance(field_obj, str) else f'{field_obj}'
            print(f'<TD>{elem_str}</TD>', end='', file=dot_file)
        else:
            print(f'<TD PORT="port_child{child_count}">⏺</TD>', end='', file=dot_file)
            child_to_be_drawn.append(field_obj)
            child_count += 1

    print(f'</TR>', file=dot_file)
    print('</TABLE>>];', file=dot_file)
    for i, child in enumerate(child_to_be_drawn):
        sub_dot_name = _draw_object(deeply=deeply, obj=child,
                                    dot_file=dot_file, seen_objs=seen_objs)
        print(f'{dot_name}:port_child{i} -> {sub_dot_name};', file=dot_file)
    return dot_name

def _draw_object(deeply: bool, obj: object, dot_file: typing.TextIO, seen_objs: dict):
    """Draw the given object in the dot file.

    And all other objects accessible from it.
    Return the dot name of the object.
    """

    # Return if obj already seen
    if id(obj) in seen_objs:
        return seen_objs[id(obj)]

    # None is sooooo special
    if obj is None:
        dot_name = _draw_none(obj, dot_file)
        seen_objs[id(obj)] = dot_name

    # For primitive type, just draw them and return
    elif _is_primitive(obj):
        dot_name = _draw_primitive(obj, dot_file)
        seen_objs[id(obj)] = dot_name

    # Handles list and tuples in the same way.
    # Drawing here depends on deeply
    elif isinstance(obj, (list, tuple)):
        dot_name = _draw_sequence(obj, dot_file, deeply, seen_objs)

    # Drawing of dict depends on deeply
    elif isinstance(obj, dict):
        dot_name = _draw_dict(obj, dot_file, deeply, seen_objs)

    # Drawing of a callable (such as a function)
    elif callable(obj):
        dot_name = _draw_callable(obj, dot_file)
        seen_objs[id(obj)] = dot_name

    # Drawing of dict depends on deeply
    elif isinstance(obj, dict):
        dot_name = _draw_dict(obj, dot_file, deeply, seen_objs)

    # Drawing of any other object
    else:
        dot_name = _draw_other(obj, dot_file, deeply, seen_objs)

    return dot_name

def _draw_arg(deeply: bool, variable: Variable, dot_file: typing.TextIO,
              seen_objs: dict):
    """Draw the given variable in the dot file.

    And all other objects accessible from it.
    """

    # Draw the variable itself
    print(f'  struct_{variable.name} [label=<', file=dot_file)
    print(f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{VARIABLE_BACKGROUND}">',
          file=dot_file)
    print(f'<TR><TD>{variable.name}</TD></TR>', file=dot_file)
    print(f'<TR><TD PORT="port_{variable.name}">⏺</TD></TR>', file=dot_file)
    print('</TABLE>>];', file=dot_file)

    # Draw the object referenced by variable and all accessible objetcs
    # from it. And the link between variable and object.
    obj_dot_name = _draw_object(deeply=deeply, obj=variable.value,
                                dot_file=dot_file, seen_objs=seen_objs)
    print(f'struct_{variable.name}:port_{variable.name} -> {obj_dot_name};', file=dot_file)

def display_vars(*args: typing.Sequence[Variable],
                 deeply: bool = True,
                 visualize: bool = True,
                 image_name: str = None):
    """Display graph of objects starting from given variables.

    Drawing is done by generating an SVG image with graphviz/dot.

    :param typing.Sequence[Variable] args: The sequence of variables
           to start the drawing from
    :param bool deeply: If True, str, int and float instances are drawn
           as in the reality, that is as instances. Else, they are
           embeded in the enclosing object if such object exists.
    :param bool visualize: If True, the generated image is opened in
           the terminal. For that, the program MUST run inside termi-
           nology. Else, the SVG file is copied into the current
           directory and its name is printed on stdout.
    :param str image_name: If visualize is False, this parameter
           allows specifying the name of the generated SVG image.
    """

    # Create the dot file as a temporary file (thanks to Python standard lib!)
    dot_f = NamedTemporaryFile(mode="w", delete=False, suffix=".dot")
    print('digraph structs {', file=dot_f)
    print('  node [shape=plaintext]', file=dot_f)

    # Draw variables one by one
    seen = {}
    for arg in args:
        _draw_arg(deeply=deeply, variable=arg, dot_file=dot_f, seen_objs=seen)

    # Convert to image and open it using tycat
    print("}", file=dot_f)
    dot_f.close()
    dot_name = dot_f.name
    #print(dot_name)
    img_name = dot_name + ".svg"
    os.system("dot -Tsvg {} -o {}".format(dot_name, img_name))

    # Open image using tycat
    if visualize:
        os.system("tycat {}".format(img_name))
        time.sleep(1)

    # Or copy the image to the current directory
    else:
        if image_name:
            target_file = f"./{image_name}.svg"
        else:
            target_file = f"./{os.path.basename(img_name)}"
        print(f"image generated as {target_file}")
        shutil.copyfile(img_name, target_file)

def display_instance(obj: object,
                     deeply: bool = True,
                     visualize: bool = True,
                     image_name: str = None):
    """Display graph of objects starting from the given object.

    Drawing is done by generating an SVG image with graphviz/dot.

    :param object obj: The object to start the drawing from
    :param bool deeply: If True, str, int and float instances are drawn
           as in the reality, that is as instances. Else, they are
           embeded in the enclosing object if such object exists.
    :param bool visualize: If True, the generated image is opened in
           the terminal. For that, the program MUST run inside termi-
           nology. Else, the SVG file is copied into the current
           directory and its name is printed on stdout.
    :param str image_name: If visualize is False, this parameter
           allows specifying the name of the generated SVG image.
    """

    # Create the dot file as a temporary file (thanks to Python standard lib!)
    dot_f = NamedTemporaryFile(mode="w", delete=False, suffix=".dot")
    print('digraph structs {', file=dot_f)
    print('  node [shape=plaintext]', file=dot_f)

    # Draw the object
    _draw_object(deeply=deeply, obj=obj, dot_file=dot_f, seen_objs={})

    # Convert to image
    print("}", file=dot_f)
    dot_f.close()
    dot_name = dot_f.name
    img_name = dot_name + ".svg"
    os.system("dot -Tsvg {} -o {}".format(dot_name, img_name))

    # Open image using tycat
    if visualize:
        os.system("tycat {}".format(img_name))
        time.sleep(1)

    # Or copy the image to the current directory
    else:
        if image_name:
            target_file = f"./{image_name}.svg"
        else:
            target_file = f"./{os.path.basename(img_name)}"
        print(f"image generated as {target_file}")
        shutil.copyfile(img_name, target_file)

def trace(deeply: bool = True,
          visualize: bool = True,
          image_name: str = None):
    """Decorator with a parameter to trace a function deeply or not.

    trace is called on the first time the definition of a function decorated
    with @traceur.trace(X) is encountered for a given X
    """
    def parametrized_tracer(function):
        """Activate terminal display (tycat) of function arguments and results.

        For a given X, parametrized_tracer is called every time the definition of
        a function decorated with @traceur.trace(X) is encountered
        """
        print(f"I was here {function}")
        def tracer(*args, **kwargs):
            """Trace and call original function.

            For a given X, tracer is called every time a function decorated with
            @traceur.trace(X) is called.
            """

            # Affiche l'appel à la fonction en texte sur stdout
            print("-----------------------------------")

            arguments = []

            # positional arguments
            posargs = inspect.getfullargspec(function).args
            for arg_name, arg_val in zip(posargs, args):
                arguments.append(Variable(arg_name, arg_val))
            posargs_str = ", ".join([str(arg.name) + "=" + str(arg.value) for arg in arguments])

            # varargs tuple
            first_vararg_index = len(posargs)
            if args[first_vararg_index:]:
                arguments.append(Variable(inspect.getfullargspec(function).varargs,
                                          args[first_vararg_index:]))
            varargs_str = "args=" + str(args[first_vararg_index:])

            # kwargs
            if kwargs:
                arguments.append(Variable("kwargs", kwargs))
            kwargs_str = "kwargs=" + str(kwargs)

            allargs_str = ", ".join(filter(None, [posargs_str, varargs_str, kwargs_str]))
            print("appel de fonction : " + function.__name__ + "(" + allargs_str + ")")

            # Affiche l'appel à la fonction en dot sur stdout avec tycat
            display_vars(*arguments, deeply=deeply, visualize=visualize, image_name=image_name)

            # Appel la fonction
            result = function(*args, **kwargs)

            # Affiche le résultat en texte sur stdout
            print("valeur de retour ----> " + str(result))

            # Affiche le résultat en dot sur stdout avec tycat
            display_instance(result, deeply=deeply, visualize=visualize, image_name=image_name)

            return result
        return tracer
    return parametrized_tracer
