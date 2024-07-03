# ********************************************************************
# Project Utility Functions Module
# A collection of utility functions to support various tasks within the project.
# ********************************************************************
import copy
import os

import numpy as np

import maya.cmds as mc
import pymel.core as pm
import pymel.core.nodetypes as nt

import shp_utils

def get_blendshape_nodes(meshes):
    """ Get the blendShape node connected to the given meshes.

        Args:
            meshes(list or str): The name or list of meshes.

        Returns:
            list: The blendShape nodes.
    """

    # Convert into a list if str
    meshes = shp_utils.convert_to_list(meshes)
    blend_nodes = []
    for mesh in meshes:
        mesh = pm.PyNode(mesh) if isinstance(mesh, str) else mesh
        for node in mesh.history(type='blendShape'):
            blend_nodes.append(node)

    return blend_nodes

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
    vtx_coords = []
    if isinstance(mesh, nt.Mesh):
        vtx_coords = mesh.getPoints()
    elif isinstance(mesh, nt.Transform):
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
            zero_threshold (float): Value to consider a delta significant. Defaults to 0.001
            clean_data (bool) : True / False

        Returns:
            dict: A dictionary containing the deltas between common vertices of base and target meshes.

        """
    common_verts = set(target_verts.keys()) & set(base_verts.keys())
    deltas = {}
    for vtx in common_verts:
        vtx_pos_difference = []
        for target, base in zip(target_verts[vtx], base_verts[vtx]):
            vtx_pos_difference.append(target - base)
        # Map vertex IDs to deltas if any exceeds the threshold
        if any(abs(diff) > zero_threshold for diff in vtx_pos_difference):
            deltas[vtx] = vtx_pos_difference

    if not clean_data:
        return deltas

    clean_deltas = copy.copy(deltas)
    has_data = False

    for id, vector in clean_deltas.items():
        vector_magnitude = np.linalg.norm(np.array(vector))
        if vector_magnitude < zero_threshold:
            clean_deltas[id] = [0, 0, 0]
        else:
            has_data = True

    return clean_deltas if has_data else None


def check_delta_path(path, mesh, blendshape_node):
    """
        Check and create necessary directories for exporting deltas.

        Args:
            path: The base directory path.
            mesh: The mesh name.
            blendshape_node: The blendshape node name.

        Returns:
            The final export path.
    """

    # Construct the full path for saving deltas
    shapes_path = os.path.join(path, mesh, blendshape_node)

    if not os.path.exists(shapes_path):
        os.makedirs(shapes_path)

    return shapes_path


def export_delta_from_blendshape(blendshape_node, path, version):
    """
    Export delta data from a blendshape node.

    Args:
        blendshape_node: Pymel blendShape node
        path: The directory path.
        version: The version type ('latest_version' or 'previous_version').

    Returns:
        The export path and a list of exported target names.
    """
    blendshape_node = pm.PyNode(blendshape_node) if isinstance(blendshape_node, str) else blendshape_node
    base_mesh = get_base_object(blendshape_node)
    base_mesh_vtx = get_verts_id_coords(base_mesh)
    export_path = check_delta_path(path, base_mesh, blendshape_node.name())
    target_names = get_targets(blendshape_node, names_only=True)

    exported = []
    for target_name in target_names:
        # Activate the target blendshape
        mc.setAttr(blendshape_node.name() + '.' + target_name, 1)
        if mc.objExists(target_name):
            target_mesh = target_name
        else:
            target_mesh = base_mesh

        target_mesh_vtx = get_verts_id_coords(target_mesh)
        delta_data = get_deltas(base_mesh_vtx, target_mesh_vtx)
        mc.setAttr(blendshape_node.name() + '.' + target_name, 0)

        if delta_data:
            name = f"{target_name}_bShape.json"
            out_data = {key: list(delta_data[key]) for key in delta_data}

            file_path = os.path.join(export_path, name)
            export_data = shp_utils.load_EXPORT_data(file_path)

            export_data['mesh_name'] = base_mesh
            export_data['blendshape_name'] = blendshape_node.name()

            # Update the version data
            # TODO: Modify this part to handle multiple versioning and not only two.
            if version == 'latest_version':
                export_data['deltas']['previous_version'] = export_data['deltas']['latest_version']
                export_data['deltas']['latest_version'] = out_data
            else:  # This part is actually redundant because 'latest_version' is the only version used
                export_data['deltas']['latest_version'] = out_data

            shp_utils.save_data(export_data, file_path)

        exported.append(target_name)

        return export_path, exported


def export_deltas_from_meshes(meshes,path,version):
    blend_nodes = get_blendshape_nodes(meshes)
    if blend_nodes:
        for node in blend_nodes:
            export_delta_from_blendshape(node,path,version)

def apply_deltas(target,base_verts,deltas):
    """
    Applies deltas to target mesh.

    Args:
        target(str): Mesh you're applying deltas to.
        base_verts(list): input base verts
        deltas: input deltas from json file

    """
    transform = pm.nodetypes.Transform(target)
    shape = pm.nodetypes.Mesh(transform.getShape())
    for delta in deltas:
        shape.setPoint(int(delta), pm.datatypes.Point(base_verts[delta]) + pm.datatypes.Point(deltas[delta]))

def import_deltas(base_mesh, dirpath):
    #TODO: Finish the import function

    base_verts = get_verts_id_coords(base_mesh)
    imported = 0

    if os.path.isfile(dirpath):
        file_names = [dirpath]
    else:
        base_mesh_name = str(base_mesh)
        if not dirpath.endswith(base_mesh_name):
            dirpath = os.path.join(dirpath, base_mesh_name)
        file_names = [item for item in os.listdir(dirpath) if item.endswith('.json')]

    target_grp = 'targetGrp'
    if not mc.objExists(target_grp):
        mc.createNode('transform', n=target_grp)
        mc.setAttr(target_grp+'.v', 0)

    target_names = list()
    for ix, filename in enumerate(file_names):
        if '_bShape' in filename:
            target_name = filename.split('_bShape')[0]
        else:  # just looks for targetName
            target_name = filename.split('.')[0]
        target_names.append(target_name)
    pass

###################################################################################################################

# TESTING
'''if delta_data:
            name = f"{target_name}_bShape.json"
            out_data = {}
            for key in delta_data:
                out_data[key] = list(delta_data[key])

            export_data = deepcopy(shp_utils.EXPORT)  # Create a deep copy of the EXPORT dictionary
            export_data['mesh_name'] = base_mesh
            export_data['blendshape_name'] = blendshape_node.name()
            export_data['deltas'][version] = out_data

            with open(os.path.join(export_path, name), "w") as file:
                json.dump(export_data, file, indent=1)

        exported.append(target_name)

    return export_path, exported'''