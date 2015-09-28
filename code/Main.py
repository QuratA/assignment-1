# the other one is functions

import math
from Functions import NumberOfCatigories, Gain, EntropyAllData, Node, isParent, CategoryEntropy, educationNumCategory, \
    fnlwgtCategory, AgeCategory, HoursCategory, median, LossCategory, GainCategory
import csv

# return True if i is an element of array
def belongTo( i, array):
    for j in array :
        if(i==j) :
            return True
    return False

# check if it's one class
def OneClass ( filename, Node, category):

    AllParents = Node.parents
    RowList= attributes[Node.name][category]


    if len(AllParents)==1:
        RowList= attributes[Node.name][category]
    else :
        for name in AllParents:
            if AllParents[name] != 'None':
                RowList = [val for val in RowList if val in attributes[name][AllParents[name]]]


    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        high=0
        less=0
        nbRow=0
        for row in csvreader:
            if belongTo(nbRow,RowList)==True  and (row[14].strip()== "<=50K"):
                high=high+1
            if belongTo(nbRow,RowList)==True  and (row[14].strip()== ">50K"):
                less=less+1
            nbRow=nbRow+1
        if (high !=0) and (less !=0):
            return False
        if high==0 :
            Class=">50K"
        if less==0 :
            Class="<=50K"

    return True,Class



#Build the decision Tree
def Main (filename, ParentNode, MapParentNode) :
        # repeat for all categories
        for category in MapParentNode :
            #check that the category is one class

            if OneClass(filename, ParentNode, category)==False:
                #compute the entropy
                categoryEntropy=CategoryEntropy(filename,ParentNode.name,category)
                # for all attributes not already in the tree
                gains= dict()
                for attribute in attributes:
                    if isParent(ParentNode,attribute)== False :
                        tmpMap={}
                        for key in (attributes[attribute]):
                            tmpMap[key]=[0,0]
                        # for each row of the file
                        with open(filename, 'rb') as csvfile:
                            csvreader = csv.reader(csvfile, delimiter=',')
                            for row in csvreader:
                                if row[ParentNode.name]== category :
                                    for key in tmpMap :
                                        if row[attribute] == key :
                                            if row[14] == ">50K":
                                                tmpMap[key][0]=tmpMap[key][0]+1
                                            else :
                                                tmpMap[key][1]=tmpMap[key][1]+1
                        # Gain
                        Entropy=0
                        for key in attributes[attribute] :
                            nb=tmpMap[key][0]+tmpMap[key][1]
                            if tmpMap[key][0] !=0  and tmpMap[key][1] !=0:
                                Entropy=Entropy+((tmpMap[key][0]/float(nb))*math.log(tmpMap[key][0]/float(nb),2) + (tmpMap[key][1]/float(nb))*math.log(tmpMap[key][1]/float(nb),2))*float(nb)/len(attributes[ParentNode.name][category])
                            else :
                                Entropy =0
                        gain= -categoryEntropy + Entropy
                        gains[attribute]=gain


                if(len(gains)!=0) :
                    # obtain the highest gain
                    att=-1
                    max_val = max(gains.itervalues())
                    for k, v in gains.iteritems() :
                        if v == max_val :
                            att=k

                    # Create the Node
                    NewNode= Node()
                    NewNode.name= att
                    # add parents
                    NewNode.parents= ParentNode.parents.copy()
                    NewNode.parents[ParentNode.name]= category
                    NewNode.parents[NewNode.name]='None'

                    # Add the node as a child of parent Node
                    ParentNode.children[category]=NewNode

                    # repeat for children
                    Main(filename,NewNode,attributes.get(NewNode.name))
                else :
                    #No more attribute, but still not a class
                    NewNode = Node()
                    NewNode.name= -1
                    NewNode.parents= ParentNode.parents.copy()
                    NewNode.parents[ParentNode.name]= category
                    NewNode.parents[NewNode.name]='None'
                    # Add the node as a child of parent Node
                    ParentNode.children[category]=NewNode

            else :
                    # the category is a class
                    NewNode = Node()
                    NewNode.name= -1
                    bool,NewNode.Class=OneClass(filename, ParentNode, category)
                    NewNode.parents= ParentNode.parents.copy()
                    NewNode.parents[ParentNode.name]= category
                    NewNode.parents[NewNode.name]='None'
                    # Add the node as a child of parent Node
                    ParentNode.children[category]=NewNode



# find the final Node
def lookup(outfile, array, Node,missingValue):
    if Node.name==-1 or missingValue==True :
        if missingValue==True :
            result= 'Unknown'
        else :
            result=Node.Class
        outfile.writerow([array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9],array[10],array[11],array[12],array[13],result])
    else :
        for category in Node.children:
            if array[Node.name].strip()==category.strip() :
                lookup(outfile,array,Node.children[category],missingValue)




# Apply the decision Tree
def DecisionTree(infilename, outfilename, Node) :
    with open(infilename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        outfile = csv.writer(open(outfilename, "wb"))
        i=0
        for row in csvreader:
            array =[]
            missingValue=False
            for i in range(14) :
                array.append(row[i])
                if row[i].strip()=='?':
                    missingValue=True
            lookup(outfile, array,Node,missingValue)
            i=i+1

# delete lines of missing values
def missingValues (filenameIn,filnameOut):
     with open(filnameOut, 'w') as fout :
          with open(filenameIn) as fin :
            for line in fin:
                if '?' not in line:
                    fout.write(line)

# reterun the nomber of rows in a file
def nbRows(filename) :
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            a=row[0]
    return reader.line_num


# Create final output file
def output( filename,outfilename):
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        outfile = csv.writer(open(outfilename, "wb"))
        i=1
        for row in csvreader:
            array=[]
            array.append(i)
            array.append(row[14])
            outfile.writerow([array[0],array[1]])
            i=i+1


# missing values and contunious categories
missingValues ('adult.data','1.output')
educationNumCategory('1.output','2.output')
fnlwgtCategory('2.output','3.output')
LossCategory('3.output','4.output',median ('3.output', 11))
GainCategory('4.output','5.output',median ('4.output', 10))
HoursCategory('5.output','6.output')
AgeCategory('6.output', 'adult1.data')


# Attributes
workClass = {'Private': [], 'Self-emp-not-inc': [], 'Local-gov' : [], 'Self-emp-inc' : [],  'Federal-gov' :[], 'State-gov' :[] , 'Without-pay' :[], 'Never-worked' : []}
education = {'Bachelors' :[], 'Some-college' :[], '11th':[], 'HS-grad' :[], 'Prof-school' :[], 'Assoc-acdm' :[], 'Assoc-voc' :[], '9th' :[], '7th-8th' :[], '12th':[], 'Masters':[], '1st-4th':[], '10th':[], 'Doctorate':[], '5th-6th':[], 'Preschool':[]}
maritalStatus = {'Married-civ-spouse': [], 'Divorced': [], 'Never-married': [], 'Separated': [], 'Widowed':[], 'Married-spouse-absent':[], 'Married-AF-spouse':[]}
occupation = {'Armed-Forces' :[],'Transport-moving': [], 'Priv-house-serv': [], 'Protective-serv': [],'Machine-op-inspct': [], 'Adm-clerical': [], 'Farming-fishing': [],'Tech-support': [], 'Craft-repair': [], 'Other-service': [], 'Sales': [], 'Exec-managerial':[], 'Prof-specialty':[], 'Handlers-cleaners':[] }
relationship = {'Wife': [], 'Own-child': [], 'Husband': [], 'Not-in-family': [], 'Other-relative':[], 'Unmarried':[]}
race = {'White': [], 'Asian-Pac-Islander': [], 'Amer-Indian-Eskimo': [], 'Other': [], 'Black': []}
sex= {'Female' :[], 'Male': []}
nativeCountry = {'Holand-Netherlands' : [],'Scotland' : [],'Thailand' : [],'Yugoslavia' : [],'El-Salvador' : [],'Trinadad&Tobago' : [],'Peru' : [],'Hong' : [],'Ecuador' :[],'Taiwan' : [],'Haiti' : [],'Columbia' : [],'Hungary' : [],'Guatemala' : [],'Nicaragua' : [],'Italy' : [],'Poland' : [], 'Jamaica' : [], 'Vietnam' : [], 'Mexico' : [], 'Portugal' : [], 'Ireland' : [], 'France' : [], 'Dominican-Republic' : [],'Laos' : [],'Germany' : [],'South': [], 'China': [], 'Cuba': [], 'Iran': [], 'Honduras': [],'Philippines': [], 'Outlying-US(Guam-USVI-etc)': [], 'India': [], 'Japan': [], 'Greece':[],'United-States': [], 'Cambodia': [], 'England': [], 'Puerto-Rico': [], 'Canada':[]}
age ={'1': [],'2': [],'3': [],'4': []}
hours ={'1': [],'2': [],'3': [],'4': []}
capitalLoss ={'1': [],'2': [],'3': []}
capitalGain ={'1': [],'2': [],'3': []}
fnlwgt={'0': []}
educationNum ={'0': []}

# Categories
NumberOfCatigories("adult1.data", age,0)
NumberOfCatigories("adult1.data",workClass, 1)
NumberOfCatigories("adult1.data", fnlwgt,2)
NumberOfCatigories("adult1.data",education, 3)
NumberOfCatigories("adult1.data", educationNum,4)
NumberOfCatigories("adult1.data",maritalStatus, 5)
NumberOfCatigories("adult1.data",occupation, 6)
NumberOfCatigories("adult1.data",relationship, 7)
NumberOfCatigories("adult1.data",race, 8)
NumberOfCatigories("adult1.data",sex, 9)
NumberOfCatigories("adult1.data", capitalGain,10)
NumberOfCatigories("adult1.data", capitalLoss,11)
NumberOfCatigories("adult1.data", hours,12)
NumberOfCatigories("adult1.data",nativeCountry, 13)


# Map of All Attributes
attributes={0:age, 1: workClass, 2: fnlwgt, 3:education, 4:educationNum, 5:maritalStatus, 6:occupation, 7:relationship, 8:race, 9:sex, 10:capitalGain, 11:capitalLoss, 12:hours, 13: nativeCountry}

# Gain

gain = []
gain.append(Gain("adult1.data", age,0,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", workClass,1,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
# ignore fnwgt attribute
gain.append(0)
gain.append(Gain("adult1.data", education,3,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
# ignore Education Number attribute
gain.append(0)
gain.append(Gain("adult1.data", maritalStatus,5,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", occupation,6,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", relationship,7,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", race,8,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", sex,9,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", capitalGain,10,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", capitalLoss,11,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", hours,12,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))
gain.append(Gain("adult1.data", nativeCountry,13,nbRows("adult1.data"), EntropyAllData("adult1.data",nbRows("adult1.data"))))

# Initialisation
Tree=Node()
Tree.name=gain.index(max(gain))
Tree.parents[Tree.name]='None'

# Build decision Tree
Main ("adult1.data",Tree,attributes[Tree.name])


#Apply Decision Tree
DecisionTree("Test", "Test1", Tree)

#output
output( "Test1","Test2")


