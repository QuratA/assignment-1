
# return a floating point value.
from __future__ import division
import csv
import math

# Node
class Node:
    def __init__(self):
        self.name=-1
        self.Class= "Unknown"
        self.parents=dict()
        self.children = dict()



# Entropy of root
# tolal : nomber of total Data
def EntropyAllData(filename, total):
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        nb=0
        for row in csvreader:
            if row[14].strip() == "<=50K":
                nb=nb+1
        Entropy=  - math.log((nb/total),2)*(nb/total) - math.log(((total-nb)/total),2)*((total-nb)/total)
    return Entropy

# Entropy of a branch
def CategoryEntropy(filename,attribute,category):
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        high=0
        less=0
        for row in csvreader:
            if (row[attribute].strip()==category) and (row[14].strip()== "<=50K") :
                high=high+1
            if (row[attribute].strip()==category) and (row[14].strip()== ">50K") :
                less=less+1
    total=high+less
    if high==0 or less==0 :
        return 0
    else :
        return (float(high)/total)*math.log((float(high)/total),2)+(float(less)/total)*math.log((float(less)/total),2)


# the number of each category of an attribute
# Map of the attribute with all the categories
# the column that represente this attribute
def NumberOfCatigories(filename, Map, AttributeNumber):

    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        NbRow=0
        for row in csvreader:
            for key in Map :
                if row[AttributeNumber].strip() == key.strip():
                    Map[key].append(NbRow)
            NbRow=NbRow+1





# Map of an attribute
# AttributeNumber : column of the attribute
# Total :Total All rows
# Entropy : Entropy of root
# caterory
def Gain(filename, Map,AttributeNumber,Total, Entropy):
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        nb=0
        EntropyMap = dict()
        for key in Map :
            EntropyMap[key]=0
            for row in csvreader:
                if (row[AttributeNumber].strip() == key.strip()) and (row[14].strip() == "<=50K"):
                    nb=nb+1

            if nb !=0 and (len(Map[key])-nb) !=0 :
                EntropyMap[key]= ((float(nb)/len(Map[key]))*math.log(float(nb)/len(Map[key]), 2)+(float((len(Map[key])-nb))/len(Map[key]))*math.log(float((len(Map[key])-nb))/len(Map[key]), 2))* float(len(Map[key]))/Total
            else :
                EntropyMap[key]=0

            nb=0;
            Gain=Entropy
        for key in Map :
            Gain=Gain -EntropyMap[key]
    return Gain





# return true if the attribute i is a parent of node
def isParent(node, i):
    for j in node.parents :
        if j==i :
            return True
    return False


# put age in categories
def AgeCategory(filename, filnameOutput) :
    with open(filename, 'rb') as csvfile:
        outfile = csv.writer(open(filnameOutput, "wb"))
        csvreader = csv.reader(csvfile, delimiter=',')
        array=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for row in csvreader:
            array[0]=row[0]
            array[1]=row[1]
            array[2]=row[2]
            array[3]=row[3]
            array[4]=row[4]
            array[5]=row[5]
            array[6]=row[6]
            array[7]=row[7]
            array[8]=row[8]
            array[9]=row[9]
            array[10]=row[10]
            array[11]=row[11]
            array[12]=row[12]
            array[13]=row[13]
            array[14]=row[14]
            # age categories
            if int(array[0]) >0 and int(array[0]) <= 45 :
                if int(array[0]) >0 and int(array[0]) <= 25 :
                    array[0]=1
                else :
                    array[0]=2
            else :
                if int(array[0]) >45 and int(array[0]) <= 65 :
                    array[0]=3
                else :
                    array[0]=4
            # Change the file ( array)
            outfile.writerow([array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9],array[10],array[11],array[12],array[13],array[14]])

# Hours per week to categories
def HoursCategory(filename,filnameOutput) :
    with open(filename, 'rb') as csvfile:
        outfile = csv.writer(open(filnameOutput, "wb"))
        csvreader = csv.reader(csvfile, delimiter=',')
        array=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for row in csvreader:
            array[0]=row[0]
            array[1]=row[1]
            array[2]=row[2]
            array[3]=row[3]
            array[4]=row[4]
            array[5]=row[5]
            array[6]=row[6]
            array[7]=row[7]
            array[8]=row[8]
            array[9]=row[9]
            array[10]=row[10]
            array[11]=row[11]
            array[12]=row[12]
            array[13]=row[13]
            array[14]=row[14]
            # age categories
            if int(array[12]) >0 and int(array[12]) <= 40 :
                if int(array[12]) >0 and int(array[12]) <= 25 :
                    array[12]=1
                else :
                    array[12]=2
            else :
                if int(array[12]) >40 and int(array[12]) <= 60 :
                    array[12]=3
                else :
                    array[12]=4
            # Change the file ( array)
            outfile.writerow([array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9],array[10],array[11],array[12],array[13],array[14]])

# median of values of one culomn
def median (filename, i):
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        nb=0
        val=0
        for row in csvreader:
            if int(row[i])> 0:
                nb=nb+1
                val=val+int(int(row[i]))
    if (nb==0):
        return 0
    return val/float(nb)


#Capital Gain to categories
def GainCategory(filename,filnameOutput,Median) :
    with open(filename, 'rb') as csvfile:
        outfile = csv.writer(open(filnameOutput, "wb"))
        csvreader = csv.reader(csvfile, delimiter=',')
        array=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for row in csvreader:
            array[0]=row[0]
            array[1]=row[1]
            array[2]=row[2]
            array[3]=row[3]
            array[4]=row[4]
            array[5]=row[5]
            array[6]=row[6]
            array[7]=row[7]
            array[8]=row[8]
            array[9]=row[9]
            array[10]=row[10]
            array[11]=row[11]
            array[12]=row[12]
            array[13]=row[13]
            array[14]=row[14]

            # categories
            if int(array[10]) > Median :
                 array[10]=  1
            else :
                if int(array[10])==0:
                    array[10]=3
                else :
                    array[10]=2
            # Change the file ( array)
            outfile.writerow([array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9],array[10],array[11],array[12],array[13],array[14]])




# Capital loss To categories
def LossCategory(filename,filnameOutput,Median) :
    with open(filename, 'rb') as csvfile:
        outfile = csv.writer(open(filnameOutput, "wb"))
        csvreader = csv.reader(csvfile, delimiter=',')
        array=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for row in csvreader:
            array[0]=row[0]
            array[1]=row[1]
            array[2]=row[2]
            array[3]=row[3]
            array[4]=row[4]
            array[5]=row[5]
            array[6]=row[6]
            array[7]=row[7]
            array[8]=row[8]
            array[9]=row[9]
            array[10]=row[10]
            array[11]=row[11]
            array[12]=row[12]
            array[13]=row[13]
            array[14]=row[14]

            # categories
            if int(array[11]) > Median :
                 array[11]=  1
            else :
                if int(array[11])==0:
                    array[11]=3
                else :
                    array[11]=2
            # Change the file ( array)
            outfile.writerow([array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9],array[10],array[11],array[12],array[13],array[14]])



# ignore the fnlwgt attribute
def fnlwgtCategory(filename,filnameOutput) :
    with open(filename, 'rb') as csvfile:
        outfile = csv.writer(open(filnameOutput, "wb"))
        csvreader = csv.reader(csvfile, delimiter=',')
        array=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for row in csvreader:
            array[0]=row[0]
            array[1]=row[1]
            array[2]=row[2]
            array[3]=row[3]
            array[4]=row[4]
            array[5]=row[5]
            array[6]=row[6]
            array[7]=row[7]
            array[8]=row[8]
            array[9]=row[9]
            array[10]=row[10]
            array[11]=row[11]
            array[12]=row[12]
            array[13]=row[13]
            array[14]=row[14]

            # categories
            array[2]=0
            # Change the file ( array)
            outfile.writerow([array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9],array[10],array[11],array[12],array[13],array[14]])

# ignore the education Number
def educationNumCategory(filename,filnameOutput) :
    with open(filename, 'rb') as csvfile:
        outfile = csv.writer(open(filnameOutput, "wb"))
        csvreader = csv.reader(csvfile, delimiter=',')
        array=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for row in csvreader:
            array[0]=row[0]
            array[1]=row[1]
            array[2]=row[2]
            array[3]=row[3]
            array[4]=row[4]
            array[5]=row[5]
            array[6]=row[6]
            array[7]=row[7]
            array[8]=row[8]
            array[9]=row[9]
            array[10]=row[10]
            array[11]=row[11]
            array[12]=row[12]
            array[13]=row[13]
            array[14]=row[14]

            # categories
            array[4]=0
            # Change the file ( array)
            outfile.writerow([array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9],array[10],array[11],array[12],array[13],array[14]])





