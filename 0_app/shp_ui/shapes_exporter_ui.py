import maya.cmds as mc
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtGui, QtCore
import shp_functions as fn

class ShapesExporterUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    UI_NAME = "shpexporter_ui"

    def __init__(self):
        super(ShapesExporterUI, self).__init__()

        self.setObjectName(ShapesExporterUI.UI_NAME)
        self.setWindowTitle("Shapes Exporter")

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.mid_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # File Loader Section
        self.file_loader_widget = QtWidgets.QWidget()
        self.file_loader_layout = QtWidgets.QHBoxLayout(self.file_loader_widget)
        self.file_label = QtWidgets.QLabel("Directory:")
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
        self.export_import_widget.addTab(self.export_from_scn_tab, "Export from Scene")
        self.export_import_widget.addTab(self.export_tab, "Export from File")
        self.export_import_widget.addTab(self.import_tab, "Import")

        # Set up export from scene tab
        self.export_scn_layout = QtWidgets.QVBoxLayout(self.export_from_scn_tab)
        self.export_from_sel_btn = QtWidgets.QPushButton("Export from Selected")
        self.export_geos_btn = QtWidgets.QPushButton("Export from all geos")
        self.export_scn_layout.addWidget(self.export_from_sel_btn, alignment=QtCore.Qt.AlignTop)
        self.export_scn_layout.addWidget(self.export_geos_btn, alignment=QtCore.Qt.AlignTop)
        self.export_scn_layout.addStretch(1)


        # Setup export from file tab
        self.exp_separator_1 = QtWidgets.QFrame()
        self.exp_separator_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.exp_separator_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.export_layout = QtWidgets.QVBoxLayout(self.export_tab)
        self.exp_type_layout = QtWidgets.QHBoxLayout()
        self.exp_type_label = QtWidgets.QLabel("Type:")
        self.exp_comboBox = QtWidgets.QComboBox()
        self.exp_comboBox.addItem("JSON")
        self.exp_comboBox.addItem("FBX")
        self.exp_comboBox.addItem("OBJ")

        self.exp_type_layout.addWidget(self.exp_type_label)
        self.exp_type_layout.addWidget(self.exp_comboBox)

        self.export_layout.addLayout(self.exp_type_layout)

        # export options section
        self.exp_separator_2 = QtWidgets.QFrame()
        self.exp_separator_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.exp_separator_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.exp_options_layout = QtWidgets.QVBoxLayout()
        self.exp_options_label = QtWidgets.QLabel("Options:")
        self.exp_selected_btn = QtWidgets.QRadioButton("Selected")
        self.exp_modified_btn = QtWidgets.QRadioButton("Modified")
        self.exp_all_btn = QtWidgets.QRadioButton("All")

        self.exp_options_layout.addWidget(self.exp_options_label)
        self.exp_options_layout.addWidget(self.exp_selected_btn)
        self.exp_options_layout.addWidget(self.exp_modified_btn)
        self.exp_options_layout.addWidget(self.exp_all_btn)

        self.exp_versions_layout = QtWidgets.QVBoxLayout()
        self.exp_versions_label = QtWidgets.QLabel("Version:")
        self.exp_new_ver_btn = QtWidgets.QRadioButton("New Version")
        self.exp_overwrite_btn = QtWidgets.QRadioButton("Overwrite Current")

        self.exp_versions_layout.addWidget(self.exp_versions_label)
        self.exp_versions_layout.addWidget(self.exp_new_ver_btn)
        self.exp_versions_layout.addWidget(self.exp_overwrite_btn)

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
        self.imp_comboBox.addItem("FBX")
        self.imp_comboBox.addItem("OBJ")

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
        self.imp_number_version_label = QtWidgets.QLabel("#")

        self.imp_versions_sel_layout = QtWidgets.QHBoxLayout()
        self.imp_new_ver_btn = QtWidgets.QRadioButton("Latest")
        self.imp_overwrite_btn = QtWidgets.QRadioButton("Custom")
        self.imp_number_version_lineEdit = QtWidgets.QLineEdit()

        self.imp_versions_layout.addWidget(self.imp_versions_label)
        self.imp_versions_layout.addWidget(self.imp_number_version_label)

        self.imp_versions_sel_layout.addWidget(self.imp_new_ver_btn)
        self.imp_versions_sel_layout.addWidget(self.imp_overwrite_btn)
        self.imp_versions_sel_layout.addWidget(self.imp_number_version_lineEdit)

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
        self.settings_menu = self.menu_bar.addMenu("Settings")
        self.help_menu = self.menu_bar.addMenu("Help")
        self.reset_action = QtWidgets.QAction("Reset", self)
        self.documentation_action = QtWidgets.QAction("Documentation", self)
        self.settings_menu.addAction(self.reset_action)
        self.help_menu.addAction(self.documentation_action)

        # Connect signals
        self.search_file_btn.clicked.connect(self.open_file_dialog)
        self.export_from_sel_btn.clicked.connect(self._on_export_from_selected)

        # Customize shapes_treeView
        self.shapes_treeView.setHeaderHidden(True)
        self.shapes_treeView.setIconSize(QtCore.QSize(0, 0))  # Hide icons

    def open_file_dialog(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.search_file_lineEdit.setText(dir_path)
            self.populate_tree_view(dir_path)

    def populate_tree_view(self, dir_path):
        model = CustomFileSystemModel()
        model.setRootPath(dir_path)
        self.shapes_treeView.setModel(model)
        self.shapes_treeView.setRootIndex(model.index(dir_path))
        self.shapes_treeView.hideColumn(1)  # Hide size column
        self.shapes_treeView.hideColumn(2)  # Hide type column
        self.shapes_treeView.hideColumn(3)  # Hide date column

    def _on_export_from_selected(self):
        path = self.search_file_lineEdit.text()
        if path:
            print(f"Exporting to: {path}")
            meshes = mc.ls(sl=1)
            if meshes:
                fn.export_deltas_from_meshes(meshes, path)
                print('Deltas exported successfully')
            else:
                print("No meshes selected.")
        else:
            print("Please provide a valid file path.")

    def dockCloseEventTriggered(self):
        """fully delete the windows when X is pressed"""
        mc.deleteUI("{}WorkspaceControl".format(ShapesExporterUI.UI_NAME))

class CustomFileSystemModel(QtWidgets.QFileSystemModel):
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DecorationRole:
            return None
        return super(CustomFileSystemModel, self).data(index, role)


###################################################################################


