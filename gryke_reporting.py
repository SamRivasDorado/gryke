
def gryke_reporting(gryke_results,labels):
    
    for result,label in zip(gryke_results,labels):
        print ('Results for '+ str(label))
        print ('-------------------------')
        print ( ' Graben area (m2) = ' + str(round(result[0],2))+ ' m2')
        print ( ' Graben width (m) = ' + str(round(result[1],2))+ ' m')
        print ( ' Graben depth (m) = ' + str(round(result[2],2))+ ' m')
        print ( ' Dike depth below regional midpoint (m) = ' + str(round(result[3],2))+ ' m')
        
        print ( ' Mid point of the graben floor (m) = ' + str(round(result[4][0],2))+ ' m')
        print ( ' Dike depth relative to datum (m) = ' + str(round(result[4][1],2))+ ' m')
        
        print ( ' Dike aperture (m) = ' + str(round(result[5],2))+ ' m')
        print ( ' Dike height (m) = ' + str(round(result[6],2))+ ' m')

        print ('-------------------------')
        print ('\n')
        
    