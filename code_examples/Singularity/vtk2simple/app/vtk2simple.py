#!/usr/local/bin/python3

import vtk
import sys
from os import path
import numpy as np
import argparse
import json

def getGrid(file_name):
    colors = vtk.vtkNamedColors()
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(file_name)
    reader.Update() # Needed because of GetScalarRange
    return reader.GetOutput()

def getDeviations(grid):
    return grid.GetPointData().GetArray(0)

def getDeviation(deviations, ind):
    return deviations.GetTuple1(ind)

def extractVerts(grid):
    len = grid.GetNumberOfPoints()
    verts = np.empty([len, 4])
    deviations = getDeviations(grid)
    for i in range(0, len):
        point = grid.GetPoint(i)
        for j in range(0,3):
            verts[i, j] = point[j]
        verts[i, 3] = getDeviation(deviations, i)
    return verts

def extractCellInds(grid):
    len = grid.GetNumberOfCells()
    vertinds = np.empty([len, 3], dtype=int)
    for i in range(0, len):
        cell = grid.GetCell(i)
        if cell.GetNumberOfPoints() != 3:
            print("Not a triangle")
        for j in range(0,3):
            vertinds[i, j] = cell.GetPointId(j)
    return vertinds

def readGrid():
    return getGrid("/data/movedVK.vtk")

def writeFile(filename, verts, cellInds):
    with open(filename, 'w') as out:
        out.write(str(verts.shape[0]) + "\n")
        for i in range (0, verts.shape[0]):
            out.write(str(verts[i,0]) + " ")
            out.write(str(verts[i,1]) + " ")
            out.write(str(verts[i,2]) + " ")
            out.write(str(verts[i,3]) + "\n")
        out.write(str(cellInds.shape[0]) + "\n")
        for i in range (0, cellInds.shape[0]):
            out.write(str(cellInds[i,0]) + " ")
            out.write(str(cellInds[i,1]) + " ")
            out.write(str(cellInds[i,2]) + "\n")

def isVtk(filename):
    pre, ext = path.splitext(filename)
    return( ext == ".vtk")


def isConversionNeeded(infile, outfile):
    if (path.isfile(outfile)):
        return (False)
    else:
        return(True)
            
def changeFileExtension(filename, newExt):
    pre, ext = path.splitext(filename)
    print (pre)
    print (ext)
    return(pre + newExt)
            
def convertFile(inputfile):
    print("inputfile: \"" + inputfile +"\"")
    if not isVtk(inputfile):
        return inputfile
    outputfile = changeFileExtension(inputfile, ".simple")
    print("outputfile: \"" + outputfile + "\"")
    print("#Checking if conversion is needed")
    conversionNeeded = isConversionNeeded(inputfile, outputfile)
    print("conversionNeeded: " + str(conversionNeeded))
    if (not conversionNeeded):
        return (outputfile)
    grid = getGrid(inputfile)
#    scalar_range = grid.GetScalarRange()
    print("ncells: ", grid.GetNumberOfCells())
    print("npoints: ", grid.GetNumberOfPoints())
    print("#extracting vertices")
    verts = extractVerts(grid)
    print("#extracting grid")
    cellInds = extractCellInds(grid)
    print ("#writing output file");	
    writeFile(outputfile, verts, cellInds)
    return(outputfile)

def convertFileList(inputliststring):
    print("inputliststring:",inputliststring)
    inputlist=json.loads(inputliststring)
    nfiles = len(inputlist)
    print("nfiles: ", nfiles)
    outputlist = [None] * nfiles

    for i in range(nfiles):
        print("currfile: ", i)
        outputlist[i] = convertFile(inputlist[i])
        print("outputlist:", json.dumps(outputlist))

    
def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--filename')
    group.add_argument('--filelist')
    parser.add_argument('--logfile')

    args = parser.parse_args()

    
    inputfile = args.filename
    inputlist = args.filelist
    logfile = args.logfile
    print(logfile)
    if logfile :
        sys.stdout = open(logfile, 'w')

        
    print(inputfile)
    print(inputlist)

    if inputfile:
        print("nfiles: ", 1)
        print("currfile: ", 1)
        convertFile(inputfile)
    if inputlist:
        convertFileList(inputlist)
        
#    return()
    print ("#Finished");	
    print ("FINISHED");	
    

if __name__ == '__main__':
    main()

