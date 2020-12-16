# -*- coding: utf-8 -*-

# TODO:
#   fix "QObject::connect: Cannot queue arguments of type 'QTextCursor'" error
#   add image ranges
#   add HP functionality
#   add manual input commands


import fnmatch
import glob
import json
import operator
import os
import re
import subprocess
import sys
from collections import namedtuple
from datetime import datetime
from itertools import chain, repeat
from pathlib import Path
from time import sleep
from typing import Dict, Type, Union

from PyQt5 import QtCore, QtGui, QtWidgets, uic

OptionWidgetDict = Dict[Type[QtWidgets.QWidget], str]
OptionValues = Dict[str, Union[bool, int, str]]

auto_save_filename = "processing/.i19.gui.autosave.json"

# Dictionary of the key property name (in the Qt sense, i.e. the attribute name in
# Python terms) for each type of user option widget.
# Any children of a UIOptionsWindow instance that are of a type listed here will be
# considered user-defined settings.  The values of each of the named properties will
# be serialised and de-serialised to (auto-)save or (auto-)load them, or to remember
# and reset default values.
option_widgets: OptionWidgetDict = {
    QtWidgets.QCheckBox: "checked",
    QtWidgets.QComboBox: "currentIndex",
    QtWidgets.QLineEdit: "text",
}

Option = namedtuple(
    "Option", ["phil", "value", "condition", "convert"], defaults=[None, None, None]
)


def small_molecule(i):
    return i == 0


numbers_regex = re.compile(r"(\d+\.?\d*|\.\d+)")


def csv(parameters, number=2):
    # TODO: Add some exception handling to warn of mangled or invalid input.
    parameters = [str(float(param)) for param in re.findall(numbers_regex, parameters)]
    assert len(parameters) == number
    return ",".join(parameters)


def indexing_method(index=0):
    return ["fft3d", "fft1d", "real_space_grid_search", "low_res_spot_match"][index]


gasket_params = [
    f"ice_rings.{param}" for param in ("filter", "unit_cell", "space_group", "width")
]


def gasket_values(index, check):
    """Tungsten, steel"""
    unit_cell_params = ["3.1652", "2.87"]
    if check:
        unit_cell = ",".join(chain(repeat(unit_cell_params[index], 3), repeat("90", 3)))
        return True, unit_cell, "Im-3m", "0.02"


# Specify how option widgets translate to PHIL parameters to be passed to xia2.
# Once it is supported in xia2 (see #7, xia2/xia2#543), add this entry:
# findSpots_maxSpot_lineEdit=Option(
#     "max_spot_size", condition="findSpots_maxSpot", convert=int
# ),
option_specification = dict(
    comboBox=Option("small_molecule", condition=small_molecule, convert=small_molecule),
    import_TrustBeamCentre=Option("trust_beam_centre"),
    importReferenceGeometryPath=Option(
        "reference_geometry", condition="import_ReferenceGeometry"
    ),
    import_DD_lineEdit=Option(
        "detector_distance", condition="import_DD", convert=float
    ),
    import_BeamCentre_X_lineEdit=Option(
        "mosflm_beam_centre",
        value="import_BeamCentre_Y_lineEdit",
        condition="import_BeamCentre",
        convert=lambda *xy: ",".join(str(float(coord)) for coord in xy),
    ),
    import_wavelength_lineEdit=Option(
        "wavelength", condition="import_Wavelengh", convert=float
    ),
    findSpots_sigmaStrong_lineEdit=Option(
        "sigma_strong", condition="findSpots_sigmaStrong", convert=float
    ),
    findSpots_minSpot_lineEdit=Option(
        "min_spot_size", condition="findSpots_minSpot", convert=int
    ),
    findSpots_dmin_lineEdit=Option("d_min", condition="findSpots_dmin", convert=float),
    findSpots_dmax_lineEdit=Option("d_max", condition="findSpots_dmax", convert=float),
    findSpots_powderRings=Option("ice_rings.filter"),
    # Put gasket selection before user-specified powder rings, to allow the width of
    # the pre-specified powder rings to be adjusted with the options below.
    HP_gasket_comboBox=Option(
        gasket_params,
        value="HP_gasket_checkBox",
        condition=gasket_values,
        convert=gasket_values,
    ),
    findSpots_powderRingsUC_lineEdit=Option(
        "ice_rings.unit_cell",
        condition=["findSpots_powderRings", "findSpots_powderRingsSG_lineEdit"],
        convert=lambda parameters: csv(parameters, number=6),
    ),
    findSpots_powderRingsSG_lineEdit=Option(
        "ice_rings.space_group",
        condition=["findSpots_powderRings", "findSpots_powderRingsUC_lineEdit"],
    ),
    findSpots_powderRingsW_lineEdit=Option(
        "ice_rings.width", condition="findSpots_powderRings", convert=float
    ),
    findSpots_resolutionRange_lineEdit_1=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_2=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_3=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_4=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_5=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_6=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_7=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_8=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_9=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_resolutionRange_lineEdit_10=Option(
        "resolution_range", condition="findSpots_resolutionRange", convert=csv
    ),
    findSpots_circleMask_lineEdit=Option(
        "circle",
        condition="findSpots_circleMask",
        convert=lambda parameters: csv(parameters, number=3),
    ),
    findSpots_recMask_lineEdit=Option(
        "rectangle",
        condition="findSpots_recMask",
        convert=lambda parameters: csv(parameters, number=4),
    ),
    Index_method_comboBox=Option("method", convert=indexing_method),
    Index_UN_lineEdit=Option(
        "unit_cell",
        condition="Index_UN_SG_checkBox",
        convert=lambda parameters: csv(parameters, number=6),
    ),
    Index_SG_lineEdit=Option("space_group", condition="Index_UN_SG_checkBox"),
    Index_minCell_lineEdit=Option(
        "min_cell", condition="Index_minCell_checkBox", convert=float
    ),
    Index_maxCell_lineEdit=Option(
        "max_cell", condition="Index_maxCell_checkBox", convert=float
    ),
    Index_multiprocessing_checkBox=Option("multi_sweep_indexing"),
    Index_multiprocessing_checkBox_2=Option("multi_sweep_refinement"),
    Index_outliers_checkBox=Option("outlier.algorithm", convert=lambda _: "null"),
    Refine_FixBeamDetector_checkBox_2=Option(
        [
            "refinement.parameterisation.beam.fix",
            "refinement.parameterisation.detector.fix",
            "refinement.parameterisation.auto_reduction.action",
        ],
        convert=lambda _: ["all", "all", "fix"],
    ),
    Integrate_scanVarying_checkBox=Option("scan_varying", convert=operator.not_),
    Index_minCell_lineEdit_2=Option(
        "min_spots.overall", condition="Integrate_scanVarying_checkBox_2", convert=int
    ),
    Index_minCell_lineEdit_3=Option(
        "min_spots.per_degree",
        condition="Integrate_scanVarying_checkBox_2",
        convert=int,
    ),
    Refine_method_comboBox=Option("pipeline", value="dials-aimless"),
    Integrate_keepAllReflections_checkBox=Option("keep_all_reflections"),
    HP_correction_shaddowing_checkBox=Option("high_pressure.correction"),
    lineEdit_2=Option("anvil.thickness", condition="checkBox_3", convert=float),
)


class UIMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent_window=None, **kwargs):
        self.dials_version = ""
        self.opening_visit = "/dls/i19-2/data/2020/"
        self.visit = ""

        self.dataset_path = ""
        self.dataset = ""
        self.multiple_dataset = {}
        self.processing_path = ""

        self.run_list = []
        self.run_image_selector = False
        self.run_selection = []
        self.image_selection = {}
        self.prefix = ""

        self.computing_location = "Cluster"

        self.xia2_options_list = " small_molecule=true"
        self.xia2_command = "xia2 "
        self.tabs = ["tab1", "tab2", "tab3", "tab4", "tab5", "tab6", "tab7", "tab8"]
        self.tabstxt = [
            "tab1t",
            "tab2t",
            "tab3t",
            "tab4t",
            "tab5t",
            "tab6t",
            "tab7t",
            "tab8t",
        ]
        self.tabs_iv = ["IV_1", "IV_2", "IV_3", "IV_4", "IV_5", "IV_6", "IV_7", "IV_8"]
        self.tabs_rlv = [
            "RLV_1",
            "RLV_2",
            "RLV_3",
            "RLV_4",
            "RLV_5",
            "RLV_6",
            "RLV_7",
            "RLV_8",
        ]
        self.tabs_html = [
            "HTML_1",
            "HTML_2",
            "HTML_3",
            "HTML_4",
            "HTML_5",
            "HTML_6",
            "HTML_7",
            "HTML_8",
        ]
        self.tabs_processing_path = [
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
        ]
        self.tabs_num = 0

        super().__init__(parent=parent_window, **kwargs)
        uic.loadUi(Path(__file__).parent / "MainWindow.ui", self)

        self.menuFile_Open.triggered.connect(self.select_dataset)
        self.menuFile_Open_Multiple.triggered.connect(self.open_multiple)
        self.menuFile_Close_GUI.triggered.connect(self.close_gui)
        self.versionCurrent.triggered.connect(self.version_current)
        self.versionLatest.triggered.connect(self.version_latest)
        self.versionNow.triggered.connect(self.version_now)
        self.version1_4.triggered.connect(self.version_1_4)
        self.viewButtons_xia2.clicked.connect(self.run_xia2)
        self.viewButtons_screen19.clicked.connect(self.run_screen19)
        # Connect the 'xia2 options' button to the method that opens the options pane.
        self.viewButtons_options.clicked.connect(self.open_options)
        self.viewButtons_albula.clicked.connect(self.run_albula)

        # Remove the close button from the main log output tab, leaving the close
        # buttons on the other tabs active.
        tab_bar = self.outputTabs.tabBar()
        log_output = self.outputTabs.indexOf(self.logOutput)
        left_delete_button = tab_bar.tabButton(log_output, tab_bar.LeftSide)
        if left_delete_button:
            left_delete_button.deleteLater()
        right_delete_button = tab_bar.tabButton(log_output, tab_bar.RightSide)
        if right_delete_button:
            right_delete_button.deleteLater()
        tab_bar.setTabButton(log_output, tab_bar.LeftSide, None)
        tab_bar.setTabButton(log_output, tab_bar.RightSide, None)
        self.outputTabs.tabCloseRequested.connect(self.outputTabs.removeTab)

        self.show()

    @staticmethod
    def append_output(tab_name, new_lines_print):
        tab_name.appendPlainText(new_lines_print)
        tab_name.moveCursor(QtGui.QTextCursor.End)

    @staticmethod
    def get_dials_version():
        return os.popen("dials.version").read().split("-")[0]

    def select_dataset(self):
        path = self.opening_visit
        self.dataset_path = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "Select a dataset folder",
            path,
            QtWidgets.QFileDialog.ShowDirsOnly,
        )
        if self.dataset_path:
            self.multiple_dataset = {}
            self.append_output(
                self.logOutputTxt, "\n    Dataset Path:        " + self.dataset_path
            )
            self.dataset = self.dataset_path.split("/")[-1]  # dataset name
            if "staging" in self.dataset_path.split("/"):
                # /dls/staging/dls/i19-2/data/2019/cy23463-1/
                self.visit = "/".join(self.dataset_path.split("/")[:8]) + "/"
            else:
                # /dls/i19-2/data/2020/cm26492-2/
                self.visit = "/".join(self.dataset_path.split("/")[:6]) + "/"
            self.opening_visit = str(self.visit)
            self.append_output(self.logOutputTxt, "    Dataset:        " + self.dataset)
            for cbf_file in os.listdir(self.dataset_path):  # prefix
                if cbf_file.endswith("_00001.cbf"):
                    self.prefix = cbf_file[:-12]
                    break

            self.append_output(self.logOutputTxt, "    Prefix:        " + self.prefix)
            self.run_list = []
            run_images_dict = {}
            for cbf_files in os.listdir(self.dataset_path):  # runs in dataset
                if cbf_files.endswith("_00001.cbf"):
                    if cbf_files[:-12] == self.prefix:
                        run = int(cbf_files[-12:-10])
                        self.run_list.append(run)

            self.run_list.sort()
            self.append_output(
                self.logOutputTxt,
                "    Number of runs:        "
                + " ".join(map(str, (len(self.run_list), self.run_list))),
            )
            for run in self.run_list:  # number of images per run
                basename_match = self.prefix + "%02d" % run + "_*.cbf"
                num_cbf_run = len(
                    fnmatch.filter(os.listdir(self.dataset_path), basename_match)
                )
                run_images_dict[run] = num_cbf_run
            self.append_output(
                self.logOutputTxt, "    Images per run:    " + str(run_images_dict)
            )
            total_num_images = sum(run_images_dict.values())  # total number of images
            self.append_output(
                self.logOutputTxt,
                "    Total number of images:    " + str(total_num_images) + "\n",
            )
            # update labels
            self.dataset_info_dataset.setText(self.dataset)
            self.dataset_info_prefix.setText(self.prefix)
            self.dataset_info_images.setText(str(run_images_dict).strip("{}"))
            self.command_command.setPlainText(
                self.xia2_command + self.dataset_path + self.xia2_options_list
            )

    # file menu, open-> select dataset ####
    def open_multiple(self):
        path = self.opening_visit
        new_dataset_path = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select a dataset folder", path, QtWidgets.QFileDialog.ShowDirsOnly
        )

        self.dataset_path = "MULTIPLE"
        prefix = ""
        dataset = ""

        if new_dataset_path:
            self.append_output(
                self.logOutputTxt,
                "\n    New Dataset Path:        " + new_dataset_path,
            )

            dataset = new_dataset_path.split("/")[-1]  # dataset name
            if "staging" in self.dataset_path.split("/"):
                # /dls/staging/dls/i19-2/data/2019/cy23463-1/
                self.visit = "/".join(self.dataset_path.split("/")[:8]) + "/"
            else:
                # /dls/i19-2/data/2020/cm26492-2/
                self.visit = "/".join(self.dataset_path.split("/")[:6]) + "/"
            self.opening_visit = str(self.visit)
            self.append_output(self.logOutputTxt, "    New Dataset:        " + dataset)
            for cbf_file in os.listdir(new_dataset_path):  # prefix
                if cbf_file.endswith("_00001.cbf"):
                    prefix = cbf_file[:-12]
                    break

        if prefix:
            self.append_output(self.logOutputTxt, "    New Prefix:        " + prefix)
            run_list = []
            run_images_dict = {}
            for cbf_file in os.listdir(new_dataset_path):  # runs in dataset
                if cbf_file.endswith("_00001.cbf"):
                    if cbf_file[:-12] == prefix:
                        run = int(cbf_file[-12:-10])
                        run_list.append(run)

            run_list.sort()
            self.append_output(
                self.logOutputTxt,
                "    New Number of runs:    "
                + str(len(run_list))
                + " "
                + str(run_list),
            )
            for run in run_list:  # number of images per run
                basename_match = f"{prefix}{run:02d}_*.cbf"
                num_cbf_run = len(
                    fnmatch.filter(os.listdir(new_dataset_path), basename_match)
                )
                run_images_dict[run] = num_cbf_run
            self.append_output(
                self.logOutputTxt,
                "    New Images per run:    " + str(run_images_dict),
            )
            total_num_images = sum(run_images_dict.values())  # total number of images
            self.append_output(
                self.logOutputTxt,
                "    New Total number of images:    " + str(total_num_images) + "\n",
            )
            # update labels
            self.dataset_info_dataset.setText(dataset)
            self.dataset_info_prefix.setText(prefix)
            self.dataset_info_images.setText(str(run_images_dict).strip("{}"))
            self.command_command.setPlainText(
                self.xia2_command + self.dataset_path + self.xia2_options_list
            )

            self.multiple_dataset[dataset] = [new_dataset_path, prefix, run_list]
            self.append_output(
                self.logOutputTxt,
                "    Multiple runs:\n    " + str(self.multiple_dataset),
            )

    # file menu, close -> close GUI ####
    def close_gui(self):
        self.append_output(self.logOutputTxt, "\n\nClosing GUI\n\n")
        QtCore.QCoreApplication.instance().quit()

    # open albula ####
    def run_albula(self):
        self.append_output(self.logOutputTxt, self.dataset_path)
        if self.dataset_path == "":
            subprocess.Popen(
                ["sh", "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/albula.sh"]
            )
        else:
            self.append_output(self.logOutputTxt, "opening albula with first image")
            image = f"{self.dataset_path}/{self.prefix}{self.run_list[0]:02d}_00001.cbf"
            subprocess.Popen(
                ["sh", "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/albula.sh", image]
            )

    # open options window ###########################################################
    def open_options(self):
        self.append_output(self.logOutputTxt, "Opening options window")
        options_window = UIOptionsWindow(
            self.xia2_command,
            self.dataset_path,
            self.visit,
            self.logOutputTxt,
            self.run_list,
            self.prefix,
            self.opening_visit,
            self,
        )
        options_window.show()

    def update_options(self):
        self.command_command.setPlainText(
            self.xia2_command + self.dataset_path + self.xia2_options_list
        )

    def run_xia2(self):
        self.append_output(self.logOutputTxt, "\nRunning xia2\n")
        # single datasets ###########
        if not self.dataset_path == "MULTIPLE":
            self.append_output(self.logOutputTxt, "Single Dataset")
            if self.prefix == "":
                self.append_output(
                    self.logOutputTxt,
                    "\n\n #########################################################",
                )
                self.append_output(
                    self.logOutputTxt,
                    "    No cbf images found in directory, "
                    "please select dataset directory",
                )
                return
            self.run_xia2_dataset(self.dataset, self.dataset_path)
        # multiple datasets ###########
        if self.dataset_path == "MULTIPLE":  # if multiple input has been utilised
            self.append_output(self.logOutputTxt, "\n Multiple dataset processing\n")
            # {
            #     "01_Prot1_21": [
            #         "/dls/i19-2/data/2020/cy23401-1/01_Prot1_21",
            #         "Prot1_21_",
            #         [1, 2, 3],
            #     ]
            # }
            # {dataset: [dataset_path, prefix, runs]}
            if not self.run_image_selector:
                for dataset_key in self.multiple_dataset:
                    dataset_path, prefix, _ = self.multiple_dataset[dataset_key]
                    if not prefix:
                        self.append_output(
                            self.logOutputTxt,
                            "\n\n ############################"
                            "############################b",
                        )
                        self.append_output(
                            self.logOutputTxt,
                            "    No cbf images found in directory, "
                            "please select dataset directory",
                        )
                        return
                    self.run_xia2_dataset(dataset_key, dataset_path)
            else:
                for dataset_key in self.multiple_dataset:
                    dataset = dataset_key
                    dataset_path = self.multiple_dataset[dataset_key][0] + "/"
                    prefix = self.multiple_dataset[dataset_key][1]
                    runs = self.multiple_dataset[dataset_key][2]
                    if prefix == "":
                        self.append_output(
                            self.logOutputTxt,
                            "\n\n ############################"
                            "############################c",
                        )
                        self.append_output(
                            self.logOutputTxt,
                            "    No cbf images found in directory, "
                            "please select dataset directory",
                        )
                        return
                    else:
                        xia2_input = ""
                        if self.run_selection:
                            for entry in self.run_selection:
                                xia2_input = (
                                    xia2_input
                                    + " image="
                                    + dataset_path
                                    + prefix
                                    + str("%02d_00001.cbf" % int(entry))
                                )
                                if entry in self.image_selection:
                                    xia2_input = (
                                        xia2_input + ":" + self.image_selection[entry]
                                    )
                        else:  # runs have NOT been selected
                            for run in runs:
                                xia2_input = (
                                    xia2_input
                                    + " image="
                                    + dataset_path
                                    + prefix
                                    + str("%02d_00001.cbf" % int(run))
                                )
                                if (run - 1) in self.image_selection:
                                    xia2_input = (
                                        xia2_input + ":" + self.image_selection[run - 1]
                                    )
                    self.run_xia2_dataset(dataset, xia2_input)

    def run_xia2_dataset(self, input_dataset, xia2_input):  # prefix # visit # dataset
        # create processing path
        time_date = str(datetime.utcnow().strftime("%Y%m%d_%H%M"))
        self.processing_path = (
            f"{self.visit}processing/xia2GUI/{input_dataset}_{time_date}/"
        )
        if not os.path.exists(self.visit + "processing/xia2GUI/"):
            os.makedirs(self.visit + "processing/xia2GUI/")
        if not os.path.exists(self.processing_path):
            os.makedirs(self.processing_path)

        self.processing_path_path.setText(self.processing_path)
        self.tabs_processing_path[self.tabs_num] = self.processing_path

        self.append_output(self.logOutputTxt, "Xia2 command:")
        # this is the bit I think i need to change!!!
        # dataset and prefix I would guess is required
        input_xia2_command = self.xia2_command + xia2_input + self.xia2_options_list
        self.append_output(self.logOutputTxt, "    " + input_xia2_command)

        # create job file

        job_file = self.processing_path + "job.sh"
        with open(job_file, "a") as f:
            f.write(str("cd " + self.processing_path) + "\n")
            f.write(str("module load dials" + self.dials_version) + "\n")
            f.write(str(input_xia2_command) + "\n")

        ################################################################################
        # open new tab with dataset and date
        self.tabs[self.tabs_num] = QtWidgets.QWidget()
        self.tabs[self.tabs_num].setObjectName("tabs[tabNum]")

        # plain text
        # clear previous??
        self.tabstxt[self.tabs_num] = QtWidgets.QPlainTextEdit(self.tabs[self.tabs_num])
        self.tabstxt[self.tabs_num].setGeometry(QtCore.QRect(0, 32, 756, 372))
        self.tabstxt[self.tabs_num].setObjectName("tabstxt[tabNum]")

        # buttons
        tab_num = int(self.tabs_num)

        self.tabs_iv[self.tabs_num] = QtWidgets.QPushButton(self.tabs[self.tabs_num])
        self.tabs_iv[self.tabs_num].setGeometry(QtCore.QRect(120, 0, 151, 31))
        self.tabs_iv[self.tabs_num].setFont(self.font_size10)
        self.tabs_iv[self.tabs_num].setObjectName("xia2output_dialsImage")
        self.tabs_iv[self.tabs_num].setText("Image Viewer")
        self.tabs_iv[self.tabs_num].clicked.connect(
            lambda: self.run_dials_image_viewer(tab_num)
        )

        self.tabs_rlv[self.tabs_num] = QtWidgets.QPushButton(self.tabs[self.tabs_num])
        self.tabs_rlv[self.tabs_num].setGeometry(QtCore.QRect(270, 0, 151, 31))
        self.tabs_rlv[self.tabs_num].setFont(self.font_size10)
        self.tabs_rlv[self.tabs_num].setObjectName("xia2output_reciprocal")
        self.tabs_rlv[self.tabs_num].setText("Reciprocal Lattice")
        self.tabs_rlv[self.tabs_num].clicked.connect(
            lambda: self.run_dials_reciprocal_lattice(tab_num)
        )

        self.tabs_html[self.tabs_num] = QtWidgets.QPushButton(self.tabs[self.tabs_num])
        self.tabs_html[self.tabs_num].setGeometry(QtCore.QRect(420, 0, 151, 31))
        self.tabs_html[self.tabs_num].setFont(self.font_size10)
        self.tabs_html[self.tabs_num].setObjectName("xia2output_html")
        self.tabs_html[self.tabs_num].setText("HTML")
        self.tabs_html[self.tabs_num].clicked.connect(
            lambda: self.run_dials_html(tab_num)
        )

        self.outputTabs.addTab(self.tabs[self.tabs_num], "")
        self.outputTabs.setTabText(
            self.outputTabs.indexOf(self.tabs[self.tabs_num]),
            input_dataset + "_" + time_date,
        )

        # edit plain text
        self.tabstxt[self.tabs_num].appendPlainText("\nRunning xia2\n")
        self.tabstxt[self.tabs_num].appendPlainText("Xia2 command:")
        self.tabstxt[self.tabs_num].appendPlainText("    " + input_xia2_command + "\n")

        ################################################################################
        # run xia2

        if input_dataset == "":
            tab_name = self.tabstxt[self.tabs_num]
            dataset_error_statement = (
                "\n\n No dataset has been selected (File>Open) \n\n"
            )
            self.append_output(self.logOutputTxt, dataset_error_statement)
            self.append_output(tab_name, dataset_error_statement)
        else:
            if self.computing_location == "Local":
                # run xia2 locally
                subprocess.Popen(["sh", job_file])
            else:
                # run xia2 on cluster?
                # module load global/cluster
                # "qsub -pe smp 1 -q medium.q " + job_file
                # module load global/hamilton
                # qsub -pe smp 20 -cwd -q all.q -P i19-2 -o /dev/null -e /dev/null \
                #   job.sh

                if "staging" in self.visit.split("/"):
                    os.system(
                        f"module load global/cluster && qsub -pe smp 1 "
                        f"-q medium.q {job_file}"
                    )
                else:
                    os.system(
                        "module load global/hamilton && qsub -pe smp 20 "
                        f"-q all.q -P i19-2 -o /dev/null -e /dev/null {job_file}"
                    )

            ############################################################################
            # output xia2.txt into tab
            self.thread = MyThread2(
                self.processing_path,
                input_dataset,
                self.tabstxt,
                self.tabs_num,
                self.logOutputTxt,
                "xia2.txt",
            )

            self.thread.finished.connect(self.thread_finished)
            self.thread.started.connect(self.thread_started)
            # self.thread.terminated.connect(self.threadTerminated)

            self.thread.start()

        ################################################################################
        self.tabs_num += 1
        if self.tabs_num > 8:
            self.tabs_num = 0

    def run_screen19(self):
        self.append_output(self.logOutputTxt, "\nRunning screen19\n")
        if self.prefix == "":
            self.append_output(
                self.logOutputTxt,
                "\n\n #########################################################",
            )
            self.append_output(
                self.logOutputTxt,
                "    No cbf images found in directory, please select dataset directory",
            )
            return
        else:
            # create processing path
            time_date = str(datetime.utcnow().strftime("%Y%m%d_%H%M"))
            self.processing_path = (
                self.visit
                + "processing/xia2GUI/"
                + self.dataset
                + "_s19_"
                + time_date
                + "/"
            )
            if not os.path.exists(self.visit + "processing/xia2GUI/"):
                os.makedirs(self.visit + "processing/xia2GUI/")
            if not os.path.exists(self.processing_path):
                os.makedirs(self.processing_path)

            self.processing_path_path.setText(self.processing_path)
            self.tabs_processing_path[self.tabs_num] = self.processing_path

            self.append_output(self.logOutputTxt, "screen19 command:")

            # remove unwanted xia2 commands
            screen19_options_list = ""
            for command in self.xia2_options_list.split(" "):
                if command == "small_molecule=true":
                    pass
                else:
                    screen19_options_list = screen19_options_list + command + " "

            input_screen19_command = (
                "screen19 " + self.dataset_path + screen19_options_list
            )
            self.append_output(self.logOutputTxt, "    " + input_screen19_command)

            # create job file
            job_file = self.processing_path + "job.sh"
            with open(job_file, "a") as jf:
                jf.write(str("cd " + self.processing_path) + "\n")
                jf.write(str("module load dials" + self.dials_version) + "\n")
                jf.write(str(input_screen19_command) + "\n")

            ############################################################################
            # open new tab with dataset and date
            self.tabs[self.tabs_num] = QtWidgets.QWidget()

            self.tabs[self.tabs_num].setObjectName("tabs[tab_num]")

            # plain text
            # clear previous??
            self.tabstxt[self.tabs_num] = QtWidgets.QPlainTextEdit(
                self.tabs[self.tabs_num]
            )
            self.tabstxt[self.tabs_num].setGeometry(QtCore.QRect(0, 32, 756, 372))
            self.tabstxt[self.tabs_num].setObjectName("tabstxt[tab_num]")

            # buttons
            tab_num = int(self.tabs_num)

            self.tabs_iv[self.tabs_num] = QtWidgets.QPushButton(
                self.tabs[self.tabs_num]
            )
            self.tabs_iv[self.tabs_num].setGeometry(QtCore.QRect(120, 0, 151, 31))
            self.tabs_iv[self.tabs_num].setFont(self.font_size10)
            self.tabs_iv[self.tabs_num].setObjectName("xia2output_dialsImage")
            self.tabs_iv[self.tabs_num].setText("Image Viewer")
            self.tabs_iv[self.tabs_num].clicked.connect(
                lambda: self.run_dials_image_viewer(tab_num)
            )

            self.tabs_rlv[self.tabs_num] = QtWidgets.QPushButton(
                self.tabs[self.tabs_num]
            )
            self.tabs_rlv[self.tabs_num].setGeometry(QtCore.QRect(270, 0, 151, 31))
            self.tabs_rlv[self.tabs_num].setFont(self.font_size10)
            self.tabs_rlv[self.tabs_num].setObjectName("xia2output_reciprocal")
            self.tabs_rlv[self.tabs_num].setText("Reciprocal Lattice")
            self.tabs_rlv[self.tabs_num].clicked.connect(
                lambda: self.run_dials_reciprocal_lattice(tab_num)
            )

            self.tabs_html[self.tabs_num] = QtWidgets.QPushButton(
                self.tabs[self.tabs_num]
            )
            self.tabs_html[self.tabs_num].setGeometry(QtCore.QRect(420, 0, 151, 31))
            self.tabs_html[self.tabs_num].setFont(self.font_size10)
            self.tabs_html[self.tabs_num].setObjectName("xia2output_html")
            self.tabs_html[self.tabs_num].setText("HTML")
            self.tabs_html[self.tabs_num].clicked.connect(
                lambda: self.run_dials_html(tab_num)
            )

            self.outputTabs.addTab(self.tabs[self.tabs_num], "")
            self.outputTabs.setTabText(
                self.outputTabs.indexOf(self.tabs[self.tabs_num]),
                self.dataset + "_s19_" + time_date,
            )

            # edit plain text
            self.tabstxt[self.tabs_num].appendPlainText("\nRunning screen19\n")
            self.tabstxt[self.tabs_num].appendPlainText("screen19 command:")
            self.tabstxt[self.tabs_num].appendPlainText(
                "    " + input_screen19_command + "\n"
            )

            ############################################################################
            # run screen19

            if self.dataset == "":
                tab_name = self.tabstxt[self.tabs_num]
                dataset_error_statement = (
                    "\n\n Dataset has not be selected (File>Open) \n\n"
                )
                self.append_output(self.logOutputTxt, dataset_error_statement)
                self.append_output(tab_name, dataset_error_statement)
            else:
                if self.computing_location == "Local":
                    # run screen19 locally
                    subprocess.Popen(["sh", job_file])
                else:
                    if "staging" in self.visit.split("/"):
                        os.system(
                            "module load global/cluster && qsub -pe smp 1 -q medium.q "
                            + job_file
                        )
                    else:
                        os.system(
                            "module load global/hamilton && qsub -pe smp 20 "
                            f"-q all.q -P i19-2 -o /dev/null -e /dev/null {job_file}"
                        )

                ########################################################################
                # output xia2.txt into tab
                self.thread = MyThread2(
                    self.processing_path,
                    self.dataset,
                    self.tabstxt,
                    self.tabs_num,
                    self.logOutputTxt,
                    "screen19.log",
                )

                self.thread.finished.connect(self.thread_finished)
                self.thread.started.connect(self.thread_started)
                # self.thread.terminated.connect(self.threadTerminated)

                self.thread.start()

            ############################################################################
            self.tabs_num += 1
            if self.tabs_num > 8:
                self.tabs_num = 0

    def thread_started(self):
        self.append_output(self.logOutputTxt, "\n*** Thread started ***\n")

    def thread_finished(self):
        self.append_output(self.logOutputTxt, "\n*** Thread finished ***\n")

    def stop_thread(self):
        self.append_output(self.logOutputTxt, "\n*** Stopping thread ***\n")
        # self.MyThread2.stop()
        # self.MyThread2.quit()

    # open run dials Reciprocal Lattice viewer ####
    def run_dials_reciprocal_lattice(self, tabs_num):
        self.append_output(self.logOutputTxt, "Opening dials reciprocal lattice viewer")
        self.append_output(
            self.logOutputTxt,
            "Processing path:" + self.tabs_processing_path[tabs_num],
        )

        latest_expt = ""
        latest_expt_time = ""
        latest_refl = ""
        latest_refl_time = ""

        expt_files = glob.glob(
            self.tabs_processing_path[tabs_num] + "/**/*.expt", recursive=True
        )
        refl_files = glob.glob(
            self.tabs_processing_path[tabs_num] + "/**/*.refl", recursive=True
        )
        for expt_file in expt_files:
            file_time = os.path.getmtime(expt_file)
            if latest_expt_time == "":
                latest_expt = expt_file
                latest_expt_time = file_time
            else:
                if file_time > latest_expt_time:
                    latest_expt = expt_file
                    latest_expt_time = file_time
        for refl_file in refl_files:
            file_time = os.path.getmtime(refl_file)
            if latest_refl_time == "":
                latest_refl = refl_file
                latest_refl_time = file_time
            else:
                if file_time > latest_refl_time:
                    latest_refl = refl_file
                    latest_refl_time = file_time
        if latest_expt == "":
            self.append_output(
                self.logOutputTxt,
                "\n\n *** Expt was not present in processing path, "
                "please wait unit after initial importing *** \n\n",
            )
            return
        if latest_refl == "":
            self.append_output(
                self.logOutputTxt,
                "\n\n ***Refl was not present in processing path, "
                "please wait unit after initial spot finding *** \n\n",
            )
            return
        else:
            self.append_output(
                self.logOutputTxt, "\nReflection file: " + str(latest_refl)
            )
            self.append_output(
                self.logOutputTxt, "Experiment file: " + str(latest_expt) + "\n"
            )
            subprocess.Popen(
                [
                    "sh",
                    (
                        "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/"
                        "dialsReciprocalLatticeViewer.sh"
                    ),
                    latest_expt,
                    latest_refl,
                ]
            )

    def run_dials_image_viewer(self, tabs_num):
        self.append_output(self.logOutputTxt, "Opening dials image viewer")
        self.append_output(
            self.logOutputTxt,
            "Processing path:" + self.tabs_processing_path[tabs_num],
        )

        latest_expt = ""
        latest_expt_time = ""
        latest_refl = ""
        latest_refl_time = ""

        expt_files = glob.glob(
            self.tabs_processing_path[tabs_num] + "/**/*.expt", recursive=True
        )
        refl_files = glob.glob(
            self.tabs_processing_path[tabs_num] + "/**/*.refl", recursive=True
        )
        for expt_file in expt_files:
            file_time = os.path.getmtime(expt_file)
            if latest_expt_time == "":
                latest_expt = expt_file
                latest_expt_time = file_time
            else:
                if file_time > latest_expt_time:
                    latest_expt = expt_file
                    latest_expt_time = file_time
        for refl_file in refl_files:
            file_time = os.path.getmtime(refl_file)
            if latest_refl_time == "":
                latest_refl = refl_file
                latest_refl_time = file_time
            else:
                if file_time > latest_refl_time:
                    latest_refl = refl_file
                    latest_refl_time = file_time
        if latest_expt == "":
            self.append_output(
                self.logOutputTxt,
                "\n\n ***Expt was not present in processing path, "
                "please wait unit after initial importing *** \n\n",
            )
        else:
            self.append_output(
                self.logOutputTxt, "\nReflection file: " + str(latest_refl)
            )
            self.append_output(
                self.logOutputTxt, "Experiment file: " + str(latest_expt) + "\n"
            )
            subprocess.Popen(
                [
                    "sh",
                    (
                        "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/"
                        "dialsImageViewer.sh"
                    ),
                    latest_expt,
                    latest_refl,
                ]
            )

    def run_dials_html(self, tabs_num):
        self.append_output(self.logOutputTxt, "Opening HTML")
        self.append_output(
            self.logOutputTxt,
            "Processing path:" + self.tabs_processing_path[tabs_num],
        )

        latest_html = ""
        latest_html_time = ""

        html_files = glob.glob(
            self.tabs_processing_path[tabs_num] + "/**/*.html", recursive=True
        )
        for html_file in html_files:
            file_time = os.path.getmtime(html_file)
            if latest_html_time == "":
                latest_html = html_file
                latest_html_time = file_time
            else:
                if file_time > latest_html_time:
                    latest_html = html_file
                    latest_html_time = file_time

        if latest_html == "":
            self.append_output(
                self.logOutputTxt,
                (
                    "\n\n *** html file was not present in processing path, "
                    "please wait unit after initial importing *** \n\n"
                ),
            )
        else:
            self.append_output(self.logOutputTxt, "HTML file: " + str(latest_html))
            subprocess.Popen(
                [
                    "sh",
                    "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/html.sh",
                    latest_html,
                ]
            )

    # version menu, change version
    def version_current(self):
        self.append_output(self.logOutputTxt, "Changing to dials version to current.")
        dial_version_pop = (
            os.popen("module unload dials; module load dials; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dials_version = ""
        # update version label
        self.menu_version.setTitle("Version(" + dial_version_pop + ")")
        self.append_output(self.logOutputTxt, "    Version(" + dial_version_pop + ")")

    # version menu, change version to latest
    def version_latest(self):
        self.append_output(self.logOutputTxt, "Changing to dials version to latest.")
        dial_version_pop = (
            os.popen("module unload dials; module load dials/latest; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dials_version = "/latest"
        # update version label
        self.menu_version.setTitle("Version(" + dial_version_pop + ")")
        self.append_output(self.logOutputTxt, "    Version(" + dial_version_pop + ")")

    # version menu, change version to now
    def version_now(self):
        self.append_output(self.logOutputTxt, "Changing to dials version to Now.")
        dial_version_pop = (
            os.popen("module unload dials; module load dials/now; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dials_version = "/now"
        # update version label
        self.menu_version.setTitle("Version(" + dial_version_pop + ")")
        self.append_output(self.logOutputTxt, "    Version(" + dial_version_pop + ")")

    # version menu, change version to 1.4
    def version_1_4(self):
        self.append_output(self.logOutputTxt, "Changing to dials version to 1.4.")
        dial_version_pop = (
            os.popen("module unload dials; module load dials/1.4; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dials_version = "/1.4"
        # update version label
        self.menu_version.setTitle("Version(" + dial_version_pop + ")")
        self.append_output(self.logOutputTxt, "    Version(" + dial_version_pop + ")")

    # version menu, change version to 2.1
    def version_2_1(self):
        self.append_output(self.logOutputTxt, "Changing to dials version to 2.1.")
        dial_version_pop = (
            os.popen("module unload dials; module load dials/2.1; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dials_version = "/2.1"
        # update version label
        self.menu_version.setTitle("Version(" + dial_version_pop + ")")
        self.append_output(self.logOutputTxt, "    Version(" + dial_version_pop + ")")


class MyThread2(QtCore.QThread):
    # finished = pyqtSignal(object)
    finished = QtCore.pyqtSignal()

    def __init__(
        self, processing_path, dataset, tabstxt, tabs_num, log_output_txt, log_file
    ):
        QtCore.QThread.__init__(self)
        self.processingPath = processing_path
        self.tabstxt = tabstxt
        self.tabsNum = tabs_num
        self.dataset = dataset
        self.mainTab_txt = log_output_txt
        self.logFile = log_file

    def __del__(self):
        self.wait()

    def run(self):
        tab_name = self.tabstxt[self.tabsNum]
        log_output_txt = self.mainTab_txt
        xia2_txt_lines_num_previous = 0
        is_running = "Yes"
        sleep(3)
        while is_running == "Yes":
            xia2txt = self.processingPath + self.logFile
            if os.path.isfile(xia2txt):
                xia2_txt_lines = [line.strip() for line in open(xia2txt)]
                new_lines = xia2_txt_lines[xia2_txt_lines_num_previous:]
                if len(new_lines) == 0:
                    pass
                else:
                    new_lines_print = "\n".join(new_lines)
                    xia2_txt_lines_num_previous = len(xia2_txt_lines)
                    tab_name.appendPlainText(new_lines_print)
                    tab_name.moveCursor(QtGui.QTextCursor.End)
                    if "Status: normal termination" in xia2_txt_lines:
                        output_message = self.tr(
                            "\n\nEnd of xia2 processing detected.\n"
                            "Stopping output to tab\n\n"
                        )
                        log_output_txt.appendPlainText(output_message)
                        log_output_txt.moveCursor(QtGui.QTextCursor.End)
                        sleep(0.1)
                        tab_name.appendPlainText(output_message)
                        tab_name.moveCursor(QtGui.QTextCursor.End)
                    if "xia2.support@gmail.com" in xia2_txt_lines:
                        output_message = self.tr(
                            "\n\nEnd of xia2 processing detected.\n"
                            "Stopping output to tab\n\n"
                        )
                        log_output_txt.appendPlainText(output_message)
                        log_output_txt.moveCursor(QtGui.QTextCursor.End)
                        sleep(0.1)
                        tab_name.appendPlainText(output_message)
                        tab_name.moveCursor(QtGui.QTextCursor.End)
            else:
                log_output_txt.appendPlainText("xia2.txt file does not exist yet")
                log_output_txt.moveCursor(QtGui.QTextCursor.End)
            sleep(5)
        log_output_txt.appendPlainText("finishing")
        log_output_txt.moveCursor(QtGui.QTextCursor.End)
        self.finished.emit()


class UIOptionsWindow(QtWidgets.QMainWindow):
    def __init__(
        self,
        xia2_command="",
        dataset_path="",
        visit="",
        run_list=None,
        prefix="",
        opening_visit="",
        parent_window=None,
        **kwargs,
    ):
        self.xia2_command = xia2_command
        self.dataset_path = dataset_path
        self.run_list = run_list or []
        self.ref_geometry_path = ""
        self.visit = visit
        self.run_image_selector = False
        self.run_selection = []
        self.image_selection = {}
        self.prefix = prefix
        self.opening_visit = opening_visit
        self.saved_options_path = None

        super().__init__(parent=parent_window, **kwargs)
        uic.loadUi(Path(__file__).parent / "OptionsWindow.ui", self)

        # Get all the widgets that record user-specified options.
        # This approach is about ten times faster than the findChildren method.
        self._option_widgets = {
            name: attribute
            for name, attribute in self.__dict__.items()
            if type(attribute) in option_widgets
        }

        self.default_options = self.options

        self.load_options_auto()

        # Connect buttons to methods.
        self.updateButton.clicked.connect(self.update_options)
        self.resetButton.clicked.connect(self.reset_options)
        self.saveButton.clicked.connect(self.save_options_manually)
        self.loadButton.clicked.connect(self.load_options_manually)
        for reference_geometry_button in (
            self.importReferenceGeometryBrowse,
            self.hpReferenceGeometryBrowse,
        ):
            reference_geometry_button.clicked.connect(self.browse_for_reference_model)

        # TODO: Dynamically create a checkbox for each sweep found.

        self.show()

    def log_output(self, message):
        try:
            log_widget = self.parent().logOutputTxt
        except AttributeError:
            print(message)
        else:
            log_widget.appendPlainText(message)
            log_widget.moveCursor(QtGui.QTextCursor.End)

    @property
    def options(self):
        return {
            name: widget.property(option_widgets[type(widget)])
            for name, widget in self._option_widgets.items()
        }

    @options.setter
    def options(self, new_values: OptionValues):
        for name, widget in self._option_widgets.items():
            value = new_values.get(name)
            if value is not None:
                property_name = option_widgets[type(widget)]
                widget.setProperty(property_name, value)

    def browse_for_reference_model(self):
        ref_geometry_path = self.ref_geometry_path or self.opening_visit
        ref_geometry_path, _filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption=self.tr("Select calibrated instrument model"),
            directory=ref_geometry_path,
            filter=self.tr("DIALS experiment list files (*.expt)"),
        )
        if ref_geometry_path:
            self.ref_geometry_path = ref_geometry_path
            ref_geometry_path = Path(ref_geometry_path)

            output_message = self.tr(
                "\nReference geometry path:\n"
                f"\t{ref_geometry_path.parent}\n"
                "Reference geometry file:\n"
                f"\t{ref_geometry_path.name}"
            )
            self.log_output(output_message)

            self.importReferenceGeometryPath.setText(ref_geometry_path.name)

    def reset_options(self):
        self.options = self.default_options

    def save_options_manually(self):
        path = self.saved_options_path or self.opening_visit
        option_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr("Choose a location for the saved settings"),
            directory=path,
            filter=self.tr("JSON files (*.json)"),
        )
        if option_file:
            self.saved_options_path = option_file
            self.save_options(Path(option_file))

    def save_options_auto(self):
        if self.visit:
            self.save_options(Path(self.visit) / auto_save_filename)

    def save_options(self, saved_options_path):
        output_message = self.tr(f"\n\tSaving settings to {saved_options_path}.")
        self.log_output(output_message)
        with open(saved_options_path, "w") as f:
            json.dump(self.options, f)

    def load_options_manually(self):
        path = self.saved_options_path or self.opening_visit
        options_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption=self.tr("Choose a file containing saved settings"),
            directory=path,
            filter=self.tr("JSON files (*.json)"),
        )
        if options_file:
            self.saved_options_path = options_file
            self.load_options(Path(options_file))

    def load_options_auto(self):
        saved_options_path = Path(self.visit) / auto_save_filename
        if not self.visit:
            output_message = self.tr(
                "\nSince you have not selected a visit or dataset, "
                "any previously auto-saved xia2 settings won't be loaded "
                "and your new settings cannot be auto-saved.\n"
                "If you have previously saved some settings and wish to load them, "
                "press the 'Load settings' button.\n"
                "You can also save your settings with the 'Save settings' button."
            )
            self.log_output(output_message)
        elif saved_options_path.is_file():
            self.load_options(saved_options_path)
        else:
            self.log_output(
                f"No auto-saved options found for the visit {self.visit}.\n"
                f"A new auto-save file will be created at {auto_save_filename}."
            )

    def load_options(self, saved_options_path: Path):
        self.log_output(self.tr(f"\n\tLoading settings from {saved_options_path}."))
        with open(saved_options_path) as f:
            self.options = json.load(f)

    def phil_params(self):
        pass

    def update_options(self):
        options = ""

        # import #######
        for variable in self.optionListImport:
            if variable.isChecked():
                if variable == self.import_trust_beam_centre:
                    options = options + " trust_beam_centre=true"
                if variable == self.import_reference_geometry:
                    if self.ref_geometry_path == "":
                        output_message = self.tr(
                            "    *** Reference geometry error. Please select "
                            ".expt file with browse button first ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " reference_geometry="
                            + str(self.ref_geometry_path)
                        )
                if variable == self.import_dd:
                    if self.import_dd_line_edit.text() == "":
                        output_message = self.tr(
                            "    *** Detector Distance Error. Please input "
                            "detector distance e.g. 85.01"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        output_message = self.tr(
                            "Detector distance: " + str(self.import_dd_line_edit.text())
                        )
                        self.log_output(output_message)
                        options = (
                            options
                            + " detector_distance="
                            + str(self.import_dd_line_edit.text())
                        )

                if variable == self.import_beam_centre:
                    if self.import_beam_centre_x_line_edit.text() == "":
                        output_message = self.tr(
                            "    *** Beam centre error. Please input Y"
                        )
                        self.log_output(output_message)
                        return
                    elif self.import_beam_centre_y_line_edit.text() == "":
                        output_message = self.tr(
                            "    *** Detector distance error. Please input X"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        output_message = self.tr(
                            "Detector distance: "
                            + str(self.import_beam_centre_x_line_edit.text())
                            + ","
                            + str(self.import_beam_centre_y_line_edit.text())
                        )
                        self.log_output(output_message)
                        options = (
                            options
                            + " mosflm_beam_centre="
                            + str(self.import_beam_centre_x_line_edit.text())
                            + ","
                            + str(self.import_beam_centre_y_line_edit.text())
                        )

                if variable == self.import_wavelengh:
                    if self.import_wavelength_line_edit.text() == "":
                        output_message = self.tr(
                            "    *** Wavelength input error. "
                            "Please add wavelength e.g. 85.01"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        output_message = self.tr(
                            "Wavelength: "
                            + str(self.import_wavelength_line_edit.text())
                        )
                        self.log_output(output_message)
                        options = (
                            options
                            + " wavelength="
                            + str(self.import_wavelength_line_edit.text())
                        )

                if variable == self.import_fix_beam_detector_check_box:
                    options = (
                        options + " integrate.phil_file=/dls_sw/i19/scripts/HP/"
                        "integration_additional_inputs.phil"
                    )

                if variable == self.import_run_selector_check_box:
                    self.run_selection = []
                    self.run_image_selector = True
                    for num, run in enumerate(self.runSelectorList, start=1):
                        if run.isChecked():
                            self.run_selection.append(num)
                    self.log_output("Run selector:    " + str(self.run_selection))
                if variable == self.Import_type_checkBox:
                    if self.Import_type_comboBox.currentText() == "Protein":
                        pass
                    else:
                        options = options + " small_molecule=True"

        # spot finding #######
        for variable in self.optionListSpotFinding:
            if variable.isChecked():
                if variable == self.findSpots_sigmaStrong:
                    if self.findSpots_sigmaStrong_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Sigma strong error."
                            " Please enter sigma strong e.g. 6 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " sigma_strong="
                            + str(self.findSpots_sigmaStrong_lineEdit.text())
                        )
                if variable == self.findSpots_minSpot:
                    if self.findSpots_minSpot_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Min spot size error, "
                            "please enter min spots size e.g. 2 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " min_spot_size="
                            + str(self.findSpots_minSpot_lineEdit.text())
                        )
                if variable == self.findSpots_maxSpot:
                    if self.findSpots_maxSpot_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Max spot size error, "
                            "please enter max spots size e.g. 2 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " max_spot_size="
                            + str(self.findSpots_maxSpot_lineEdit.text())
                        )
                if variable == self.findSpots_dmin:
                    if self.findSpots_dmin_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** d_min error, please enter d_min e.g. 0.84 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " d_min="
                            + str(self.findSpots_dmin_lineEdit.text())
                        )
                if variable == self.findSpots_dmax:
                    if self.findSpots_dmax_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** d_max error, please enter d_max e.g. 10 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " d_max="
                            + str(self.findSpots_dmax_lineEdit.text())
                        )
                if variable == self.findSpots_iceRings:
                    options = options + " ice_rings=true"

                if variable == self.findSpots_powderRings:

                    powder_ring_line_edits = [
                        self.findSpots_powderRingsUC_lineEdit.text(),
                        self.findSpots_powderRingsSG_lineEdit.text(),
                        self.findSpots_powderRingsW_lineEdit.text(),
                    ]
                    for entry in powder_ring_line_edits:
                        if entry == "":
                            output_message = self.tr(
                                "    *** Powder ring mask error ***"
                            )
                            self.log_output(output_message)
                            return
                    ice_rings_uv_command = " ice_rings.unit_cell=" + str(
                        self.findSpots_powderRingsUC_lineEdit.text()
                    )
                    ice_rings_sg_command = " ice_rings.space_group=" + str(
                        self.findSpots_powderRingsSG_lineEdit.text()
                    )
                    ice_rings_w_command = " ice_rings.width=" + str(
                        self.findSpots_powderRingsW_lineEdit.text()
                    )
                    options = (
                        options
                        + ice_rings_uv_command
                        + ice_rings_sg_command
                        + ice_rings_w_command
                    )

                if variable == self.findSpots_resolutionRange:
                    find_spot_res_range_list = [
                        self.findSpots_resolutionRange_lineEdit_1.text(),
                        self.findSpots_resolutionRange_lineEdit_2.text(),
                        self.findSpots_resolutionRange_lineEdit_3.text(),
                        self.findSpots_resolutionRange_lineEdit_4.text(),
                        self.findSpots_resolutionRange_lineEdit_5.text(),
                        self.findSpots_resolutionRange_lineEdit_6.text(),
                        self.findSpots_resolutionRange_lineEdit_7.text(),
                        self.findSpots_resolutionRange_lineEdit_8.text(),
                        self.findSpots_resolutionRange_lineEdit_9.text(),
                        self.findSpots_resolutionRange_lineEdit_10.text(),
                    ]
                    for res in find_spot_res_range_list:
                        if not res == "":
                            options = options + " resolution_range=" + str(res)

                if variable == self.findSpots_circleMask:
                    if self.findSpots_circleMask_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Circle mask error, please enter in the "
                            "following format: xc,yc,r ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " circle="
                            + str(self.findSpots_circleMask_lineEdit.text())
                        )

                if variable == self.findSpots_recMask:
                    if self.findSpots_recMask_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Rectangle mask error, please enter is "
                            "the following format: x0,x1,y0,y1 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " rectangle="
                            + str(self.findSpots_recMask_lineEdit.text())
                        )

        # indexing #######
        for variable in self.optionListIndexing:
            if variable.isChecked():
                if variable == self.Index_method_checkBox:
                    options = (
                        options
                        + " method="
                        + str(self.Index_method_comboBox.currentText())
                    )
                if variable == self.Index_scanVarying_checkBox:
                    options = options + " scan_varying=False"
                if variable == self.Index_UN_SG_checkBox:
                    uc_sg_line_edits = [
                        self.Index_UN_lineEdit.text(),
                        self.Index_SG_lineEdit.text(),
                    ]
                    for entry in uc_sg_line_edits:
                        self.log_output(entry)
                        if entry == "":
                            output_message = self.tr(
                                "    *** Error in unit cell or space group entry ***"
                            )
                            self.log_output(output_message)
                            return
                    uc_command = " unit_cell=" + str(self.Index_UN_lineEdit.text())
                    sg_command = " space_group=" + str(self.Index_SG_lineEdit.text())
                    options = options + uc_command + sg_command
                if variable == self.Index_minCell_checkBox:
                    if self.Index_minCell_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Please enter valid min cell ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " min_cell="
                            + str(self.Index_minCell_lineEdit.text())
                        )
                if variable == self.Index_maxCell_checkBox:
                    if self.Index_maxCell_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Please enter valid max cell ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " max_cell="
                            + str(self.Index_maxCell_lineEdit.text())
                        )
                if variable == self.Index_multiprocessing_checkBox:
                    options = options + " multi_sweep_processing=True"
                if variable == self.Index_multiSweepRefine_checkBox:
                    options = options + " multi_sweep_refinement=False"
                if variable == self.Index_outliers_checkBox:
                    options = options + " outlier.algorithm=null"

        # integrate #####
        for variable in self.optionListIntegrate:
            if variable.isChecked():
                if variable == self.Integrate_keepAllReflections_checkBox:
                    options = options + " keep_all_reflections=true"
                if variable == self.Integrate_scanVarying_checkBox:
                    options = options + " scan_varying=False"
                if variable == self.Integrate_minSpotProfile_checkBox:
                    spot_profile_line_edits = [
                        self.Integrate_minCellOverall_lineEdit.text(),
                        self.Integrate_minCellDegree_lineEdit.text(),
                    ]
                    for entry in spot_profile_line_edits:
                        if entry == "":
                            output_message = self.tr(
                                "    *** Error in overall or per degree entry ***"
                            )
                            self.log_output(output_message)
                            return
                        if self.visit == "":
                            output_message = self.tr(
                                "    *** For this option a .phil needs to be created, "
                                "this requires a the visit to be known."
                                "    Please open a dataset and retry (File>Open). ***"
                            )
                            self.log_output(output_message)
                            return
                    overall_line = (
                        "    profile.gaussian_rs.min_spots.overall="
                        + str(self.Integrate_minCellOverall_lineEdit.text())
                        + "\n"
                    )
                    degree_line = (
                        "    profile.gaussian_rs.min_spots.per_degree="
                        + str(self.Integrate_minCellDegree_lineEdit.text())
                        + "\n"
                    )
                    xia2_gui_path = self.visit + "processing/xia2GUI/"
                    if not os.path.exists(xia2_gui_path):
                        os.makedirs(xia2_gui_path)
                    phil_file = xia2_gui_path + "integration_additional_inputs.phil"
                    with open(phil_file, "a") as f:
                        f.write(
                            "refinement_additional_inputs.phil:\n"
                            + overall_line
                            + degree_line
                        )
                    options = options + " integrate.phil_file=" + phil_file

        # refine ####
        for variable in self.optionListRefineScale:
            if variable.isChecked():
                if variable == self.Refine_method_checkBox:
                    options = (
                        options
                        + " method="
                        + str(self.Refine_method_comboBox.currentText())
                    )
                if variable == self.Refine_FixBeamDetector_checkBox:
                    xia2_gui_path = self.visit + "processing/xia2GUI/"
                    if not os.path.exists(xia2_gui_path):
                        os.makedirs(xia2_gui_path)
                    phil_file = xia2_gui_path + "refine_additional_inputs.phil"
                    with open(phil_file, "a") as f:
                        refine_line1 = "refinement.parameterisation.beam.fix=all\n"
                        refine_line2 = "refinement.parameterisation.detector.fix=all\n"
                        refine_line3 = (
                            "refinement.parameterisation.auto_reduction.action=fix\n"
                        )
                        f.write(refine_line1 + refine_line2 + refine_line3)
                    options = options + " refine.phil_file=" + phil_file

        # other #####
        for variable in self.optionListOther:
            if variable.isChecked():
                if variable == self.Other_failover_checkBox:
                    options = options + " failover=true"
                if variable == self.Other_manualInput1_checkBox:
                    options = options + " " + self.Other_manualInput1_lineEdit.text()
                if variable == self.Other_manualInput2_checkBox:
                    options = options + " " + self.Other_manualInput2_lineEdit.text()
                if variable == self.Other_manualInput3_checkBox:
                    options = options + " " + self.Other_manualInput3_lineEdit.text()
                if variable == self.Other_manualInput4_checkBox:
                    options = options + " " + self.Other_manualInput4_lineEdit.text()

        # HP #####
        for variable in self.optionListHP:
            if variable.isChecked():
                if variable == self.HP_correction_shadowing_checkBox:
                    options = (
                        options
                        + " high_pressure.correction=True dynamic_shadowing=True "
                        "resolution_range=999,15"
                    )
                if variable == self.HP_scanVarying_checkBox:
                    options = options + " scan_varying=False"
                if variable == self.HP_ReferenceGeometry_checkBox:
                    if self.ref_geometry_path == "":
                        output_message = self.tr(
                            "    *** Reference geometry error. "
                            "Please select .expt file with browse button first ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " reference_geometry="
                            + str(self.ref_geometry_path)
                        )
                if variable == self.HP_gasket_checkBox:
                    gasket_type = str(self.HP_gasket_comboBox.currentText())
                    if gasket_type == "Tungsten":
                        options = (
                            options + " ice_rings.filter=True "
                            "ice_rings.unit_cell=3.1652,3.1652,3.1652,90,90,90 "
                            "ice_rings.space_group=Im-3m "
                            "ice_rings.width=0.02"
                        )
                    if gasket_type == "Steel":
                        # Steel gaskets are often either Fe or Ni.
                        # The unit cell for Fe is given below.
                        options = (
                            options + " ice_rings.filter=True "
                            "ice_rings.unit_cell=2.87,2.87,2.87,90,90,90 "
                            "ice_rings.space_group=Im-3m "
                            "ice_rings.width=0.02"
                        )

                if variable == self.HP_gasketUser_checkBox:
                    powder_ring_line_edits = [
                        self.HP_gasketUserUC_lineEdit.text(),
                        self.HP_gasketUserSG_lineEdit.text(),
                        self.HP_gasketUserW_lineEdit.text(),
                    ]
                    for entry in powder_ring_line_edits:
                        if entry == "":
                            output_message = self.tr(
                                "    *** Powder ring mask error ***"
                            )
                            self.log_output(output_message)
                            return
                    ice_rings_uv_command = " ice_rings.unit_cell=" + str(
                        self.HP_gasketUserUC_lineEdit.text()
                    )
                    ice_rings_sg_command = " ice_rings.space_group=" + str(
                        self.HP_gasketUserSG_lineEdit.text()
                    )
                    ice_rings_w_command = " ice_rings.width=" + str(
                        self.HP_gasketUserW_lineEdit.text()
                    )
                    options = (
                        options
                        + ice_rings_uv_command
                        + ice_rings_sg_command
                        + ice_rings_w_command
                    )
                # medium difficulty:
                if variable == self.HP_UN_SG_checkBox:
                    uc_sg_line_edits = [
                        self.HP_UN_lineEdit.text(),
                        self.HP_SG_lineEdit.text(),
                    ]
                    for entry in uc_sg_line_edits:
                        self.log_output(entry)
                        if entry == "":
                            output_message = self.tr(
                                "    *** Error in unit cell or space group entry ***"
                            )
                            self.log_output(output_message)
                            return
                    uc_command = " unit_cell=" + str(self.HP_UN_lineEdit.text())
                    sg_command = " space_group=" + str(self.HP_SG_lineEdit.text())
                    options = options + uc_command + sg_command

                if variable == self.HP_dmin_checkBox:
                    if self.HP_dmin_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** d_min HP error, please enter d_min e.g. 0.84 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options + " d_min=" + str(self.HP_dmin_lineEdit.text())
                        )

                if variable == self.HP_runStartEnd_checkBox:
                    self.run_image_selector = True
                    counter = 0
                    self.runStartEnd_lineEdits = [
                        self.HP_runStartEnd_lineEdit_1.text(),
                        self.HP_runStartEnd_lineEdit_2.text(),
                        self.HP_runStartEnd_lineEdit_3.text(),
                        self.HP_runStartEnd_lineEdit_4.text(),
                        self.HP_runStartEnd_lineEdit_5.text(),
                        self.HP_runStartEnd_lineEdit_6.text(),
                        self.HP_runStartEnd_lineEdit_7.text(),
                        self.HP_runStartEnd_lineEdit_8.text(),
                        self.HP_runStartEnd_lineEdit_9.text(),
                        self.HP_runStartEnd_lineEdit_10.text(),
                    ]

                    for entry in self.runStartEnd_lineEdits:
                        if entry == "":
                            counter += 1
                        else:
                            self.image_selection[counter] = entry
                            counter += 1
                    output_message = self.tr(
                        "Image start/end option selected.\n"
                        "    " + str(self.image_selection)
                    )
                    self.log_output(output_message)

                if variable == self.HP_FixBeamDetector_checkBox:
                    options = (
                        options + " integrate.phil_file=/dls_sw/i19/scripts/HP/"
                        "integration_additional_inputs.phil"
                    )
                    # integration_additional_inputs.phil:
                    # refinement.parameterisation.beam.fix=all
                    # refinement.parameterisation.detector.fix=all
                    # refinement.parameterisation.auto_reduction.action=fix

                if variable == self.HP_anvilThickness_checkBox:
                    if self.HP_anvilThickness_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Anvil thickness input error, "
                            "please enter thickness e.g. 2.1 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        options = (
                            options
                            + " high_pressure.anvil.thickness="
                            + str(self.HP_anvilThickness_lineEdit.text())
                        )

                if variable == self.HP_anvilOpeningAngle_checkBox:
                    if self.HP_anvilOpeningAngle_lineEdit.text() == "":
                        output_message = self.tr(
                            "    *** Anvil opening angle input error, "
                            "please enter opening angle e.g. 38 ***"
                        )
                        self.log_output(output_message)
                        return
                    else:
                        pass
                        # options = options + " high_pressure.anvil.angle=" + \
                        #           str(self.HP_anvilOpeningAngle_lineEdit.text())

        if not self.dataset_path == "MULTIPLE":

            if not self.run_image_selector:
                dataset_input = self.dataset_path

            else:  # causing issues when multiple ###########
                if self.dataset_path == "":
                    dataset_input = self.dataset_path
                    self.log_output(
                        "Dataset must be selected before selecting runs or images "
                        "start/end"
                    )
                else:
                    dataset_input = ""
                    if self.run_selection:  # runs have been selected
                        for entry in self.run_selection:
                            dataset_input = (
                                dataset_input
                                + " image="
                                + self.dataset_path
                                + "/"
                                + self.prefix
                                + str("%02d_00001.cbf" % int(entry))
                            )
                            if (entry - 1) in self.image_selection:
                                dataset_input = (
                                    dataset_input
                                    + ":"
                                    + self.image_selection[entry - 1]
                                )
                    else:  # runs have NOT been selected
                        for run in self.run_list:
                            dataset_input = (
                                dataset_input
                                + " image="
                                + self.dataset_path
                                + "/"
                                + self.prefix
                                + str("%02d_00001.cbf" % int(run))
                            )
                            if (run - 1) in self.image_selection:
                                dataset_input = (
                                    dataset_input + ":" + self.image_selection[run - 1]
                                )

            self.dataset_path = dataset_input

        self.log_output(
            "\n\nUpdating options"
            + "\n    Xia2 command: "
            + "\n    "
            + self.xia2_command
            + self.dataset_path
            + options
        )

        ui_main_window = self.parent()
        ui_main_window.xia2_command = self.xia2_command
        ui_main_window.dataset_path = self.dataset_path
        ui_main_window.xia2_options_list = options
        ui_main_window.update_options()

        self.save_options_auto()


if __name__ == "__main__":
    # We must assign the QApplication and MainWindow instances to variables to
    # prevent garbage collection messing with the open UI.
    app = QtWidgets.QApplication(sys.argv)
    # QApplication.setOverrideCursor(Qt.WaitCursor)
    ui = UIMainWindow()
    sys.exit(app.exec_())
