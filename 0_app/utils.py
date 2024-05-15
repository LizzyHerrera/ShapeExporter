# ********************************************************************
# A collection of utility functions for use in Autodesk Maya.
# ********************************************************************

import maya.cmds as mc
import pymel.core as pm

def convert_to_list(input):
    """ Convert input into a list if str, if not, continue.

    Args:
        input(list or str): input to be converted

    Returns:
        list: input as list.
    """

    return list(input) if isinstance(input, str) else input

