import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd
import os
import dropbox

def augument_save_np4d(array4D,dir,arrName):

    #Flip the MRI File
    flp0 = array4D[:,:,:,::-1]

    #Rotating the original MRI File
    org90 = np.rot90(array4D,axes=(1,2))
    org180 = np.rot90(org90,axes=(1,2))
    org270 = np.rot90(org180,axes=(1,2))

    #Rotating the flipped MRI file
    flp90 = np.rot90(flp0,axes=(1,2))
    flp180 = np.rot90(flp90,axes=(1,2))
    flp270 = np.rot90(flp180,axes=(1,2))

    sv_org0 = dir + "/" + arrName + "_org0.npy"
    sv_flp0 = dir + "/" + arrName + "_flp0.npy"

    sv_org90 = dir + "/" + arrName + "_org90.npy"
    sv_org180 = dir + "/" + arrName + "_org180.npy"
    sv_org270 = dir + "/" + arrName + "_org270.npy"

    sv_flp90 = dir + "/" + arrName + "_flp90.npy"
    sv_flp180 = dir + "/" + arrName + "_flp180.npy"
    sv_flp270 = dir + "/" + arrName + "_flp270.npy"

    np.save(sv_org0,array4D)
    np.save(sv_flp0,flp0)

    np.save(sv_org90,org90)
    np.save(sv_org180,org180)
    np.save(sv_org270,org270)

    np.save(sv_flp90,flp90)
    np.save(sv_flp180,flp180)
    np.save(sv_flp270,flp270)

    return [sv_org0,sv_org90,sv_org180,sv_org270,sv_flp0,sv_flp90,sv_flp180,sv_flp270]

def uploadDicom(row_list,dbx): #have to define this since dicom uploading takes a lot of time
    for rows in row_list:
        patName = rows[0]
        dcmIter = 1

        for dcmdir in rows[1]:
            dicomBin = open(dcmdir,mode='rb').read()
            dbx.files_upload(dicomBin,'/DICOM Files/'+patName+"/"+str(dcmIter)+".dcm",mode=dropbox.files.WriteMode('add'))
            dcmIter+=1


def uploadPatientCSVdropbox(dir,dbx): #to upload the patient CSV online
	csvFile = open(dir,mode='rb').read()
	dbx.files_upload(csvFile,'/patDetails.pkl',mode=dropbox.files.WriteMode('add'))


def process_unaugumented_patients(uploadNP = False,uploadDICOM = False, uploadPatientCSV=False):

    print("------------------------------------------------ Augumenting and Uploading...")

    dbx = None
    if uploadNP or uploadDICOM:
        dbx = dropbox.Dropbox("ncIFm-QIFTAAAAAAAAAACTOi8H6JSGo0EdRg3gwS4XAH5cJEogzfUPHI4QHA4OHK") #Logging into Dropbox

    patientDetails = pd.read_pickle(os.pardir + "/patDetails.pkl")#Reading the Patient Information Generated (Pandas)
    augumentedDestination = os.pardir + "/Augumented_Numpy_Files" #output destination of the augumented files

    nameSet = ["_org0.npy","_org90.npy","_org180.npy","_org270.npy","_flp0.npy","_flp90.npy","_flp180.npy","_flp270.npy"]
    dicomUploadList = []

    for index,row in patientDetails.iterrows(): #Looping through each patient detailed in the Information Generated 

        augumentedBoolean = row["Augumented"] #Obtain whether we have augumented this data copy yet or not

        if augumentedBoolean == True: #If already augumented before, then skip the rest of the statements and next row
            continue

        np4d = np.load(row["File Directory"]) #Loading the 4D numpy array
        patName = row["PatientID"] #Getting the Patient's name



        #Perform Data Augmentation on the 'Scaled' Array
        quadNp4DSet = augument_save_np4d(np4d,augumentedDestination,patName)
        print("-------------------- Augumentation and Save  [COMPLETE]")

        #Writing the Augumented as true
        patientDetails.at[index,'Augumented'] = 1.0

        #Uploading to DropBox [Only uploading the Augumented Files]
        if uploadNP:
            nameIter = 0;
            for np4d_dir in quadNp4DSet:
                np4d = open(np4d_dir,mode='rb').read()
                dbx.files_upload(np4d,'/Augumented Numpy Files/'+ patName + nameSet[nameIter],mode=dropbox.files.WriteMode('add'))
                nameIter+=1


        #Uploading the DICOM files
        
        if uploadDICOM:
            dicomUploadList.append([patName,row["Slice Directory"]])


    #Saving the Pandas Dataframe back to place
    pat_save_name = os.pardir + "/patDetails.pkl"
    patientDetails.to_pickle(pat_save_name)
    print("--------------------Patient CSV  [UPDATED]")

    if uploadPatientCSV:
    	uploadPatientCSVdropbox(pat_save_name,dbx)


    if uploadNP:
        print("-------------------- Uploaded Augumented Numpy  [COMPLETE]")



    if uploadDICOM:
        print("-------------------- Uploading Selected Dicoms...")
        uploadDicom(dicomUploadList,dbx)
        print("-------------------- Uploaded Selected Dicoms   [COMPLETE]")



