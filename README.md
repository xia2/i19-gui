[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/xia2/i19-gui.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/xia2/i19-gui/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/xia2/i19-gui.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/xia2/i19-gui/alerts/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# i19-gui

A graphical interface to the most commonly used data processing tools for single-crystal X-ray diffraction data on [beamline I19 of Diamond Light Source](https://www.diamond.ac.uk/Instruments/Crystallography/I19.html).

## Run it at Diamond

The GUI is distributed on Diamond's environment modules system as part of the `i19` modulefile.
To use it, first call
```Bash
module load i19
```
to load the environment module, then call
```Bash
i19.gui
```

## What can it do?

i19-gui gives you a user-friendly tool for running [screen19](https://github.com/xia2/screen19) and [xia2](https://github.com/xia2/xia2) processing on the Diamond computing clusters without having to know all the magic spells.
It aims to make your beamtime data processing quick and relatively effortless.
It contains all the most commonly used options for processing I19 diffraction data, including trickier cases such as samples in a diamond anvil pressure cell.
