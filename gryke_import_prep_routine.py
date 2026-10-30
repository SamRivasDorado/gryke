import numpy as np
from gryke import gryke                                             # The gryke.py file must be in the same folder as this file
from gryke import dike_model_section                              # All the files called below must be in the same folder as this file.
                                                                    # Alternatively, the paths of each file may be provided.
                                                                    # Preferably, all the files should be .csv files separated by ;

########################### Preparing the 2D data ###########################
    
def prepare_topography (files, skips):
    
    topo=[]                                                             # A list to store the geometry of all the studied profiles
    labels=[]                                                           # A list to store the desired labels for the studied profiles
    
    if len(files)==1:
        for hskip,fskip in zip(skips[0],skips[1]):
            x,y,z=np.genfromtxt(files[0],delimiter=';',usecols=(2,3,4),skip_header=hskip, skip_footer=fskip,unpack=True)
            label=np.genfromtxt(files[0],delimiter=';',usecols=(1),dtype=str,skip_header=hskip, skip_footer=fskip,unpack=True)
            array=np.array([x,y,z],dtype='float')
        
            topo.append(array)
            labels.append(label[0])
            
    return topo, labels
    
# .... to here. #

########################### Preparing the input for gryke  ###########################


def prepare_input_files (labels,input_file):
    
    gryke_input=[] 
    tracks=[]

    header_skips = np.arange(1,len(labels)+1)
    footer_skips = np.flip(np.arange(0,len(labels)))
    
    for hs,fs in zip(header_skips,footer_skips):
        
        tip1x,tip1y,angle1,tip2x,tip2y,angle2,graben_depth,regional1x,regional1y,regional2x,regional2y,LNB=np.genfromtxt(input_file,delimiter=';',skip_header=hs,skip_footer=fs,usecols=(1,2,3,4,5,6,7,8,9,10,11,12),unpack=True)
        track=np.genfromtxt(input_file, delimiter=';',dtype='str',skip_header=hs,skip_footer=fs,usecols=(0),unpack=True)
        tip1=(tip1x,tip1y)
        tip2=(tip2x,tip2y)
        regional1=(regional1x,regional1y)
        regional2=(regional2x,regional2y)
  
        tracks.append(track)
        gryke_input.append((track,tip1,angle1,tip2,angle2,graben_depth,regional1,regional2,LNB))
        
    return gryke_input
    
# .... to here #
    
########################### Running gryke ###########################

def run_gryke(gryke_input):

    # A list to store the results of running gryke, separated by dataset
    gryke_results=[]                                        
    
    i=1
    for i in range(len(gryke_input)):
        parameters = gryke_input[i]
        results=(gryke(parameters[0],parameters[1],parameters[2],parameters[3],parameters[4],parameters[5],parameters[6],parameters[7],parameters[8]))
        gryke_results.append(results)
        # file.write(str(i)+' '+str(results))
        # file.write('\n')
        # i=i+1
    
    # A list to store the results of running gryke, which contains each of the parameters separately as a single list
    gryke_output=[]                                        
     
    for i in range(0,len(gryke_results[0])):
        temp_result = []
        for j in range(0,len(gryke_results)):
            temp_result.append(gryke_results[j][i])
        
        gryke_output.append(temp_result)
        
    return gryke_results, gryke_output
 
########################### Uncomment below for plotting the results for all datasets ###########################

# for topo,inputs,results in zip(topo,gryke_input,gryke_results):
#     dike_model_section(topo, inputs, results)
