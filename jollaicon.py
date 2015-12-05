"""
NAME
    jollaicon -- easy way to shape your ``png`` icon to sailfish style

SYNOPSIS
    jollaicon [options] <input> <output>

DESCRIPTION
    -1, --top-left        make top left rectangle instead of round
    -2, --top-right       make top right rectangle instead of round
    -3, --bottom-right    make bottom right rectangle instead of round
    -4, --bottom-left     make bottom left rectangle instead of round
    -h, --help            print this screen
    -v, --version         print version of this script
    -f, --fill[=<color>]  fill color for transparent part. No effect when your
                          icon file is full-filled with color already. It
                          should in ``(r, g, b)`` or ``(r, g, b, alpha)``
                          number group. use white when this option appears but
                          no color specified.

    <input>               path to your icon file (png format only)
    <output>              output file (png format)

    This program can easily shape your ``png`` icon file into sailfish OS style

    Note: if you need to write <input>/<output> after -f option without color
    specified, use ``--`` (double dashes) to separate:

    jollaicon --fill -- myicon.png converted.png       # need ``--``
    jollaicon --fill=(0,0,0) myicon.png converted.png  # no need ``--``
    jollaicon --fill -i myicon.png converted.png       # no need ``--``

AUTHOR
    TylerTemp <tylertempdev@gmail.com>

    BUG reports are welcome:
    https://github.com/TylerTemp/jollaicon/issues
"""
import cairocffi as cairo
import math

__version__ = '0.0.1'

def make_mask(context,
              top_left=False, top_right=False,
              bottom_left=False, bottom_right=False):

    surface = context.get_target()
    width = min(surface.get_height(), surface.get_width())

    start_x = width / 2
    center_x = start_x
    center_y = start_x
    radius = start_x
    pi = math.pi

    if top_left:
        context.line_to(0, 0)
        context.line_to(center_x, 0)
    else:
        context.arc(center_x, center_y, radius, 1 * pi, 1.5 * pi)

    if top_right:
        context.line_to(width, 0)
        context.line_to(width, center_y)
    else:
        context.arc(center_x, center_y, radius, -0.5 * pi, 0)

    if bottom_right:
        context.line_to(width, width)
        context.line_to(center_x, width)
    else:
        context.arc(center_x, center_y, radius, 0, 0.5 * pi)

    if bottom_left:
        context.line_to(0, width)
        context.line_to(0, center_y)
    else:
        context.arc(center_x, center_y, radius, 0.5 * pi, 1 * pi)


def icon(icon_file, out_file,
         top_left=False, top_right=False, bottom_right=False, bottom_left=False,
         bg=(0, 0, 0, 0)):
    """shape ``icon_file`` and save it into ``out_file``

    icon_file: file name or file-like object of your icon file (png only)
    out_file: file name or file-like object to save the shaped file (png)
    top_left/top_right/bottom_right/bottom_left: for the 4 corner of your icon
        file, set to True to make it rectangle instead of round(default)
    bg: for some android icon, the corners are usually a bit round. For after
        shaping, these corner will contain transparent pixels (depending on the
        shape you set). this argument will fill color at these pixels.
        format: (r, g, b[, alpha])
    """
    source = cairo.ImageSurface.create_from_png(icon_file)
    width = min(source.get_height(), source.get_width())
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, width)
    mask = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, width)
    background = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, width)

    context = cairo.Context(surface)

    # paint source
    context.set_source_surface(source)
    context.paint()

    # make mask
    mask_context = cairo.Context(mask)
    make_mask(mask_context, top_left=top_left, top_right=top_right,
              bottom_left=bottom_left, bottom_right=bottom_right)
    mask_context.fill()

    # paint mask
    context.set_operator(cairo.OPERATOR_DEST_IN)
    context.set_source_surface(mask)
    context.paint()

    # make background
    bg_context = cairo.Context(background)
    # - fill transparent
    bg_context.set_source_rgba(0, 0, 0, 0)
    bg_context.rectangle(0, 0, width, width)
    bg_context.fill()
    # - fill color
    bg_context.set_source_rgba(*bg)
    make_mask(bg_context, top_left=top_left, top_right=top_right,
              bottom_left=bottom_left, bottom_right=bottom_right)
    bg_context.fill()

    # paint source
    bg_context.set_source_surface(surface)
    bg_context.paint()

    # save file
    background.write_to_png(out_file)


main = icon


if __name__ == '__main__':
    import sys
    from docpie import Docpie

    class Pie(Docpie):
        usage_name = 'SYNOPSIS'
        option_name = 'DESCRIPTION'

    args = dict(Pie(__doc__, version=__version__, appearedonly=True).docpie())
    main_args = {}
    main_args['top_left'] = args.get('--top-left', False)
    main_args['top_right'] = args.get('--top-right', False)
    main_args['bottom_right'] = args.get('--bottom-right', False)
    main_args['bottom_left'] = args.get('--bottom-left', False)
    if '--fill' in args:
        if args['--fill']:
            color = args['--fill']
            if color.startswith('('):
                color = color[1:-1]
            bg = [int(x) for x in color.split(',')]
        else:
            bg = (255, 255, 255)
        main_args['bg'] = bg

    in_file = args['<input>']
    if in_file == '-':
        in_file = sys.stdin
    out_file = args['<output>']
    if out_file == '-':
        out_file = sys.stdout

    main_args['icon_file'] = in_file
    main_args['out_file'] = out_file

    icon(**main_args)