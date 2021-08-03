# Getting Started with MoDX

This document is a "Getting Started Guide" for CTPS's Travel Demand Model Data Explorer (a.k.a. __MoDX__.) 
It walks new users through all the steps required to install and run MoDX, including:
* Installing Anaconda 
* Creating a Anaconda _environment_ in which to run MoDX Jupyter notebooks
* Getting your local system ready to run ModDX Jupyter notebooks
* Launching Jupyter notebooks
* Running a MoDX Jupyter notebook
* Closing a MoDX Jupyter notebook 
* Closing down Jupyter notebooks

## Introduction 

MoDX is a colleciton of [Jupyter](https://jupyter.org) notebooks that allow users without access to a TransCAD machine
and a TransCAD software license to view the inputs to and outputs from CTPS's Travel Demand Model, generate reports, graphs, and maps from this data,
and otherwise to frolic about in what otherwise might appear to be tens of gigabytes of unintelligible gibberish. 

A Jupyter Notebook is an open-source web
application that allows user to create and share documents that contain live code, equations, visualizations and narrative text. The code in MoDX Jupyter notebooks is
written in the [Python](https://python.org) programming language, and makes use of many "packages" in addition to those included in the Python Standard Library.
These packages provide support forsuch things as working with files in [OMX](https://github.com/osPlanning/omx/wiki/Specification) matrix format,
efficiently executing numerical calcutions on large arrays of of data, working with tabular and spatial datain "data frames", 
generating static and interactive graphs, plots, and maps, and so forth.

Because of the many packages required by MoDX, and the subtle dependencies among them, we use [Anaconda](https://www.anaconda.com/) to build and maintain
a consistent set of these packages that is known to work together.
Without such a tool, maintaining a consistent set of packages among the many and varied users of ModDX would become an enormous and time-consuming headache.
Consequently, getting started with MoDX first entails installing Anaconda and creating a correct environment in which
to run MoDX Jupyter notebooks.

## Installing Anaconda and Anaconda Navigator

Install the [Anaconda Individual Edition](https://www.anaconda.com/products/individual).
This installation will require 477 MegaBytes of storage on your hard drive on a Windows 10 system.
The installation includes the Anaconda Shell ("command box") as well as Anaconda Navigator, a graphical front-end to Anaconda.
It is useful to become familiar with both the command-line and graphical interfaces to Anaconda.

## Creating an Anaconda Environment for MoDX

A collection of packages that are compatible and work together is called an _environment_ in the Anaconda world.
MoDX requires a specific collection of packages, based on Python version __3.8__.
In order to create such an environment, perform the following steps:
* Go to the [MoDX GitHub page](https://www.github.com/CTPSSTAFF/modx-prototype-1)
* Navigate to the file __environments/modx_p1d0_envt.yml__
* Save the file on your local computer, keeping the name "modx_p1d0_envt.yml"
* Fron the Windows 10 Start menu, select __Anaconda3  (64-bit) > Anaconda Prompt (anaconda3)__ - this opens an Anaconda command window
* In this command window, type __conda env create -f modx_p1d0_envt.yml__, being sure to specify the _full path_ to the .yml file.

## Gettng Your Local System Ready to Run MoDX

To get your local computer system ready to run MoDX, perform the following steps:
* Clone the MoDX GitHub Repository:
* * Change directory to the __parent__ directory into which you want to clone the MoDX GitHub repo; then clone it:
* * __git clone https://github.com/CTPSSTAFF/modx-prototype-1__
* * For the purpose of the rest of this discussion, we'll call the _fully-qualified_ path to this directory __my_modx_dir__
* Set this folder as the default location from which to launch Jupyter notebooks.
* * In an Anaconda command window, type __jupyter notebook --generate-config__
* * This will write to the file __C:\Users\username\.jupyter\jupyter_notebook_config.py__
* * Browse to the file location and open it in an editor (such as Notepad++, Vim, or VS Code)
* * Search for the following line in the file: # __c.NotebookApp.notebook_dir = ''__
* * Delete the comment character ('#') on this line
* * Replace the entire line with with __c.NotebookApp.notebook_dir = 'my_modx_dir'__
* * * Note that __my_modx_dir__ must be surrounded in single quotes
* * * For example: __c.NotebookApp.notebook_dir = 'S:/my_modx_notebooks'__
* * * NOTE: The full path to one's MoDX directory must be delimited by __single__ quotes, and use __forward__ slashes!
* Create a "sandbox" folder for output you generate by running MoDX Jupyter notebooks. This folder must be in a location to which you have write priveleges, and can have a name of your own chosing.
* * __mkdir _S:/my_modx_output_dir_ __ 

## Launching Jupyter Notbooks

To launch any of the MoDX Jupyter notebooks, perform the following steps:
* From the Windows Start Menu, select Anaconda3 (64 bit) > Jupyter Notebook (modx_p1d0_envt)
* This will take a few minutes to run; when complete a new tab will open in your default web browser
* The tab will display a 'file browser' view of the directory into which you cloned the MoDX GitHub repository

## Running a MoDX Jupyter Notebook

To launch a particular MoDX Jupyter notebook, perform the following steps:
* In the 'file browser' tab created in your web browser in the previous step, navigate to the folder containing the Jupyter notebook you want to run
* Click on the name of the notebook you wish to run
* In a few moments, the notebook will launch in a _new_ tab in your web browser
* __TO BE CONTINUED__

## Shutting Down a MoDX Jupyter Notebook 

To shut down a particular Jupyter notebook, perform the following steps:
* In your web browser, navigate to the tab with the 'file system view' of your MoDX directory
* Scroll to the top of this page
* Click on the __Running__ tab
* A list of your running Jupyter notbeooks will be displayed
* Navigate to the row listing the notebook you want to shut down
* Click on the orange __Stop Kernel__ button __>>>*** CHECK THIS ***<<<__
* Wait a few moments for the kernel running your notebook to be shut down
* When it has shut down, feel free to navigate back to the __TBD__ tab in the 'file browser' view
* In your web browser, switch to the tab in which your notebook was running
* Click the __x__ button on the browser tab to close the tab
* When prompted to stay on the page or leave it, select __leave__  __>>>*** CHECK THIS ***<<<__

## Shutting Down Jupyter Notebooks

To shut down Jupyter notebooks completely, perform the following steps:
* __TBD__
* __TBD__
* __TBD__