import numpy as np
from gryke import gryke                                             # The gryke.py file must be in the same folder as this file.
                                                                    # All the data files may be given with their full paths.
                                                                    # All the data files should be .csv files separated by ;

########################### Preparing the 2D data ###########################

def prepare_topography (files, skips=None, header_rows=1):
    """
    Parameters
    ----------
    files : the path of a file, or a list of paths, containing the 2D geometry of
    the investigated horizons. Each should be in the same format as the provided
    gryke_2D_section_example.csv file: column 1 holds the profile ID, and columns
    2, 3 and 4 hold the X, Y and Z coordinates. Other columns are ignored.

    skips : None (recommended), to separate the profiles in each file by their
    profile ID, in the order in which they appear.
    Alternatively, the header and footer skips required to read each profile, as
    in previous versions. For a single file, a tuple of two tuples: the first
    with the header_skips and the second with the footer_skips of each profile.
    For several files, a list with one such tuple per file. For more info on
    header and footer skips check the genfromtxt documentation.

    header_rows : number of header rows at the top of each file, used when skips
    is None.

    Returns
    ----------
    topo : a list with one 3D array of the x,y,z values per profile
    labels : a list with the profile ID of each profile, in the same order
    """

    if isinstance(files,str):
        files=[files]

    topo=[]                                                         # A list to store the geometry of all the studied profiles
    labels=[]                                                       # A list to store the labels of the studied profiles

    if skips is None:
        for file in files:
            ids=np.atleast_1d(np.genfromtxt(file,delimiter=';',usecols=(1),dtype=str,skip_header=header_rows))
            xyz=np.atleast_2d(np.genfromtxt(file,delimiter=';',usecols=(2,3,4),skip_header=header_rows))
            for profile_id in dict.fromkeys(ids):                   # The unique IDs, in order of appearance
                topo.append(xyz[ids==profile_id].T.astype('float'))
                labels.append(str(profile_id))

    else:
        # A single (header_skips, footer_skips) pair is accepted for a single file.
        if np.isscalar(skips[0][0]):
            skips=[skips]
        if len(skips)!=len(files):
            raise ValueError('One (header_skips, footer_skips) pair is needed per file: '+str(len(files))+' files and '+str(len(skips))+' pairs were given.')

        for file,skip in zip(files,skips):
            for hskip,fskip in zip(skip[0],skip[1]):
                x,y,z=np.genfromtxt(file,delimiter=';',usecols=(2,3,4),skip_header=hskip, skip_footer=fskip,unpack=True)
                label=np.atleast_1d(np.genfromtxt(file,delimiter=';',usecols=(1),dtype=str,skip_header=hskip, skip_footer=fskip,unpack=True))
                array=np.array([x,y,z],dtype='float')

                topo.append(array)
                labels.append(str(label[0]))

    if len(topo)==0:
        raise ValueError('No topographic profiles were read from '+str(files)+'. Check the file paths and the skips.')

    return topo, labels


########################### Preparing the input for gryke  ###########################

def prepare_input_files (input_files, labels=None):
    """
    Parameters
    ----------
    input_files : the path of a file, or a list of paths, containing the input
    parameters for gryke. Each should follow the same structure as the example
    file Gryke_Input_Example.csv, with one header row and one row per profile:
    Name;Profile_number;tip1_x;tip1_y;angle1;tip2_x;tip2_y;angle2;graben_depth;
    regional1_x;regional1_y;regional2_x;regional2_y;LNB
    The Profile_number column is not used.

    labels : optional, the profile IDs returned by prepare_topography. If given,
    the inputs are returned in the same order as these labels, so that each
    input matches its topographic profile. An error is raised if a label has
    no input, and inputs without a label are left out with a warning.

    Returns
    ----------
    gryke_input : a list with one tuple of gryke parameters per profile:
    (Name, tip1, angle1, tip2, angle2, graben_depth, regional1, regional2, LNB)
    """

    if isinstance(input_files,str):
        input_files=[input_files]

    gryke_input=[]

    for input_file in input_files:
        names=np.atleast_1d(np.genfromtxt(input_file,delimiter=';',dtype=str,skip_header=1,usecols=(0)))
        values=np.atleast_2d(np.genfromtxt(input_file,delimiter=';',skip_header=1,usecols=(2,3,4,5,6,7,8,9,10,11,12,13)))

        for name,row in zip(names,values):
            tip1x,tip1y,angle1,tip2x,tip2y,angle2,graben_depth,regional1x,regional1y,regional2x,regional2y,LNB=row
            tip1=(tip1x,tip1y)
            tip2=(tip2x,tip2y)
            regional1=(regional1x,regional1y)
            regional2=(regional2x,regional2y)
            gryke_input.append((str(name),tip1,angle1,tip2,angle2,graben_depth,regional1,regional2,LNB))

    if labels is None:
        return gryke_input

    # Matching the inputs to the topographic profiles.
    names=[inp[0] for inp in gryke_input]
    duplicates=sorted(set(n for n in names if names.count(n)>1))
    if duplicates:
        raise ValueError('These names appear more than once in the input files: '+', '.join(duplicates))
    by_name=dict(zip(names,gryke_input))

    missing=[label for label in labels if label not in by_name]
    if missing:
        raise ValueError('These topographic profiles have no input parameters: '+', '.join(missing))
    extra=[name for name in names if name not in labels]
    if extra:
        print('Warning: these inputs have no topographic profile and are left out: '+', '.join(extra))

    return [by_name[label] for label in labels]


########################### Running gryke ###########################

def run_gryke(gryke_input):
    """
    Parameters
    ----------
    gryke_input : a list of tuples of gryke parameters, as returned by prepare_input_files

    Returns
    ----------
    gryke_results : a list with the results of gryke for each profile
    gryke_output : the same results organised by parameter, i.e. a list where each
    element holds the values of one of the gryke results for all the profiles
    """

    # A list to store the results of running gryke for each profile
    gryke_results=[]

    for parameters in gryke_input:
        gryke_results.append(gryke(*parameters))

    # A list to store the results of running gryke, which contains each of the parameters separately as a single list
    gryke_output=[]

    for i in range(0,len(gryke_results[0])):
        temp_result = []
        for j in range(0,len(gryke_results)):
            temp_result.append(gryke_results[j][i])

        gryke_output.append(temp_result)

    return gryke_results, gryke_output
