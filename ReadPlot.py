

#Function Accepts File Name and Event Number, Outputs Event Title and Data of called event
def dataRead(file_name, eventNum):
    import string
    file = open(file_name)
    cc = 0 #not needed, but hey, if it aint broke...
    while cc<1:
        line = file.readline()
        if not line:
            break
        cc=cc+1
    for c in string.punctuation:
        line = line.replace(c,"")
    line = string.lower(line)
    bb = line.rsplit() # bb is the Title line
    
    # skip to the eventNum asked for
    while int(bb[1])!=eventNum:
        for m in range(int(bb[3])+1):
            line = file.readline()
            if not line:
                break
        if not line:
            break
        for symbols in string.punctuation:
            line = line.replace(symbols,"")
        line = string.lower(line)
        bb = line.rsplit()
        
    #bb is the first line seperated into a tuple, bb(3) is the next how many points in the set
    M = int(bb[3])
    #M = 3
    N = 5
    DD = [[0]*N]*M
    w = ''
    for m in range(M):
        line = file.readline()
        if not line:
            break
        for c in string.punctuation:
            line = line.replace(c,"")
        line = string.lower(line)
        w = w+line
    r = w.rsplit()
    Volume=[]
    Row=[]
    Column=[]
    Bucket=[]
    ADC=[]
    for m in range(M):
        Volume.append(int(r[m*N]))
        Row.append(int(r[m*N+1]))
        Column.append(int(r[m*N+2]))
        Bucket.append(int(r[m*N+3]))
        ADC.append(int(r[m*N+4]))
    #bb is the title sequence info
    
    return bb, Volume, Row, Column, Bucket, ADC


def ReadHexAndCart(file_name, eventNum):
    [Title, Volume, Row, Column, Bucket, ADC] = dataRead(file_name, eventNum)
    M = int(Title[3])
    x = []
    y = []
    z = []
    for m in range(M):
        point = MapHexToCart(Volume[m], Row[m], Column[m], Bucket[m])
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    return Title, Volume, Row, Column, Bucket, ADC, x, y , z

import math
#import voxel as vox
#import SpacePoint as sp

def MapHexToCart(volume, column, row, bucket):
    
    """Map the indices to x,y,z coordinates for
    the NIFFTE detector geometry.
    """
    fA = 0.1 # (cm) parameter for hexagonal geometry
    fB = 2.0 * fA / math.sqrt(3.0) # (cm) parameter for hexagonal geometry
    fCenterX = 47.0 # (cm) offset to center of volume
    fCenterY = 61.0 # (cm) offset to center of volume

    # In this (r,c) coordinate system, the Hex at (0,1) is
    # down and to the right of (0,0).
    x = column * 1.5 * fB
    y = -row * 2.0 * fA + math.fabs((column+1) % 2 * fA)

    # Shift the row/col coordinate system so that x=y=0.0
    # is at the center of the row/col field
    x -= fCenterX * fB;
    y += fCenterY * fA;

    # Now work on z coordinate
    fDriftDistance = 5.4 # (cm) size of drift volume
    fClockRate = 50.0 # MHz
    fDriftSpeed = 5.2 # (cm/us) default value
    fNumberOfBuckets = int(fDriftDistance * fClockRate / fDriftSpeed) # number of buckets per volume
    z = (fDriftDistance - float(bucket) + 0.5) * fDriftDistance/fNumberOfBuckets

    if (volume == 0):
        z = -z
    if (volume == 1):
       x = -x

    return x,y,z


def PlotStuff(Title, x,y,z,ADC):
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    ss = int(Title[3])
    
    
    # Create Map
    cm = plt.get_cmap("RdYlGn")
    #col = np.arange(30)
    col = ADC
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #For connected points:
    #plt.plot(x,y,z)
#    for c, m in [('r', 'o')]:
#        xs = x
#        ys = y
#        zs = z
#        ax.scatter(xs,ys,zs, c=ADC, marker=m)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    
    p3d = ax.scatter(x, y, z, s=ss, c=col, marker='o')                                                                                

    plt.show()
    return None




# 3D Plot

#[Title, Volume, Row, Column, Bucket, ADC] = dataRead('Data_Sample.txt',3)

# x y and z are in cartesian
numeroEvento = input('Please specify which event (0-98) you would like to view: ')
[Title, Volume, Row, Column, Bucket, ADC, x, y , z] = ReadHexAndCart('Data_Sample.txt',numeroEvento)

PlotStuff(Title,x,y,z,ADC) #colorcoded by ADC value, will add title and Colorbar later
