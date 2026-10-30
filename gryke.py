import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator)
from matplotlib.patches import Ellipse

def points_distance(point1,point2):
    """
    Parameters
    ----------
    points1: array-like object with the (x,y) coordinates of a point
    points2: array-like object with the (x,y) coordinates of another point
    x and y should be in the same units and within the same reference frame
    
    Returns
    -------
    The distance between point1 and point2 in the units given.
    """
    d=((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)**0.5
    return d

def profile_building(X,Y):
    """
    Parameters
    ----------
    X: 1D array with the x coordinates of a set of points
    Y: 1D array with the y coordinates of a set of points
    both of the same length.
    
    Returns
    -------
    1D array of the same length where each element is the 
    distance between the first point and each point of the coordinate set
    """
    
    x1=X[0] ; y1=Y[0] ; profile_points=[]
    
    i=0
    for x in X:
        profile_points.append(((x-x1)**2+(Y[i]-y1)**2)**0.5)
        i=i+1
        
    profile_points=np.asarray(profile_points)
    
    return profile_points

def shoelace (points):
    """
    Parameters
    ----------
    points: array-like object formed by tuples/lists of [x,y] pairs of values 
    that define a polygon, ordered clockwise. x and y should be in the same
    units.
    
    Returns
    ----------
    The area of the polygon, in the square units of x and y
    """
    
    term1=0 ; term3=0
    
    for i in range (len(points)-1):
        term1=term1+points[i][0]*points[i+1][1]
        term3=term3+points[i+1][0]*points[i][1]
            
    term2=points[len(points)-1][0]*points[0][1]
    term4=points[0][0]*points[len(points)-1][1]  
   
    return (0.5*abs(term1+term2-term3-term4))
  
def gryke(ID,tip1,angle1,tip2,angle2,graben_depth,regional1,regional2,LNB):
    """
    Parameters
    -----------------------
    ID: a str identifying the investigated structure. This is not used in gryke
    but in the model builder function dike_model_section.
    
    Then, for the left-hand side fault:
    tip1 : (x,y) , ints/floats in m, the fault tip position
    angle1 : int/float between 0-90,
    
    for the right-hand side fault:
    tip2 : (x,y), ints/floats in m, the fault tip position
    angle2 : int/float between 0-90,   
    
    graben_depth : int/float in m, the elevation of the observed graben floor,    
    
    and two points to define the regional level:
        regional1 : (x,y), ints/floats in m for a point to the left
        regional2 : (x,y), ints/floats in m for a point to the right,
    
    LNB: int/float, positive depth in m of the Level of Neutral Buoyancy, measured
    below the regional level (the same reference as d below). The dike is assumed
    to be centred on the LNB, so its height is dh = 2*(LNB-d).

    The left-hand fault (tip1) must be to the left of the right-hand fault (tip2),
    and both faults are assumed to dip towards the graben centre.

    Returns
    -----------------------
    A tuple of 21 values, in this order (index in brackets):

    [0]  graben_area : area lost by the graben between the regional level and the
         graben floor, in m2
    [1]  gw : graben width in m, between the two fault tips
    [2]  gd : graben depth in m, between the mid point elevation of the regional
         and the graben floor
    [3]  d : depth of the dike tip below the mid point of the regional, in m
    [4]  (dx,dy) : x of the mid point of the graben floor, and elevation of the
         dike tip relative to datum, in m. These are the coordinates of the dike tip
    [5]  dw : dike width (aperture) in m, equal to the sum of the fault heaves
    [6]  dh : dike height in m
    [7]  lower_intersections : list of two (x,y) tuples in m, the intersections of
         the faults with the graben floor
    [8]  lower_boundaries : list of two (x,y) tuples in m, the points down to which
         the faults are plotted, at the depth of the dike tip (dy)
    [9]  fi : (x,y) intersection point of the two faults at depth
    [10] lb_f1 : length in m of buried fault 1, from the graben floor to its lower boundary
    [11] lb_f2 : length in m of buried fault 2, from the graben floor to its lower boundary
    [12] l_f1 : full length in m of fault 1, from its tip to its lower boundary
    [13] l_f2 : full length in m of fault 2, from its tip to its lower boundary
    [14] heave of fault 1 in m
    [15] heave of fault 2 in m
    [16] slip of fault 1 in m
    [17] slip of fault 2 in m
    [18] throw of fault 1 in m
    [19] throw of fault 2 in m
    [20] d_below_graben : depth of the dike tip below the graben floor, in m

    Fault 1 is the left-hand fault and fault 2 the right-hand fault.
    Values are not rounded.
    """

    # Check the input geometry before calculating.
    for angle in (angle1,angle2):
        if not 0<angle<90:
            raise ValueError(str(ID)+': fault angles must be greater than 0 and lower than 90 degrees, got '+str(angle))
    if not tip1[0]<tip2[0]:
        raise ValueError(str(ID)+': tip1 (left-hand fault) must have a lower x than tip2 (right-hand fault)')
    if LNB<=0:
        raise ValueError(str(ID)+': LNB must be given as a positive depth in m')

    # Calculate the intersection between the faults and the graben floor based
    # on the fault tips, fault angle, and graben depth. Then store the intersections.
    tips=(tip1,tip2) ; angles=(angle1,angle2)
    
    all_intersections=[] ; lower_intersections=[] ; throws=[] ; heaves=[]
    
    i=0
    for tip,angle in zip(tips,angles):
        x2=(((graben_depth-tip[1])/(np.cos(np.radians(90-angle))))**2-(graben_depth-tip[1])**2)**0.5+tip[0]
        
        # Calculating the right x2 value for the second fault.
        if i==1:
            x2=tip[0]-abs(tip[0]-x2)
        
        y2=graben_depth
        
        throws.append(abs(graben_depth-tip[1]))
        heaves.append(abs(x2-tip[0]))
        
        lower_intersections.append((x2,y2))
        all_intersections.append((x2,y2))
        i=i+1
            
    # Create lines that define the faults through the upper tips and lower intersections.
    fault1=np.polyfit((tip1[0],lower_intersections[0][0]),(tip1[1],lower_intersections[0][1]),1)
    fault2=np.polyfit((tip2[0],lower_intersections[1][0]),(tip2[1],lower_intersections[1][1]),1)
    
    # Find the intersections of the faults with the regional line. Then store these.
    # Here the second fault is calculated first for the all_intersections list to be 
    # in the right order for the shoelace formula.
    upper_intersections=[]
    regional=np.polyfit((regional1[0],regional2[0]), (regional1[1],regional2[1]),1)
    for fault in (fault2,fault1):
        x3=(fault[1]-regional[1])/(regional[0]-fault[0])
        regional_usable=np.poly1d(regional)
        y3=regional_usable(x3)
        upper_intersections.append((x3,y3))
        all_intersections.append((x3,y3))
    
    # Calculate the lost area with all the previous intersections.
    graben_area=shoelace(all_intersections)
    
    # Performing the area balance
    gw=abs(tip2[0]-tip1[0])
    d1=abs(lower_intersections[0][0]-tip1[0])
    d2=abs(lower_intersections[1][0]-tip2[0])
    dw=d1+d2
    d=graben_area/dw
    regional_mid_elevation=np.average([regional1[1],regional2[1]])
    dy=regional_mid_elevation-d
    d=abs(dy-regional_mid_elevation)
    gd=abs(graben_depth-regional_mid_elevation)
    d_below_graben=d-gd
    dx=np.average((lower_intersections[1][0],lower_intersections[0][0]))
    dh=(LNB-d)*2
    
    # Calculating the depth coordinates to which to plot the faults (the y coordinate is dy),
    # fault lengths from the lower intersections to that depth, and their intersection point. 
    # The coordinates of the depths to which the faults are plotted are the lower_boundaries. 
    # Finally, the full fault lengths from the tip to the lower boundary are calculated.
    fault1_inverse=np.polyfit((tip1[1],lower_intersections[0][1]),(tip1[0],lower_intersections[0][0]),1)
    fault2_inverse=np.polyfit((tip2[1],lower_intersections[1][1]),(tip2[0],lower_intersections[1][0]),1)
    
    fault1_inverse_poly1d=np.poly1d(fault1_inverse) ; fault2_inverse_poly1d=np.poly1d(fault2_inverse)
        
    f1_low_bound_x=fault1_inverse_poly1d(dy) ; f2_low_bound_x=fault2_inverse_poly1d(dy)
    
    lower_boundaries=[(f1_low_bound_x,dy),(f2_low_bound_x,dy)]

    faults_intersection_x=(fault1[1]-fault2[1])/(fault2[0]-fault1[0])
    fault1_poly1d=np.poly1d(fault1)
    faults_intersection_y=fault1_poly1d(faults_intersection_x)
    fi=(faults_intersection_x,faults_intersection_y)
    
    lb_f1=points_distance(lower_boundaries[0],lower_intersections[0])
    lb_f2=points_distance(lower_boundaries[1],lower_intersections[1])
    
    l_f1=points_distance(lower_boundaries[0],tip1)
    l_f2=points_distance(lower_boundaries[1],tip2)
    
    slips=(l_f1-lb_f1,l_f2-lb_f2) 
    
    return graben_area,gw,gd,d,(dx,dy),dw,dh,lower_intersections,lower_boundaries,fi,lb_f1,lb_f2,l_f1,l_f2,heaves[0],heaves[1],slips[0],slips[1],throws[0],throws[1],d_below_graben

def dike_model_section(topography,inputs,gryke_results,xlims=None,ylims=(-10000,0),
                       xticks=(1000,5000),yticks=(500,1000),legend_section=-1,legend_loc='lower left',
                       directions=('SW','NE'),save_dir=None,save_format='svg',show=True):
    """
    Parameters
    -----------------------
    Takes, for multiple cross sections,
    topography : the topography of each section as a 3D array of the x,y,z values,
    inputs : the gryke input parameters of each section, as given to gryke,
    gryke_results : the results of the gryke function for each section.

    Note: Each of these is a list of lists, list of arrays, array
    of arrays, or analogue data structure. e.g.: topography is
    a list of two 3D arrays containing the topography for two
    topographic profiles. Additionaly, the profiles, inputs, and
    outputs, need all to be in the same order.

    Optional plot settings, which may be changed depending on the scale of investigation:
    xlims : (min,max) of the x axis in m. None lets matplotlib choose.
    ylims : (min,max) of the y axis in m. None lets matplotlib choose.
    xticks : (minor,major) tick spacing of the x axis in m.
    yticks : (minor,major) tick spacing of the y axis in m.
    legend_section : index of the section in which to plot the legend (-1 is the
        last one). None for no legend.
    legend_loc : location of the legend, as in matplotlib (e.g. 'lower left', 'best').
        'best' avoids the plotted lines but not the inset with the model parameters.
    directions : (left,right) labels for the ends of the sections, e.g. ('SW','NE').
        None for no labels.
    save_dir : folder in which to save each figure. None to not save them.
    save_format : file format of the saved figures, e.g. 'svg', 'png', 'pdf'.
    show : whether to show each figure with plt.show().

    Returns
    -----------------------
    A list with the matplotlib figures of the given topographic profiles, with
    the title indicating the investigated section with the provided identifier,
    and numbering it in the sequence of all topographic profiles given. The legend
    is placed in the section chosen with legend_section, and shows all the elements
    modeled. The dike is represented at depth.

    An inset shows three relevant model parameters:
    d_dg : Depth of dike below the graben floor
    A : dike aperture
    H : dike height
    """

    n_sections=min(len(topography),len(inputs),len(gryke_results))
    if not len(topography)==len(inputs)==len(gryke_results):
        print('Warning: '+str(len(topography))+' topographic profiles, '+str(len(inputs))+' input sets and '
              +str(len(gryke_results))+' results were given. Only the first '+str(n_sections)+' sections are plotted.')
    if legend_section is not None and legend_section<0:
        legend_section=n_sections+legend_section
    if save_dir is not None:
        os.makedirs(save_dir,exist_ok=True)

    figures=[]
    i=1
    for profile,inp,results in zip(topography,inputs,gryke_results):

        i=i+1
        section=plt.figure(figsize=(7,5))
        ax=section.add_subplot(111)
        ax.set_title(str(inp[0])+' - Section '+str(i-1),fontsize=16)
        ax.plot(profile_building(profile[0],profile[1]),profile[2],marker='o',markersize=4,color='black',ls='-',lw=1, label='Topography')
        ax.set_ylabel('Elevation (m)',fontsize=16)
        ax.set_xlabel('Distance along profile (m)',fontsize=16)
        ax.grid(which='major',alpha=0.5)
        ax.grid(which='minor',alpha=0.2)
        
        # The axis locators and limits are set with the optional plot settings.
        ax.xaxis.set_major_locator(MultipleLocator(xticks[1]))
        ax.xaxis.set_minor_locator(MultipleLocator(xticks[0]))

        ax.yaxis.set_major_locator(MultipleLocator(yticks[1]))
        ax.yaxis.set_minor_locator(MultipleLocator(yticks[0]))

        if ylims is not None:
            ax.set_ylim(ylims[0],ylims[1])
        if xlims is not None:
            ax.set_xlim(xlims[0],xlims[1])
        
        # Plotting the regional line.
        ax.plot((inp[6][0],inp[7][0]),(inp[6][1],inp[7][1]),color='black',ls='--',lw=0.8, label='Regional level')
    
        # Plotting the graben floor.
        ax.plot((results[7][0][0],results[7][1][0]),(results[7][0][1],results[7][1][1]),color='blue',ls='-',lw=2, label='Assumed graben floor')
            
        # Plotting the faults to the graben floor.
        ax.plot((inp[1][0],results[7][0][0]),(inp[1][1],results[7][0][1]),color='sienna',ls='-',lw=2,zorder=0, label='Exposed fault trace')
        ax.plot((inp[3][0],results[7][1][0]),(inp[3][1],results[7][1][1]),color='sienna',ls='-',lw=2,zorder=0)
        
        # Plotting the faults below the graben floor.
        ax.plot((results[7][0][0],results[8][0][0]),(results[7][0][1],results[8][0][1]),color='sienna',ls='--',lw=2,zorder=0, label='Buried fault trace')
        ax.plot((results[7][1][0],results[8][1][0]),(results[7][1][1],results[8][1][1]),color='sienna',ls='--',lw=2,zorder=0)
        
        # Plotting the calculated detachment depth and a sketch of the dyke.   
        ax.scatter(results[4][0],results[4][1],color='red',edgecolor='black',marker='o',s=50, label='Upper dike tip')
        dyke=Ellipse((results[4][0],results[4][1]-results[6]/2),results[5],results[6], facecolor='red',edgecolor='black',alpha=0.5,lw=1,zorder=0, label='Dike representation')
        ax.add_patch(dyke)

        if directions is not None:
            ax.annotate(directions[0],(0.01,0.955),xycoords='axes fraction')
            ax.annotate(directions[1],(0.99,0.955),xycoords='axes fraction',ha='right')

        # Modify coordinates to adjust the position of the inset.
        ax.annotate(r'd$_{dg}$: '+str(round(results[-1],1))+' m\nA: '+str(round(results[5],1))+' m\nH: '+str(round(results[6]/1000,1))+' km',
                    (0.77,0.04),xycoords='axes fraction',bbox=dict(boxstyle="round", fc="white", ec="black", lw=1), fontsize=13)
        
        # The legend is plotted in the section chosen with legend_section (by default the last one).
        if legend_section is not None and (i-2)==legend_section:
            ax.legend(loc=legend_loc,edgecolor='black',fontsize=11)

        # Saving each figure produced in save_dir, if given.
        if save_dir is not None:
            safe_id=''.join(c if c.isalnum() or c in '-_.' else '_' for c in str(inp[0]))
            section.savefig(os.path.join(save_dir,'Section_'+str(i-1)+'_'+safe_id+'.'+save_format),dpi=600,format=save_format,bbox_inches='tight')

        figures.append(section)
        if show:
            plt.show()

    return figures
