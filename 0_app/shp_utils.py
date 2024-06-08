# ********************************************************************
# A collection of utility functions for use in Autodesk Maya.
# ********************************************************************
import os
import json

import maya.cmds as mc
import pymel.core as pm

EXPORT = {
            'name_space': '',
            'blendshape_name': '',
            'vertex_count': '',
            'deltas':
                {
                    'current_version': {},
                    'last_version': {}
                }
         }

def convert_to_list(input):
    """ Convert input into a list if str, if not, continue.

    Args:
        input(list or str): input to be converted

    Returns:
        list: input as list.
    """

    return list(input) if isinstance(input, str) else input


def export_json_file(data, name, path):
    out_data = {}
    for key in data:
        out_data[key] = list(data[key])
    with open(os.path.join(path, name), "w") as file:
        json.dump(out_data, file)

def import_json(file_name, path):
    with open(os.path.join(path, file_name), "r") as file:
        data = json.load(file)

    return data

# esto es un test