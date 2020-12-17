import numpy as np

def points_distance(point1,point2):
    d=((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)**0.5
    return d

def shoelace (points):
    'A list formed by lists of [x,y] pairs of values that define a polygon'
    'Applies the shoelace formula to calculate the area of the polygon'
    'Returns the are of the polygon'
    
    term1=0
    term3=0
    for i in range (len(points)-1):
        term1=term1+points[i][0]*points[i+1][1]
        term3=term3+points[i+1][0]*points[i][1]
            
    term2=points[len(points)-1][0]*points[0][1]
    term4=points[0][0]*points[len(points)-1][1]  
   
    return (0.5*abs(term1+term2-term3-term4))
  
def gryke(tip1,angle1,tip2,angle2,graben_depth,regional1,regional2,LNB):
    'For a given coordinate system takes, for the left-hand side fault:'
    'tip1 : (x,y),floats in m, the fault tip position'
    'angle1 : float between 0-90'
    
    'for the right-hand side fault:'
    'tip2 : (x,y),floats in m, the fault tip position'
    'angle2 : float between 0-90'    
    'the graben_depth : float in m, the elevation of the observed graben floor,'    
    'two points to define the regional level:'
    'regional1 : (x,y), floats in m for a point to the left'
    'regional2 : (x,y), floats in m for a point to the right,' 
    'Also takes a depth for the Level of Neutral Buoyancy LNB in m.'
    
    'Returns:'
    'gw : Graben width in m'
    'gd :  graben depth in m between the mid point elevation of the regional and the graben depth'
    'd : Depth of the dike below the midpoint of the regional'
    '(dx,dy) : mid point of the graben floor in m, depth of dike relative to datum in m'
    'dx and dy are the coordinates at which to place the dike tip'
    'dw : Dike width in m'
    'dh : Dike height in m'
    'lower_intersections = A list of two tuples with (x,y) coordinates in m which define the intersections of the faults with the graben base'
    'lower_boundaries: A list of two tuples with (x,y) coordinates in m which define the bottom depth to which to plot the faults, which is dy'
    'fi : intersection point of the faults at depth'
    'lb_f1, lb_f2 : length of the buried fault1 and fault 2 trace to the corresponding lower boundary'
    'l_f1, lb_f2 : length of the buried fault1 trace to the corresponding lower boundary'
    'heaves, '
    'total_slips, '
    'and throws, '
    'for the fault1 to the left-hand side, and fault2 to the right-hand side'
    'd_below_graben: dike depth below the graben floor in m'
    
    'All rounded to the second decimal'    

    'Define a line for the base of the graben'
    graben_base=np.polyfit((0,20000),(graben_depth,graben_depth),1)
    
    'Calculate the intersection between the faults and the graben floor based on the fault tips, fault angle, and graben depth.'
    'Store the intersections'
    tips=(tip1,tip2)
    angles=(angle1,angle2)
    
    all_intersections=[]
    
    lower_intersections=[]
    throws=[]
    heaves=[]
    
    i=0
    for tip,angle in zip(tips,angles):
        x2=(((graben_depth-tip[1])/(np.cos(np.radians(90-angle))))**2-(graben_depth-tip[1])**2)**0.5+tip[0]
        
        'To calculate the right x2 value for the second fault'
        if i==1:
            x2=tip[0]-abs(tip[0]-x2)
        
        y2=graben_depth
        
        throws.append(abs(graben_depth-tip[1]))
        heaves.append(abs(x2-tip[0]))
        
        lower_intersections.append((x2,y2))
        all_intersections.append((x2,y2))
        i=i+1
            
    'Create lines that define the faults with the upper tips and intersections'
    fault1=np.polyfit((tip1[0],lower_intersections[0][0]),(tip1[1],lower_intersections[0][1]),1)
    fault2=np.polyfit((tip2[0],lower_intersections[1][0]),(tip2[1],lower_intersections[1][1]),1)
    
    'Find the intersections of the faults with the regional line.Store the intersections'
    'Here the second fault is calculated first for the all_intersections list to be ready for the shoelace formula.'
    upper_intersections=[]
    regional=np.polyfit((regional1[0],regional2[0]), (regional1[1],regional2[1]),1)
    for fault in (fault2,fault1):
        x3=(fault[1]-regional[1])/(regional[0]-fault[0])
        regional_usable=np.poly1d(regional)
        y3=regional_usable(x3)
        upper_intersections.append((x3,y3))
        all_intersections.append((x3,y3))
    
    'Calculate the lost area with all the previous intersections.'    
    graben_area=shoelace(all_intersections)
    
    'Area-balance'
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
    
    'Calculating depth coordinates to which to plot the faults (the y coordinate is dy),'
    'fault lengths from the lower intersections to that depth, and their intersection point. The coordinates of the depths'
    'to which the faults are plotted are the -lower_boundaries-. Finally, the full fault lengths from the tip to the lower boundary'
    'are calculated as well'
    fault1_inverse=np.polyfit((tip1[1],lower_intersections[0][1]),(tip1[0],lower_intersections[0][0]),1)
    fault2_inverse=np.polyfit((tip2[1],lower_intersections[1][1]),(tip2[0],lower_intersections[1][0]),1)
    
    fault1_inverse_poly1d=np.poly1d(fault1_inverse)
    fault2_inverse_poly1d=np.poly1d(fault2_inverse)
        
    f1_low_bound_x=fault1_inverse_poly1d(dy)
    f2_low_bound_x=fault2_inverse_poly1d(dy)
    
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
    # 20 results