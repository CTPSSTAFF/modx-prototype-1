# Getting Started with MoDX

This document is a "Getting Started Guide" for MoDX. It walks new users through all the steps required to install and run MoDX, including:
* Installing Anaconda Navigator
* Creating an appropriately-configured Anaconda Environment in which to run MoDX Jupyter notebooks
* Launching MoDX Jupyter notebooks
* and more.

## Introduction 

The CTPS Travel Demand Model Data Explorer (a.k.a. __MoDX__) is a colleciton of [Jupyter](https://jupyter.org) notebooks that allow users without access to a TransCAD machine
and a TransCAD software license to view the inputs to and outputs from CTPS's Travel Demand Model, generate reports, graphs, and maps from this data,
and otherwise have a jolly good time frolicking in what otherwise might seem to be tens of gigabytes of unintelligible gibberish. (A Jupyter Notebook is an open-source web
application that allows user to create and share documents that contain live code, equations, visualizations and narrative text.) The code in MoDX Jupyter notebooks is
written in the [Python](https://python.org) programming language, and makes use of many "packages" in addition to those included in the Python Standard Library.
These packages provide support for working with files in [OMX](https://github.com/osPlanning/omx/wiki/Specification) matrix format,
efficiently executing numerical calcutions on large quantities of data, working with tabular and spatial datain "data frames", 
and generating static and interactive graphs, plots, and maps.  

Because of the many packages required by MoDX, and the subtle dependencies among them, Anaconda is used to build and maintain a consistent set of these packages
that are known to work together. Without such a tool, maintaining a consistent set of packages among the many and varied users of ModDX would become an enormous
resource drain, not to mention headache. Consequently, getting started with MoDX first entails installing Anaconda, and creating a correct environment in which
to run MoDX Jupyter notebooks.

## Installing Anaconda Navigator

Although it is possible to run Anaconda as a "command line" tool (a.k.a. "conda"), we strongly recommend installing Anaconda Navigator, a graphical front-end
for Anaconda that will help make working with Anaconda simpler particularly for newcomers. Installation instructions for your operating system
can be found [here](https://docs.anaconda.com/anaconda/install/). __Install the  _individual_ edition of Anaconda.__ 
We recommend installing Anaconda in _administrator_ mode.

## Creating an Anaconda Environment for MoDX

MoDX requires a parther.
Execute the following steps __in sequence__ to create the configuration required by MoDX; assign this configuration the name __modx_p1d0_config__:
* Launch Anaconda Navigator
* Select __Environments__ from the list of choices on the left-hand side of the page.
* Press the __+ Create__ button
* In the dialog box that appears:
* * Set __Name__ to __modx_p1d0_config__
* * Check the box for __Python__, and select version __3.7__ (_not version 3.8!__)
* * Press the __Create__ button
* * The new environment will appear in the list of environments (under "Search Environments") in the Navigator window.
* Install the __openmatrix__ package - this package is not known to any Anaconda "Channel", and so must be installed manually:
* * Right-mouse click on the __modx_p1d0_config__ environment, and select __terminal__.
* * In the terminal window that appears type _pip install -m openmatrix_
* Install the __jenkspy__ package - This is also a somewhat specialized package and must be installed manually.
* * Use the same sequence of steps as for __openmatrix__.
* * You may minimize the terminal window at this point, and return to Anaconda Navigator.
* Install the __pandas__ package
* * From the combo-box at the top of the right-hand portion of the Anaconda window, select __Not installed__. (It probably reads __Installed__ at Navigator start-up.)
* * In the search box, near the top right of the Navigator window, enter __pandas__.
* * In the search results list, check the box next to __pandas__.
* * Click the __Apply__ button that appears in the bottom right hand portion of the Navigator window.
* Install the __geopands__ package
* Install the __hvplot__ package
* Install the __geoviews__ package
* Install the __folium__ package

## Cloning the MoDX GitHub Repository

* Set this folder as the default location from which to launch Jupyter notebooks.

## Creating a "Sandbox" Folder for Your MoDX Output

## Launching MoDX Jupyter Notbooks

