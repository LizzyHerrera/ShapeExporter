# Shape Exporter Tool for Autodesk Maya

This tool facilitates efficient exporting of blendshape deltas from Maya to JSON files, supporting version control and streamlined workflows.

Features Export Deltas: Export blendshape delta information as JSON files. Version Control: Supports maintaining the latest and previous versions of blendshape deltas. UI Integration: Intuitive UI with options to export from selected meshes or all meshes. Path Management: Automatically manages directory structure for exported data. Tree View Display: Organizes blendshape data in a hierarchical structure: 
---Mesh Name 
------Blendshape Name 
----------Target Name

Motivation This tool was developed to address specific needs encountered in 3D modeling workflows:

-Efficiency: Simplifies the process of exporting and managing blendshape deltas, reducing manual effort. 
-Versioning: Implements version control for exported data to easily track changes and revert if necessary.

Usage Export Options: 
-Choose between exporting from selected meshes or all meshes. 
-Select whether to create a new version or overwrite the latest version of exported data. 

Version Control: 
-Maintain both the latest and previous versions of exported blendshape deltas. 

User Interface: 
-Tree View: Displays blendshape data organized by mesh name, blendshape name, and target name. 
-Radio Buttons: Select export options (selected/all meshes) and versioning options (new version/overwrite latest).

Troubleshooting For issues, feedback, or feature requests, please create a new issue on the GitHub Issues page.

Acknowledgements Special thanks to Alexander Richter for their valuable feedback and suggestions during the development of this tool.
