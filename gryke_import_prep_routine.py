import numpy as np
from gryke import gryke                                             # The gryke.py file must be in the same folder as this file
from gryke_1 import dike_model_section                              # All the files called below must be in the same folder as this file.
                                                                    # Alternatively, the paths of each file may be provided.
                                                                    # Preferably, all the files should be .csv files separated by ;

########################### Preparing the 2D data ###########################
    
files=['TopoFile1','TopoFile2','TopoFilen']                         # Write here the name of the files which contain the 2D geometry of the investigated horizons.
                                                                    # Each should be in the same format as the provided Gryke_2D_section_Example.csv file. It may 
                                                                    # contain the data for all the investigated cross sections, when only one horizon is investigated. 
                                                                    # This is how the example file is constructed. However, alternatively, each file may contain data 
                                                                    # for multiple horizons but for a single cross section.

skips=[(),()]                                                       # A list of two tuples. The first tuple contains the header_skips required for reading the data in the
                                                                    # files above. The second contains the footer_skips required for reading each of the files above.
                                                                    # For more info on header and footer skips check the genfromtxt documentation.

# Do not edit from here .... #

topo=[]                                                             # A list to store the geometry of all the studied profiles
labels=[]                                                           # A list to store the desired labels for the studied profiles

for skip,file in zip(skips,files):
    temporary_set=[]
    temporary_labels=[]
    for hskip,fskip in zip(skip[0],skip[-1]):
        x,y,z=np.genfromtxt(file,delimiter=';',usecols=(2,3,4),skip_header=hskip, skip_footer=fskip,unpack=True)
        label=np.genfromtxt(file,delimiter=';',usecols=(1),dtype=str,skip_header=hskip, skip_footer=fskip,unpack=True)
        array=np.array([x,y,z],dtype='float')
        temporary_set.append(array)    
        temporary_labels.append(label[0])     

    topo.append(temporary_set)
    labels.append(temporary_labels) 
    
# .... to here. #

########################### Preparing the input for gryke  ###########################

datasets=('LabelForTopoFile1','LabelForTopoFile2','LabelForTopoFilen')                        # The desired names to label the data in files.
files=('inputfile1','inputfile2','inputfilen')                                                # The files that contain the input parameters for gryke.
                                                                                              # It should follow the same structure as the example file
                                                                                              # Gryke_Input_Example.csv. This file contains 1 set of input
                                                                                              # values for each topographic profile in Gryke_2D_section_Example.csv
# Do not edit from here .... #

gryke_input=[] 
tracks=[]
n=[]

for element in topo:
    n.append(len(topo))


for n,file in zip(n,files):
    temporary_input=[]
    temporary_tracks=[]
    for i in range(1,n+1):
        Profile,tip1x,tip1y,angle1,tip2x,tip2y,angle2,graben_depth,regional1x,regional1y,regional2x,regional2y,LNB=np.genfromtxt(file,delimiter=';',skip_header=i,skip_footer=n-i,usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13),unpack=True)
        track=np.genfromtxt(file, delimiter=';',dtype='str',skip_header=i,skip_footer=n-i,usecols=(0),unpack=True)
        tip1=(tip1x,tip1y)
        tip2=(tip2x,tip2y)
        regional1=(regional1x,regional1y)
        regional2=(regional2x,regional2y)
        temporary_tracks.append(track)
        temporary_input.append((track,tip1,angle1,tip2,angle2,graben_depth,regional1,regional2,LNB))
        
    tracks.append(temporary_tracks)
    gryke_input.append(temporary_input)
    
# .... to here #
    
########################### Running gryke ###########################

gryke_results=[]                                        # A list to store the results of running gryke, separated by dataset

i=1
for data in gryke_input:
    temporary_results=[]
    for parameters in data:
        results=(gryke(parameters[0],parameters[1],parameters[2],parameters[3],parameters[4],parameters[5],parameters[6],parameters[7],parameters[8]))
        temporary_results.append(results)
        # file.write(str(i)+' '+str(results))
        # file.write('\n')
        # i=i+1
    gryke_results.append(temporary_results)


gryke_output=[]                                         # A list to store the results of running gryke, which contains each of the parameters separately

for i in range(len(gryke_results[0][0])):
    temp_list=[]
    for dataset in gryke_results:
        for profile in dataset:
            temp_list.append(profile[i])
    gryke_output.append(temp_list)
 
########################### Uncomment below for plotting the results for all datasets ###########################

# for topo,inputs,results in zip(topo,gryke_input,gryke_results):
#     dike_model_section(topo, inputs, results)
