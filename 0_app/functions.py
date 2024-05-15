# ********************************************************************
# Project Utility Functions Module
# A collection of utility functions to support various tasks within the project.

# NOTE: Make sure to use python 3.8.0 or higher.
# ********************************************************************
import copy

import numpy as np

import pymel.core as pm
import maya.cmds as mc

import utils

def get_blendshape_nodes(meshes):
    """ Get the blendShape node connected to the given meshes.

        Args:
            meshes(list or str): The name or list of meshes.

        Returns:
            list: The blendShape nodes.
    """

    # Convert into a list if str
    meshes = utils.convert_to_list(meshes)
    blendshape_nodes = []
    for mesh in meshes:
        mesh = pm.PyNode(mesh) if isinstance(mesh, str) else mesh
        blend_shape = [node for node in mesh.history(type='blendShape')]
        blendshape_nodes.append(blend_shape)

    return blendshape_nodes

def get_base_object(blendshape_node):
    base_object = blendshape_node.getBaseObjects()[0]
    return base_object.name()

def get_targets(blendshape_node, names_only=False):
    """ Get the blendShape targets connected to the given blendShape node.

        Args:
            blendshape_node(str): Name
            names_only(bool):
        Returns:
            list or dictionary: List of target names or dictionary of target index(key) and name(value).
    """
    # Check if PyNode; if so, stringify it.
    if isinstance(blendshape_node, pm.general.PyNode):
        blendshape_node = blendshape_node.name()
    else:
        blendshape_node = blendshape_node

    alias_attr = pm.aliasAttr(blendshape_node, query=True)
    targets = {}
    for ix in range(1, len(alias_attr), 2):
        weight_ix = int(alias_attr[ix].split('[')[1].split(']')[0])
        targets_name = alias_attr[ix-1]
        targets[weight_ix] = targets_name

    tgt_names = [targets[ix] for ix in targets]

    return tgt_names if names_only else targets

def get_verts_id_coords(mesh):
    """Retrieves the coordinates of each vertex in the given mesh.

    Args:
        mesh (str or pm.general.PyNode): The mesh to retrieve vertex coordinates from.

    Returns:
        dict: A dictionary mapping vertex IDs to their corresponding coordinates.

    """
    mesh = mesh if isinstance(mesh, pm.general.PyNode) else pm.PyNode(mesh)
    # Get vertex coordinates
    vtx_coords = mesh.getShape().getPoints()

    # Map vertex IDs to coordinates
    verts = {}
    for id, vtx in enumerate(vtx_coords):
        verts[str(id)] = [vtx.x, vtx.y, vtx.z]

    return verts

def get_deltas(base_verts, target_verts, zero_threshold=0.001, clean_data=True):
    """
        Args:
            base_verts (dict): Base mesh vertices id(key) and coords(value).
            target_verts (dict): Target mesh vertices id(key) and coords(value).
            zero_threshold (float): Value to consider a delta significant. Defaults to 0.00001

        Returns:
            dict: A dictionary containing the deltas between common vertices of base and target meshes.

        """
    # Ensure only common vertices are used for zip operation later
    common_verts = set(target_verts.keys()) & set(base_verts.keys())
    deltas = {}
    for ix in common_verts:
        vtx_pos_difference = []
        for target, base in zip(target_verts[ix], base_verts[ix]):
            vtx_pos_difference.append(target - base)
        # Map vertex IDs to deltas if any exceeds the threshold
        if any(abs(diff) > zero_threshold for diff in vtx_pos_difference):
            deltas[ix] = vtx_pos_difference

    if clean_data:
        clean_deltas = copy.copy(deltas)
        data = False

        for id, vector in clean_deltas.items():
            vector_magnitude = np.linalg.norm(np.array(vector))
            if vector_magnitude < 0.001:
                clean_deltas[id] = [0, 0, 0]
            elif vector_magnitude > 0.001:
                data = True
        if not data:
            return None
        else:
            return clean_deltas
    else:
        return deltas


def check_delta_path(path):
    pass

def export_blendshape_data(blendshape_node, path):

    base_mesh = pm.PyNode(get_base_object(blendshape_node))
    export_path = check_delta_path(path)
    target_names = get_targets(blendshape_node, names_only=True)

    for tgt in target_names:
        mc.setAttr(blendshape_node.name() + '.' + tgt, 1)
        if mc.objExists(tgt):
            tgt_mesh = tgt
        else:
            tgt_mesh = base_mesh
