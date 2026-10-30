import os
import sys

# The folder of this script, where all the gryke .py files should be.
gryke_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, gryke_folder)

from gryke_import_prep_routine import prepare_topography
from gryke_import_prep_routine import prepare_input_files
from gryke_import_prep_routine import run_gryke
from gryke_reporting import gryke_reporting
from gryke import dike_model_section


################# Define the following inputs as per the instructions below #################
# By default, this script runs the example files provided with gryke.

files=[os.path.join(gryke_folder,'gryke_2D_section_example.csv')]  # Write here the path of the files which contain the 2D geometry of the investigated horizons.
                                                                    # Each should be in the same format as the provided gryke_2D_section_example.csv file. It may
                                                                    # contain the data for all the investigated cross sections, when only one horizon is investigated.
                                                                    # This is how the example file is constructed.

skips=None                                                          # None (recommended) to separate the profiles in each file by their profile ID.
                                                                    # Alternatively, a tuple of two tuples per file: the first with the header_skips and the second
                                                                    # with the footer_skips required for reading each profile. For more info on header and footer
                                                                    # skips check the genfromtxt documentation.

input_files=[os.path.join(gryke_folder,'Gryke_Input_Example.csv')]  # The files that contain the input parameters for gryke.
                                                                    # They should follow the same structure as the example file Gryke_Input_Example.csv,
                                                                    # which contains 1 set of input values for each topographic profile in gryke_2D_section_example.csv.
                                                                    # The names in its first column must match the profile IDs of the topography files.

plot=True                                                           # Whether to plot the model sections.
save_dir=None                                                       # A folder in which to save the plotted sections, e.g. os.path.join(gryke_folder,'sections'). None to not save them.

# Plot settings, which may be changed depending on the scale of investigation.
xlims=(0,22000)                                                     # (min,max) of the x axis in m. None for automatic limits.
ylims=(-10000,0)                                                    # (min,max) of the y axis in m. None for automatic limits.
xticks=(1000,5000)                                                  # (minor,major) tick spacing of the x axis in m.
yticks=(500,1000)                                                   # (minor,major) tick spacing of the y axis in m.
directions=('SW','NE')                                              # Labels for the left and right ends of the sections. None for no labels.

#################


topo, labels = prepare_topography(files, skips)

gryke_input = prepare_input_files(input_files, labels)

gryke_results, gryke_output = run_gryke(gryke_input)

gryke_reporting(gryke_results, labels)

if plot:
    dike_model_section(topo, gryke_input, gryke_results, xlims=xlims, ylims=ylims, xticks=xticks, yticks=yticks,
                       directions=directions, save_dir=save_dir)
