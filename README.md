gryke is composed of a series of .py files, each of which are described below.

The calculations applied by gryke are explained in detail in the paper 'Subsurface Geometry and Emplacement Conditions of a Giant Dike System in Elysium Fossae, Mars' (https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2020JE006512).

# Quick start
gryke needs Python 3 with numpy and matplotlib, which can be installed with:

```
pip install -r requirements.txt
```

Then, running

```
python gryke_run.py
```

runs gryke on the example files included here, prints the results for each profile, and plots each modeled cross section. To run your own data, edit the inputs block at the top of gryke_run.py.

# gryke.py
A set of functions which applies the classic structural geology concept of area balance (Chamberlin, 1909) to model the geometry of a dike underneath a long linear graben. The core function, gryke, returns a series of dike and fault parameters which allow to model the subsurface geometry of the intrusion in a cross section orthogonal to the investigated graben, through the helper function dike_model_section. The docstring of gryke lists all the returned parameters, in order.

dike_model_section plots the modeled cross sections. Its optional settings control the axis limits and ticks, the section in which the legend is plotted, the direction labels at the ends of the sections, and whether and where the figures are saved.

# gryke_import_prep_routine.py
Functions to import the data and prepare it for gryke, and to run gryke:
- prepare_topography reads one or more topography files and separates them into profiles by their profile ID. The header and footer skips used by previous versions are still supported.
- prepare_input_files reads one or more input files and, when given the profile IDs from prepare_topography, matches each input to its topographic profile by name.
- run_gryke runs gryke for every profile.

# gryke_reporting.py
Prints a summary of the main results for each profile.

# gryke_run.py
The script to edit and run. It defines the input files and plot settings, and calls the functions above in order.

# gryke_2D_section_example.csv
An example on how the topography, cross section, or horizon data should be formatted. In my case, each block of rows with the same ID in this file represent the X, Y and Z coordinates of a topographic profile, below which I wanted to model the dikes. However, this file may contain data for the topology of subsurface 2D horizons, or any analogue data that comes to mind. The profile ID must be in the second column, and X, Y and Z in the third, fourth and fifth columns.

# Gryke_Input_Example.csv
An example on how the input data for gryke should be formatted. In my case, each of the rows represents the input data to model dikes below each one of the topographic profiles contained in the file above. The names in the first column must match the profile IDs in the topography file.

For running gryke, these two last files are not needed in tandem. For each dataset that one wants to model, an analogue Gryke_Input_Example.csv file is required. If one also wants to plot the data in a cross section, then an analogue gryke_2D_section_example.csv file is also needed. All files should be .csv files separated by ;.
