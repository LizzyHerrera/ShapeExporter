# ********************************************************************
# A collection of utility functions for use in Autodesk Maya.
# ********************************************************************
import os
import json
from copy import deepcopy

import pymel.core as pm

EXPORT = {
    'mesh_name': '',
    'blendshape_name': '',
    'deltas':
        {
            'latest_version': {},
            'previous_version': {}
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

def load_EXPORT_data(path):
    """
        Load existing data from a JSON with the EXPORT dictionary.
    """

    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return deepcopy(EXPORT)

def save_data(data, path):
    """
        Saves data to a json file.
    """
    with open(path, 'w') as file:
        json.dump(data, file, indent=1)

def get_scene_meshes(transforms=True):
    """
        Returns a list of all meshes in scene as pymel mesh nodes or transform nodes.

    """
    mesh_nodes = [mesh for mesh in pm.ls(type='mesh') if not mesh.endswith('Orig')]
    mesh_transforms = list(set([mesh.getParent() for mesh in mesh_nodes]))
    return mesh_transforms if transforms is True else mesh_nodes

def import_json(file_name, path):
    with open(os.path.join(path, file_name), "r") as file:
        data = json.load(file)

    return data
