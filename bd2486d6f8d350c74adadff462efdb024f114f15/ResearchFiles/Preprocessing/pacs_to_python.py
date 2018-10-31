# 'dicom_cropper' takes in a folder of dicom data and outputs the cropped contour regions
# the folder "DICOM_Files" should be in parallel to the "Pacs2Python" folder

import os
import shutil
import struct
import pydicom as dcm #Dealing with Meta
import numpy as np
import pandas as pd


#depthExtend : obtain a slightly deeper cropped box
#widHeiExtend : obtain a wider crop

#Some functions Needed in this dicom cropper***********************************
def drawBoundingBox(xd,yd,prevBox):

    updatedBox = [0,0,0,0]

    if prevBox[0]==None:
        updatedBox[0]=min(xd)
    else:
        updatedBox[0]=min(min(xd),prevBox[0])

    if prevBox[1]==None:
        updatedBox[1]=max(xd)
    else:
        updatedBox[1]=max(max(xd),prevBox[1])

    if prevBox[2]==None:
        updatedBox[2]=min(yd)
    else:
        updatedBox[2]=min(min(yd),prevBox[2])

    if prevBox[3]==None:
        updatedBox[3]=max(yd)
    else:
        updatedBox[3]=max(max(yd),prevBox[3])

    return updatedBox

def processT(sliceNumbers,t,depExtend):
    if(len(sliceNumbers)==1 or not sliceNumbers):
        print("Error in Contours- No Contour Slices Detected")
        return None

    totalSlc = sliceNumbers[0]
    oneTRange = int(totalSlc/4)
    minSlice = min(sliceNumbers[1:])
    maxSlice = max(sliceNumbers[1:])

    for i in range(1,depExtend+1): #extending the depth of the drawn contour
        sliceNumbers.append(minSlice-i)
        sliceNumbers.append(maxSlice+i)

    updatedSlices = []

    for indexes in sliceNumbers[1:]:
        upSlc = list(range(indexes,totalSlc,oneTRange)) #upwards slices
        dwSlc = list(range(indexes,0,-oneTRange)) #downwards slices
        sliceNumbers = np.union1d(upSlc,dwSlc)
        updatedSlices = np.union1d(updatedSlices,sliceNumbers)

    return [int(x) for x in np.sort(updatedSlices)]
#******************************************************************************

def convertPacsToPython(PATH=os.pardir + "/DICOM_Files",dicom_header="MR",
    contour_header="PSg",timeTakes=4,depthExtend=0,widHeiExtend=0,savePandas=False):

    print("------------------------------------------------  Converting Pacs to Python...")

    #Creating an empty DataFrame
    if savePandas == True:
        csv_format = ['PatientID','TumorShape [h,w,d]','Pixel Spacing [mm]',
                        'Slice Thickness [mm]','Augumented','File Directory','Slice Directory']
        patient_csv = pd.DataFrame( {'PatientID':[], 'TumorShape [h,w,d]':[],'Pixel Spacing [mm]':[],
                        'Slice Thickness [mm]':[],'Augumented':[],'File Directory':[],'Slice Directory':[]})
        patient_csv = patient_csv[csv_format]

    #Separate the raw DICOM with contours into folders 'D' and 'C'
    for dirpath,dirname,filename in os.walk(PATH): #go thru the folder of patient info
        for pat in dirname: #looping thru each patient
            pat_path = PATH + '/' + pat; #the directory of the current patient

            #Checking if the folder 'DICOM' or 'Contours' exists
            if os.path.exists(pat_path+"/DICOM") == False:
                os.makedirs(pat_path+"/DICOM") #Makes it if doesn't exist
            if os.path.exists(pat_path+"/Contours") == False:
                os.makedirs(pat_path+"/Contours") #Makes it if doesn't exist

            #Moving the corresponding files into the corresponding folders
            files = os.listdir(pat_path)
            for f in files:
                if f.startswith(dicom_header):
                    shutil.move(pat_path+"/"+f,pat_path+"/DICOM/"+f)
                elif f.startswith(contour_header):
                    shutil.move(pat_path+"/"+f,pat_path+"/Contours/"+f)


            #Set the initial bounding box as Nones
            boundingBox = [None,None,None,None]
            #Need the layers (eg.134, 257) for the slices of DICOM with tumor details
            sliceNumbers = [] 


            #Obtain the sliceNumbers, boundingBox values
            for f in os.listdir(pat_path+"/Contours"):
                ds = dcm.dcmread(pat_path+"/Contours/"+f)

                if("GraphicAnnotationSequence" in ds): #We have found a file that contains a drawn contour

                    roi = ds.GraphicAnnotationSequence[0].GraphicObjectSequence[0].GraphicData #x,y dots of the contour
                    xdata = roi[::2]
                    ydata = roi[1::2]
                    #Obtaining the bounding box for all T'

                    boundingBox = drawBoundingBox(xdata,ydata,boundingBox) #x_min,x_max,y_min,y_max, compares with last computed b.b.
                    if not sliceNumbers: #if empty
                        sliceNumbers.append(len(os.listdir(pat_path+"/Contours"))) #first element is how many layers for 1 t
                    sliceNumbers.append(ds.InstanceNumber-1); #the index > 1 just records the actual layer values

                    #Goal :
                    #(1)Extract a single numpy array from the countoured region for each 'T'
                    #(2)Obtain a position + width,length array for the scans (just one)
                    #print(xdata,ydata)

            boundingBox = [int(x) for x in boundingBox] #type conversion to integer
            sliceNumbers = processT(sliceNumbers,timeTakes,depthExtend) #generating the slices for each T captured
            pixelDist = max(boundingBox[1]-boundingBox[0],boundingBox[3]-boundingBox[2])
            depthDist = int(len(sliceNumbers)/timeTakes)

            #Define an empty 4D array for patient
            tumors4D = np.empty((timeTakes,pixelDist+(2*widHeiExtend),pixelDist+(2*widHeiExtend),depthDist)) 

            #Defining parameters for current scanned data for PANDAS
            patID = None
            tumor_shape = (pixelDist+(2*widHeiExtend),pixelDist+(2*widHeiExtend),depthDist)
            pixelSpacing = None
            sliceThickness = None
            slicesDir = []

            
            for takes in range(1,timeTakes+1):

                lay = 0
                for interestedSlices in sliceNumbers[(takes-1)*depthDist:takes*depthDist]: #cropping the numpy arrays
                    sliceFile = os.listdir(pat_path+"/DICOM")[interestedSlices]
                    dcmFile = dcm.dcmread(pat_path+"/DICOM/"+sliceFile)
                    slicePixels = dcmFile.pixel_array
                    #Generating a Cubed Output 3x3x3
                    slicePixels = slicePixels[boundingBox[2]-widHeiExtend:boundingBox[2]+widHeiExtend
                            +pixelDist,boundingBox[0]-widHeiExtend:boundingBox[0]+pixelDist+widHeiExtend]

                    tumors4D[takes-1,:,:,lay] = slicePixels
                    lay += 1;


                    #capturing data for Pandas
                    if savePandas == True:
                        if patID == None:
                            patIDstr = dcmFile.PatientID
                            patID = ''.join(i for i in patIDstr if i.isdigit())
                        if sliceThickness == None:
                            sliceThickness = dcmFile.SliceThickness 
                        if pixelSpacing == None:
                            pixelSpacing = dcmFile.PixelSpacing
                        slicesDir.append(pat_path+"/DICOM/"+sliceFile) #add the current slices to an array


            #Save the cropped Numpy file
            saveName = os.pardir +"/Cropped_Numpy_Files/"  + pat + ".npy"
            np.save(saveName,tumors4D)
            print("Saved" + saveName + "[COMPLETE]")
                
            
            #Saving into Pandas Dataframe
            if savePandas == True:
                row_df = pd.DataFrame([[patID,tumor_shape,pixelSpacing,sliceThickness,False,saveName,slicesDir]],
                    columns = csv_format)
                patient_csv=patient_csv.append(row_df)


        break; #stop the for-loop from looping into the DICOM_Files directory

    pat_save_name = os.pardir + "/patDetails.pkl"

    if savePandas == True:
        patient_csv.to_pickle(pat_save_name)
        print("Patient details saved")

    print("------------------------------------------------ Convertion to Python [COMPLETE]")


