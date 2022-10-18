
'''
initial var
tor=0.001 #margin of error
width = 100
length = 173.205
if some error point to max(),may be you should double click the Part-1-1 in assembly model
edge nodesets include ABPE four points' nodes and LRUD four edges' nodes
'''
from abaqus import *
from abaqusConstants import *
import load

def LiPBC(ModelName):
    mymodel=mdb.models[ModelName]
    myparts=mdb.models[ModelName].parts['Part-1']
    myrootAssembly = mymodel.rootAssembly
    myinstances=myrootAssembly.instances['Part-1-1']

    x=[]
    y=[]
    j=0
    A=[]
    B=[]
    E=[]
    P=[]
    L=[]
    R=[]
    U=[]
    D=[]
    meshsens=1e-7# error allowed
    Nodeset=mdb.models[ModelName].rootAssembly.instances['Part-1-1'].nodes

    # find boundary nodes'label
    for i in Nodeset:
        x.insert(j,i.coordinates[0])
        y.insert(j,i.coordinates[1])
        j=j+1

    Max=max(x)
    May=max(y)
    Mnx=min(x)
    Mny=min(y)
    for i in Nodeset:
        if (Mnx+meshsens) < i.coordinates[0] < (Max-meshsens) and (Mny+meshsens) < i.coordinates[1] < (May-meshsens):
            continue
        if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-May)<=meshsens:
            E.insert(0,i.label)
        if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-May)<=meshsens:
            B.insert(0,i.label)
        if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens:
            P.insert(0,i.label)
        if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens:
            A.insert(0,i.label)
        if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens:
            R.append(i.label)
        if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens:
            L.append(i.label) 
        if abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
            U.append(i.label)
        if abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
            D.append(i.label)

    # creat ABAQUS sets
    myparts.SetFromNodeLabels(name='E',nodeLabels=(E))
    myparts.SetFromNodeLabels(name='B',nodeLabels=(B))
    myparts.SetFromNodeLabels(name='P',nodeLabels=(P))
    myparts.SetFromNodeLabels(name='A',nodeLabels=(A))
    myparts.SetFromNodeLabels(name='R',nodeLabels=(R))
    myparts.SetFromNodeLabels(name='L',nodeLabels=(L))
    myparts.SetFromNodeLabels(name='U',nodeLabels=(U))
    myparts.SetFromNodeLabels(name='D',nodeLabels=(D))



    #node sets
        #left wall
    a=[]
    for i in myparts.sets['L'].nodes:
            a=a+[(i.coordinates[1],i.label)]
    a.sort()
    rep=1
    for i in a:
            myparts.Set(name='L-'+str(rep), nodes=
                myparts.nodes[(i[1]-1):(i[1])])
            rep=rep+1
    print('\n the set L sort finished.set number=%s.^_^' %rep)


        #node sets
        #right wall
    a=[]
    for i in myparts.sets['R'].nodes:
            a=a+[(i.coordinates[1],i.label)]
    a.sort()
    rep=1
    for i in a:
            myparts.Set(name='R-'+str(rep), nodes=
                myparts.nodes[(i[1]-1):(i[1])])
            rep=rep+1
    print('\n the set R sort finished.set number=%s.^_^' %rep)        

       #node sets
        #up wall
    a=[]
    for i in myparts.sets['U'].nodes:
            a=a+[(i.coordinates[0],i.label)]
    a.sort()
    rep=1
    for i in a:
            myparts.Set(name='U-'+str(rep), nodes=
                myparts.nodes[(i[1]-1):(i[1])])
            rep=rep+1
    print('\n the set U sort finished.set number=%s.^_^' %rep)

        #node sets
        #down wall
    a=[]
    for i in myparts.sets['D'].nodes:
            a=a+[(i.coordinates[0],i.label)]
    a.sort()
    rep=1
    for i in a:
            myparts.Set(name='D-'+str(rep), nodes=
                myparts.nodes[(i[1]-1):(i[1])])
            rep=rep+1
    print('\n the set D sort finished.set number=%s.^_^' %rep)

        #constraints left and right
    Num=[0,0]
    Num[0]=len(myparts.sets['L'].nodes)
    Num[1]=len(myparts.sets['R'].nodes)
    if Num[0]!=Num[1]:
        print("\n the number of the nodes not equal!!! LEFT=%s;RIGHT=%s" %(Num[0],Num[1]))
    else:    
        print("\n nodes number equal. ^_^ left=right=%s" %Num[0])
        rep=1
        for i in range(0,Num[0]):
         mdb.models[ModelName].Equation(name='LRx-'+str(i+1), 
           terms=((-1.0, 'Part-1-1.L-'+str(rep), 1),(1.0, 'Part-1-1.R-'+str(rep), 1),(-1.0,'Part-1-1.P',1)))
         mdb.models[ModelName].Equation(name='LRy-'+str(i+1), 
           terms=((-1.0, 'Part-1-1.L-'+str(rep), 2),(1.0, 'Part-1-1.R-'+str(rep), 2),(-1.0,'Part-1-1.P',2)))
         rep=1+rep
        mdb.models[ModelName].Equation(name='Ex',terms=((1.0,'Part-1-1.E',1),(-1.0,'Part-1-1.B',1),(-1.0,'Part-1-1.P',1)))
        print("\n the constraints left and right finished. ^_^ left=right=%s" %Num[0])
        
        #constraints up and down
    Num=[0,0]
    Num[0]=len(myparts.sets['U'].nodes)
    Num[1]=len(myparts.sets['D'].nodes)
    if Num[0]!=Num[1]:
        print("\n the number of the nodes not equal!!! UP=%s;down=%s" %(Num[0],Num[1]))
    else:    
        print("\n nodes number equal. ^_^ up=down=%s" %Num[0])
        rep=1
        for i in range(0,Num[0]):
         mdb.models[ModelName].Equation(name='UDx-'+str(i+1), 
           terms=((1.0, 'Part-1-1.U-'+str(rep), 1),(-1.0, 'Part-1-1.D-'+str(rep), 1),(-1.0,'Part-1-1.B',1)))
         mdb.models[ModelName].Equation(name='UDy-'+str(i+1), 
           terms=((1.0, 'Part-1-1.U-'+str(rep), 2),(-1.0, 'Part-1-1.D-'+str(rep), 2),(-1.0,'Part-1-1.B',2)))
         rep=1+rep
        mdb.models[ModelName].Equation(name='Ey',terms=((1.0,'Part-1-1.E',2),(-1.0,'Part-1-1.P',2),(-1.0,'Part-1-1.B',2)))
        print("\n the constraints up and down finished. ^_^ left=right=%s" %Num[0])

        #creat analysis step
    mymodel.StaticStep(name='Step-1', previous='Initial', 
        maxNumInc=1000, initialInc=0.001, minInc=1e-12, maxInc=0.1)
    mymodel.fieldOutputRequests['F-Output-1'].setValues(variables=(
        'S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
        'VVF', 'VVFG', 'VVFN'))
    print("\n The analysis step finish SUCCESS.")    
        
        
        #load step
    regionA=myinstances.sets['A']
    regionB=myinstances.sets['B']
    regionP=myinstances.sets['P']
    mymodel.DisplacementBC(name='BC-1', createStepName='Initial', 
        region=regionA, u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    mymodel.DisplacementBC(name='BC-2', createStepName='Initial', 
        region=regionB, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    mymodel.DisplacementBC(name='BC-3', createStepName='Initial', 
        region=regionP, u1=UNSET, u2=SET, ur3=UNSET, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)  
    mymodel.DisplacementBC(name='BC-4', createStepName='Step-1', 
        region=regionP, u1=30, u2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    print("\n The Load step finish SUCCESS.") 
    '''
    after this you should change all elements type to plane strain!!!
    then run the analysis
    '''