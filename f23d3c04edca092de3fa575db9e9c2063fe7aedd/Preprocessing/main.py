#The Main Program

import os
import pacs_to_python
import augument_and_upload


import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

#*****************************************************************************
def viewMRI(np4D):

    fig = plt.figure()
    ax = plt.subplot()

    l = ax.imshow(np4D[:,:,0])

    depth = plt.axes([0.08, 0.02, 0.83, 0.03])
    slid = Slider(depth, 'Depth', 0, np4D.shape[2]-1, valinit=0)

    def update(val):
        layer = int(slid.val)
        im=np4D[:,:,layer]
        l.set_data(im)
        fig.canvas.draw()

    slid.on_changed(update)
    plt.show()


def viewPickle(pickleDir):
	if not pickleDir:
		print("No Data to Read")

	if pickleDir:
		pickFile = pd.read_pickle(pickleDir)
		print(pickFile)

#******************************************************************************



#Please first place the DICOM Folders into '/DICOM_Files/'



#Generating the necessary folders
if os.path.exists(os.pardir+"/Augumented_Numpy_Files") == False:
    os.makedirs(os.pardir+"/Augumented_Numpy_Files") #Makes it if doesn't exist

if os.path.exists(os.pardir+"/Cropped_Numpy_Files") == False:
    os.makedirs(os.pardir+"/Cropped_Numpy_Files") #Makes it if doesn't exist


pacs_to_python.convertPacsToPython(savePandas = True,widHeiExtend=2,depthExtend=1)
augument_and_upload.process_unaugumented_patients(uploadNP=True,uploadDICOM=True,uploadPatientCSV=True)


viewPickle(os.pardir + "/patDetails.pkl")
