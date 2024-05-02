# ********************************************************************
# A collection of utility functions for use in Autodesk Maya.
# ********************************************************************

import maya.cmds as mc
import pymel.core as pm

def convert_to_list(input):
    """ Convert input into a list if it's a string, otherwise leave it unchanged.

    Args:
        input (list or str): The input to be converted

    Returns:
        list: The list containing input if it was a string, or input itself if it was already a list.
    """

    return list(input) if isinstance(input, str) else input

