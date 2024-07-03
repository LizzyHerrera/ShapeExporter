
# Shape Exporter Tool for Autodesk Maya
![shapeExporter](https://github.com/LizzyHerrera/ShapeExporter/assets/109104254/1caed251-c079-400a-a3dd-20c91d651067)

## Description

ShapeExporter is a tool designed to assist 3D modelers?riggers in Maya by simplifying the process of exporting blendshapes as deltas and managing versions of deltas. This tool is part of a development project for the Python Advanced course taught by Alexander Richter.

## Features
### Blendshape Exporter
- Export from Selected: Export deltas from selected blendshapes.
- Export from All: Export deltas from all blendshapes.
- New Version: Save deltas as a new version.
- Overwrite Latest: Overwrite the latest version of deltas.
### Import Blendshapes
- Import Selected: Import deltas into selected blendshapes.
- Import All: Import deltas into all blendshapes.
- Latest Version: Import the latest version of deltas.
- Previous Version: Import the previous version of deltas.

## UI Overview
The UI is designed to be intuitive and user-friendly, with the following structure:

- Tree View: Displays the blendshapes in a hierarchical structure:

---Mesh Name

------Blendshape Name 

----------Target Name

![shapeExporter2](https://github.com/LizzyHerrera/ShapeExporter/assets/109104254/6918793b-6fd4-43f7-ab2b-c9a62359d258)

- Export Options: 1. Selected 2. All
- Version Options: 1. New Version 2.Overwrite Latest

## JSON Structure
The exported JSON files follow a specific structure, ensuring that all necessary data is captured and easily accessible. Below is an example of the JSON structure:

![image](https://github.com/LizzyHerrera/ShapeExporter/assets/109104254/920f70b2-1760-427d-9ad8-89222268dc4a)

Explanation of Fields:
- mesh_name: The name of the base mesh.
- blendshape_name: The name of the blendshape node.
- deltas:
------latest_version: Contains the latest delta data.
------previous_version: Contains the previous delta data.

## Usage
Usage Export Options: 
-Choose between exporting from selected meshes or all meshes. 
-Select whether to create a new version or overwrite the latest version of exported data. 

Version Control: 
-Maintain both the latest and previous versions of exported blendshape deltas. 

User Interface: 
-Tree View: Displays blendshape data organized by mesh name, blendshape name, and target name. 
-Radio Buttons: Select export options (selected/all meshes) and versioning options (new version/overwrite latest).

## Motivation
This tool was developed to address specific needs encountered in 3D modeling workflows:

-Efficiency: Simplifies the process of exporting and managing blendshape deltas, reducing manual effort. 
-Versioning: Implements version control for exported data to easily track changes and revert if necessary.

## Credits

Special thanks to Alexander Richter for their valuable feedback and suggestions during the development of this tool.

---

