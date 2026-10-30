
def gryke_reporting(gryke_results,labels):
    """
    Prints a summary of the main gryke results for each profile.

    Parameters
    ----------
    gryke_results : a list with the results of gryke for each profile, as returned by run_gryke
    labels : a list with the name of each profile, in the same order
    """

    for result,label in zip(gryke_results,labels):
        print ('Results for '+ str(label))
        print ('-------------------------')
        print ( ' Graben area = ' + str(round(result[0],2))+ ' m2')
        print ( ' Graben width = ' + str(round(result[1],2))+ ' m')
        print ( ' Graben depth = ' + str(round(result[2],2))+ ' m')
        print ( ' Dike depth below regional midpoint = ' + str(round(result[3],2))+ ' m')
        print ( ' Dike depth below graben floor = ' + str(round(result[20],2))+ ' m')

        print ( ' Mid point of the graben floor = ' + str(round(result[4][0],2))+ ' m')
        print ( ' Dike tip elevation relative to datum = ' + str(round(result[4][1],2))+ ' m')

        print ( ' Dike aperture = ' + str(round(result[5],2))+ ' m')
        print ( ' Dike height = ' + str(round(result[6],2))+ ' m')

        print ('-------------------------')
        print ('\n')
