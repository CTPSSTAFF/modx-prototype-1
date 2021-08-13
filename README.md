# modx-prototype-1
Model Data Explorer Prototype #1

## Ojbectives

* Make Travel Demand Model (TDM) input and output data accessible to users without requiring access to a TransCAD machine or SW license
* * Reduce contention for TransCAD machines
* * Make model data more easily accessible to modelers
* * Make model data accessible to non-modelers
* Leverage broader set of non-TransCAD skills to develop model reports and summaries

## Requirements

* All data in an open, standards-compliant format
* * OMX, CSV, SHP, JSON, GeoJSON, etc.
* * Export data in proprietary format to one of the above formats
* Open-source implementation 
* * Enables MoDX to be “run anywhere, by anyone”
* * Exploration of model data doesn’t require SW license ($$$)
* * Leverage open source community expertise in analysis, visualization, etc.

## Implementation - Choice of Platform
* Two principal candidates
* * R / RStudio
* * Python / Jupyter Notebooks
* R / RStudio
* * Looked promising at first, but...
* * Obstacles: R OMX library issues, RAM consumption
* * Python / Jupyter Notebooks
* * Python OMX library worked “out of the box”
* * RAM consumption issues manageable
* __Python / Jupyter Notebooks__ selected as implementation platform.
