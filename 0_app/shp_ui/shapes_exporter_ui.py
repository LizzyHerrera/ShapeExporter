# ********************************************************************
#  UI functions and classes for the Shapes Exporter Tool
# ********************************************************************

import webbrowser

import maya.cmds as mc
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtGui, QtCore

import shp_utils
import shp_functions as fn


class ShapesExporterUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    UI_NAME = "shapeExporter_ui"

    def __init__(self):
        super(ShapesExporterUI, self).__init__()

        self.setObjectName(ShapesExporterUI.UI_NAME)
        self.setWindowTitle("Shapes Exporter")

        self.setup_ui()

        # Connect signals
        self.search_file_lineEdit.textChanged.connect(self.update_tab_status)

        # Initial update of tab status
        self.update_tab_status()

    def setup_ui(self):

        #Set Up components and layout.
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.mid_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # File Loader Section
        self.file_loader_widget = QtWidgets.QWidget()
        self.file_loader_layout = QtWidgets.QHBoxLayout(self.file_loader_widget)
        self.file_label = QtWidgets.QLabel("Set Dir:")
        self.search_file_lineEdit = QtWidgets.QLineEdit()
        self.search_file_btn = QtWidgets.QPushButton("...")
        self.file_loader_layout.addWidget(self.file_label)
        self.file_loader_layout.addWidget(self.search_file_lineEdit)
        self.file_loader_layout.addWidget(self.search_file_btn)

        self.main_layout.addWidget(self.file_loader_widget)
        self.main_layout.addLayout(self.mid_layout)

        # Shapes Tree View Section
        self.shapes_widget = QtWidgets.QWidget()
        self.shapes_layout = QtWidgets.QVBoxLayout(self.shapes_widget)
        self.bshapes_label = QtWidgets.QLabel("Blendshapes:")
        self.shapes_layout.addWidget(self.bshapes_label)
        self.shapes_treeView = QtWidgets.QTreeView()
        self.shapes_layout.addWidget(self.shapes_treeView)
        self.mid_layout.addWidget(self.shapes_widget)

        # Export/Import Section
        self.export_import_widget = QtWidgets.QTabWidget()
        self.export_from_scn_tab = QtWidgets.QWidget()
        self.export_tab = QtWidgets.QWidget()
        self.import_tab = QtWidgets.QWidget()

        self.export_import_widget.addTab(self.export_tab, "Export")
        self.export_import_widget.addTab(self.import_tab, "Import")

        # Setup export from file tab
        self.exp_separator_1 = QtWidgets.QFrame()
        self.exp_separator_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.exp_separator_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.export_layout = QtWidgets.QVBoxLayout(self.export_tab)
        self.exp_type_layout = QtWidgets.QHBoxLayout()
        self.exp_type_label = QtWidgets.QLabel("Type:")
        self.exp_comboBox = QtWidgets.QComboBox()
        self.exp_comboBox.addItem("JSON")
        #self.exp_comboBox.addItem("FBX")
        #self.exp_comboBox.addItem("OBJ")

        self.exp_type_layout.addWidget(self.exp_type_label)
        self.exp_type_layout.addWidget(self.exp_comboBox)

        self.export_layout.addLayout(self.exp_type_layout)

        # Export options section
        self.exp_separator_2 = QtWidgets.QFrame()
        self.exp_separator_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.exp_separator_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.exp_options_layout = QtWidgets.QVBoxLayout()
        self.exp_options_label = QtWidgets.QLabel("Options:")
        self.exp_selected_btn = QtWidgets.QRadioButton("Selected")
        #self.exp_modified_btn = QtWidgets.QRadioButton("Modified")
        self.exp_all_btn = QtWidgets.QRadioButton("All")

        self.exp_options_layout.addWidget(self.exp_options_label)
        self.exp_options_layout.addWidget(self.exp_selected_btn)
        #self.exp_options_layout.addWidget(self.exp_modified_btn)
        self.exp_options_layout.addWidget(self.exp_all_btn)

        self.exp_versions_layout = QtWidgets.QVBoxLayout()
        self.exp_versions_label = QtWidgets.QLabel("Version:")
        self.exp_new_ver_btn = QtWidgets.QRadioButton("New Version")
        self.exp_overwrite_btn = QtWidgets.QRadioButton("Overwrite Latest")

        self.exp_versions_layout.addWidget(self.exp_versions_label)
        self.exp_versions_layout.addWidget(self.exp_new_ver_btn)
        self.exp_versions_layout.addWidget(self.exp_overwrite_btn)

        # Create button groups for export options and versions
        self.export_options_group = QtWidgets.QButtonGroup(self)
        self.export_versions_group = QtWidgets.QButtonGroup(self)

        # Add radio buttons to their respective groups
        self.export_options_group.addButton(self.exp_selected_btn)
        self.export_options_group.addButton(self.exp_all_btn)

        self.export_versions_group.addButton(self.exp_new_ver_btn)
        self.export_versions_group.addButton(self.exp_overwrite_btn)

        # Set exclusive behavior for each button group
        self.export_options_group.setExclusive(True)
        self.export_versions_group.setExclusive(True)

        # Ensure initial selections
        self.exp_all_btn.setChecked(True)
        self.exp_new_ver_btn.setChecked(True)

        self.export_btn = QtWidgets.QPushButton("Export")

        self.export_layout.addWidget(self.exp_separator_1)
        self.export_layout.addLayout(self.exp_options_layout)
        self.export_layout.addWidget(self.exp_separator_2)
        self.export_layout.addLayout(self.exp_versions_layout)
        self.export_layout.addWidget(self.export_btn)


        # Setup import tab
        self.imp_separator_1 = QtWidgets.QFrame()
        self.imp_separator_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.imp_separator_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.import_layout = QtWidgets.QVBoxLayout(self.import_tab)
        self.imp_type_layout = QtWidgets.QHBoxLayout()
        self.imp_type_label = QtWidgets.QLabel("Type:")
        self.imp_comboBox = QtWidgets.QComboBox()
        self.imp_comboBox.addItem("JSON")
        #self.imp_comboBox.addItem("FBX")
        #self.imp_comboBox.addItem("OBJ")

        self.imp_type_layout.addWidget(self.imp_type_label)
        self.imp_type_layout.addWidget(self.imp_comboBox)

        self.import_layout.addLayout(self.imp_type_layout)

        # export options section
        self.imp_separator_2 = QtWidgets.QFrame()
        self.imp_separator_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.exp_separator_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imp_options_layout = QtWidgets.QVBoxLayout()
        self.imp_options_label = QtWidgets.QLabel("Options:")
        self.imp_selected_btn = QtWidgets.QRadioButton("Selected")
        self.imp_all_btn = QtWidgets.QRadioButton("All")

        self.imp_options_layout.addWidget(self.imp_options_label)
        self.imp_options_layout.addWidget(self.imp_selected_btn)
        self.imp_options_layout.addWidget(self.imp_all_btn)

        self.imp_versions_layout = QtWidgets.QHBoxLayout()
        self.imp_versions_label = QtWidgets.QLabel("Version:")
        self.imp_number_version_label = QtWidgets.QLabel()

        self.imp_versions_sel_layout = QtWidgets.QHBoxLayout()
        self.imp_latest_btn = QtWidgets.QRadioButton("Latest")
        self.imp_prev_btn = QtWidgets.QRadioButton("Previous")
        #self.imp_number_version_lineEdit = QtWidgets.QLineEdit()

        self.imp_versions_layout.addWidget(self.imp_versions_label)
        self.imp_versions_layout.addWidget(self.imp_number_version_label)

        self.imp_versions_sel_layout.addWidget(self.imp_latest_btn)
        self.imp_versions_sel_layout.addWidget(self.imp_prev_btn)
        #self.imp_versions_sel_layout.addWidget(self.imp_number_version_lineEdit)

        # Create button groups for import options and versions
        self.import_options_group = QtWidgets.QButtonGroup(self)
        self.import_versions_group = QtWidgets.QButtonGroup(self)

        # Add radio buttons to their respective groups
        self.import_options_group.addButton(self.imp_selected_btn)
        self.import_options_group.addButton(self.imp_all_btn)

        self.import_versions_group.addButton(self.imp_latest_btn)
        self.import_versions_group.addButton(self.imp_prev_btn)

        # Set exclusive behavior for each button group
        self.import_options_group.setExclusive(True)
        self.import_versions_group.setExclusive(True)

        # Ensure initial selections
        self.imp_all_btn.setChecked(True)
        self.imp_latest_btn.setChecked(True)

        self.import_btn = QtWidgets.QPushButton("Import")

        self.import_layout.addWidget(self.imp_separator_1)
        self.import_layout.addLayout(self.imp_options_layout)
        self.import_layout.addWidget(self.imp_separator_2)
        self.import_layout.addLayout(self.imp_versions_layout)
        self.import_layout.addLayout(self.imp_versions_sel_layout)
        self.import_layout.addWidget(self.import_btn)

        self.mid_layout.addWidget(self.export_import_widget)

        # Menubar
        self.menu_bar = self.menuBar()
        self.help_menu = self.menu_bar.addMenu("Help")
        self.documentation_action = QtWidgets.QAction("Documentation", self)
        self.help_menu.addAction(self.documentation_action)
        self.documentation_action.triggered.connect(self.press_help)

        # Connect signals
        self.search_file_btn.clicked.connect(self.open_file_dialog)
        self.export_btn.clicked.connect(self._on_export)

        # Customize shapes_treeView
        self.shapes_treeView.setHeaderHidden(True)
        self.shapes_treeView.setIconSize(QtCore.QSize(0, 0))  # Hide icons

    def open_file_dialog(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.search_file_lineEdit.setText(dir_path)
            self.populate_tree_view(dir_path)

    def populate_tree_view(self, dir_path):
        """
        Populate the tree view with the contents of the given directory path.
        """

        model = CustomFileSystemModel()
        model.setRootPath(dir_path)

        self.shapes_treeView.setModel(model)
        self.shapes_treeView.setRootIndex(model.index(dir_path))
        self.shapes_treeView.hideColumn(1)  # Hide size column
        self.shapes_treeView.hideColumn(2)  # Hide type column
        self.shapes_treeView.hideColumn(3)  # Hide date column

    def _on_export(self):
        path = self.search_file_lineEdit.text()

        if self.exp_new_ver_btn.isChecked():
            version = 'latest_version'
        else:
            version = 'latest_version'

        if self.exp_all_btn.isChecked():
            self._on_export_from_all_meshes(path, version)
        elif self.exp_selected_btn.isChecked():
            self._on_export_from_selected(path, version)

    def _on_export_from_selected(self, path, version):

        if path:
            print(f"Exporting to: {path}")
            meshes = mc.ls(sl=1)
            if meshes:
                fn.export_deltas_from_meshes(meshes, path, version)
                print('Deltas exported successfully')
            else:
                print("No meshes selected.")
        else:
            print("Please provide a valid file path.")

    def _on_export_from_all_meshes(self, path, version):

        if path:
            print(f"Exporting to: {path}")
            meshes = [mesh.name() for mesh in shp_utils.get_scene_meshes(transforms=True)]
            if meshes:
                fn.export_deltas_from_meshes(meshes, path, version)
                print('Deltas exported successfully')
            else:
                print("No meshes selected.")
        else:
            print("Please provide a valid file path.")

    def _on_import_from_all_meshes(self):
        pass

    def _on_import_selected(self):
        pass

    def _on_import(self):
        path = self.search_file_lineEdit.text()
        version = 'latest_version'

        if self.imp_all_btn.isChecked():
            self._on_import_from_all_meshes(path, version)
        elif self.imp_selected_btn.isChecked():
            self._on_import_selected(path, version)

    def dockCloseEventTriggered(self):
        """fully delete the windows when X is pressed"""
        mc.deleteUI("{}WorkspaceControl".format(ShapesExporterUI.UI_NAME))

    def update_tab_status(self):
        """
        Update the status of tabs based on the current state of the UI.
        """

        dir_enable = bool(self.search_file_lineEdit.text())

        #TODO : Make tabs enable if the treeView has data
        '''# Check if tree view has data
        if self.shapes_treeView.model() and self.shapes_treeView.model().rowCount(QtCore.QModelIndex()) > 0:
            file_enable = True  # Enable tabs if tree view has data
        else:
            file_enable = False  # Disable tabs if tree view is empty'''

        ix_export_scn_tab = self.export_import_widget.indexOf(self.export_from_scn_tab)
        self.export_import_widget.setTabEnabled(ix_export_scn_tab, dir_enable)

        ix_export_tab = self.export_import_widget.indexOf(self.export_tab)
        self.export_import_widget.setTabEnabled(ix_export_tab, dir_enable)

        ix_import_tab = self.export_import_widget.indexOf(self.import_tab)
        self.export_import_widget.setTabEnabled(ix_import_tab, dir_enable)

        # Set the current tab to the first tab that is enabled
        self.export_import_widget.setCurrentIndex(0)

    def press_help(self):
        webbrowser.open("https://github.com/LizzyHerrera/ShapeExporter")


class CustomFileSystemModel(QtWidgets.QFileSystemModel):
    """
    Custom file system model to modify the default behavior of QFileSystemModel.
    """
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DecorationRole:
            return None
        return super(CustomFileSystemModel, self).data(index, role)




