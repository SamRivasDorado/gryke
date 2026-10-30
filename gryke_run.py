import sys
sys.path.append (r'C:\Users\Samuel\iCloudDrive\Geology\Programs\Gryke')

from gryke_import_prep_routine import prepare_topography
from gryke_import_prep_routine import prepare_input_files
from gryke_import_prep_routine import run_gryke
from gryke import dike_model_section 


################# Define the following inputs as per the instructions below #################

files=['TopoFile1','TopoFile2','TopoFilen']                         # Write here the path of the files which contain the 2D geometry of the investigated horizons.
                                                                    # Each should be in the same format as the provided Gryke_2D_section_Example.csv file. It may 
                                                                    # contain the data for all the investigated cross sections, when only one horizon is investigated. 
                                                                    # This is how the example file is constructed. However, alternatively, each file may contain data 
                                                                    # for multiple horizons but for a single cross section.

skips=[(),()]                                                       # A list of two tuples. The first tuple contains the header_skips required for reading the data in the
                                                                    # files above. The second contains the footer_skips required for reading each of the files above.
                                                                    # For more info on header and footer skips check the genfromtxt documentation.


datasets=('LabelForTopoFile1','LabelForTopoFile2','LabelForTopoFilen')                        # The desired names to label the data in files.
input_files=('inputfile1','inputfile2','inputfilen')                                                # The files that contain the input parameters for gryke.
                                                                                              # It should follow the same structure as the example file
                                                                                              # Gryke_Input_Example.csv. This file contains 1 set of input  
                                                                                              
#################


topo, labels = prepare_topography (files, skips)

gryke_input = prepare_input_files(topo, input_files)

gryke_results, gryke_output = run_gryke(gryke_input)

dike_model_section(topo, gryke_input, gryke_results)

                                                                             