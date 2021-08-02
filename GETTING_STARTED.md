# Getting Started with MoDX

This document is a "Getting Started Guide" for MoDX. It walks new users through all the steps required to install and run MoDX, including:
* Installing Anaconda Navigator
* Creating an appropriately-configured Anaconda Environment in which to run MoDX Jupyter notebooks
* Launching MoDX Jupyter notebooks
* and more.

## Introduction 

The CTPS Travel Demand Model Data Explorer (a.k.a. __MoDX__) is a colleciton of [Jupyter](https://jupyter.org) notebooks that allow users without access to a TransCAD machine
and a TransCAD software license to view the inputs to and outputs from CTPS's Travel Demand Model, generate reports, graphs, and maps from this data,
and otherwise have a jolly good time frolicking about in what otherwise might seem to be tens of gigabytes of unintelligible gibberish. 

A Jupyter Notebook is an open-source web
application that allows user to create and share documents that contain live code, equations, visualizations and narrative text. The code in MoDX Jupyter notebooks is
written in the [Python](https://python.org) programming language, and makes use of many "packages" in addition to those included in the Python Standard Library.
These packages provide support forsuch things as working with files in [OMX](https://github.com/osPlanning/omx/wiki/Specification) matrix format,
efficiently executing numerical calcutions on large arrays of of data, working with tabular and spatial datain "data frames", 
generating static and interactive graphs, plots, and maps, and so forth.

Because of the many packages required by MoDX, and the subtle dependencies among them, we use [Anaconda](https://www.anaconda.com/) to build and maintain
a consistent set of these packages that is known to work together.
 Without such a tool, maintaining a consistent set of packages among the many and varied users of ModDX would become an enormous
resource drain, not to mention headache. Consequently, getting started with MoDX first entails installing Anaconda and creating a correct environment in which
to run MoDX Jupyter notebooks.

## Installing Anaconda and Anaconda Navigator

Install the [Anaconda Individual Edition](https://www.anaconda.com/products/individual).
This installation will require 477 MegaBytes of storage on your hard drive on a Windows 10 system.
The installation includes the Anaconda Shell ("command box") as well as Anaconda Navigator, a graphical front-end to Anaconda.
We will be working with Anaconda both at the command-line and using the GUI.

## Creating an Anaconda Environment for MoDX

A collection of packages that are compatible and work together is called an _environment_ in the Anaconda world.
MoDX requires a specific collection of packages, based on Python version 3.8.
In order to create such an environment, do the following:
* Go to the [MoDX GitHub page](https://www.github.com/CTPSSTAFF/modx-prototype-1)
* Navigate to the file __environments/modx_p1d0_envt.yml__
* Save the file on your local computer, keepong the name "modx_p1d0_envt.yml"
* Fron the Windows 10 Start menu, select __Anaconda3  (64-bit) > Anaconda Prompt (anaconda3)__ - this opens an Anaconda command window
* In this command window, type __conda env create -f modx_p1d0_envt.yml__, being sure to specify the _full path_ to the .yml file.

## Gettng Your Local System Ready to Run MoDX

* Clone the Cloning the MoDX GitHub Repository:
* * Change directory to the __parent__ directory into which you want to clone the MoDX GitHub repo, then clone it:
* * __git clone https://github.com/CTPSSTAFF/modx-prototype-1__
* Set this folder as the default location from which to launch Jupyter notebooks.
* * TBD
* Create a "sandbox" folder for your MoDX output:
* * __mkdir 

## Launching MoDX Jupyter Notbooks

