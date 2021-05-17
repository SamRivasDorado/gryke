gryke is composed of a series of .py files, each of which are described below.

# gryke.py
A set of functions which applies the classic structural geology concept of area balance (Chamberlin, 1909) to model the geometry of a dike underneath a long linear graben. The core function, gryke, returns a series of dike and fault parameters which allow to model the subsurface geometry of the intrusion in a cross section orthogonal to the investigated graben, through the helper function dike_model_section.

The calculations applied by the gryke core function are explained in detail in the paper 'Subsurface Geometry and Emplacement Conditions of a Giant Dike System in Elysium Fossae, Mars' (https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2020JE006512).

# gryke_import_prep_routine.py
A short script to import data, prepare it for gryke, running gryke, and optionally, plot the model results in a cross section.

# gryke_2D_section_example.csv
An example on how the topography, cross section, or horizon data should be formatted. In my case, each block of rows with the same ID in this file represent the X, Y and Z coordinates of a topographic profile, below which I wanted to model the dikes. However, this file may contain data for the topology of subsurface 2D horizons, or any 
analogue data that comes to mind. 

# gryke_input_example.csv
An example on how the input data for gryke should be formatted. In my case, each of the rows represents the input data to model dikes below each one of the topographic
profiles contained in the file above. 

For running gryke, these two last files are not needed in tandem. For each dataset that one wants to model, an analogue gryke_input.csv file is required. If one also wants to plot the data in a cross section, then an analogue gryke_2D_section.csv file is also needed. The script in gryke_import_prep_routine may be used with the desired input data to run and possibly plot the output. Preferably, all the files must be in the same folder, for ease of use. 
