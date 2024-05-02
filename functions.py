# ********************************************************************
# Project Utility Functions Module
# A collection of utility functions to support various tasks within the project.
# ********************************************************************

import pymel.core as pm

import utils

def get_blendshape_nodes(meshes):
    """ Get the blendShape node connected to the given meshes.

        Args:
            meshes(list or str): The name or list of meshes.

        Returns:
            list: The blendShape nodes.
        """

    # Convert meshes argument into a list in case a str is given
    meshes = utils.convert_to_list(meshes)
    blendshape_nodes = []
    for mesh in meshes:
        mesh = pm.PyNode(mesh) if isinstance(mesh, str) else mesh
        blend_shape = [node for node in mesh.history(type='blendShape')]
        blendshape_nodes.append(blend_shape)

    return blendshape_nodes

def get_base_object(blendshape_node):
    """
        Returns:
            str: The name of the base object affected by the blendshape node.
        """
    base_object = blendshape_node.getBaseObjects()[0]
    return base_object.name()

def get_targets(blendshape_node, names_only=False):
    """ Get the blendShape node connected to the given meshes.

        Args:
            blendshape_node(str): Name
            names_only(bool):
        Returns:
            list or dictionary: A list of target names or a dictionary of target index(key) and names(value).
        """
    # Check if blendshape_node is a PyNode; if it is, convert it to a string."
    blendshape_node = blendshape_node.name() if isinstance(blendshape_node, pm.general.PyNode) else blendshape_node

    alias_attr = pm.aliasAttr(blendshape_node, query=True)
    targets = {}
    for i in range(1, len(alias_attr), 2):
        weight_ix = int(alias_attr[i].split('[')[1].split(']')[0])
        targets_name = alias_attr[i-1]
        targets[weight_ix] = targets_name

    return [targets[ix] for ix in targets] if names_only else targets

def export_blendshape_data():
    pass