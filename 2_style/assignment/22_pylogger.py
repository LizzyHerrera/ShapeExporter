# STYLE ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************

# original: logging.init.py

def find_caller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """

    current_frame = currentframe()
    # Note: Certain versions of IronPython, currentframe() returns None if
    # IronPython isn't run with -X:Frames.

    if current_frame:
        current_frame = current_frame.f_back

    while hasattr(current_frame, "f_code"):
        frame_code = current_frame.f_code
        file_name = os.path.normcase(frame_code.co_filename)

        if file_name == _srcfile:
            current_frame = current_frame.f_back
        else:
            return (frame_code.co_filename, current_frame.f_lineno, frame_code.co_name)

    return "(unknown file)", 0, "(unknown function)"

# How can we make this code better?
