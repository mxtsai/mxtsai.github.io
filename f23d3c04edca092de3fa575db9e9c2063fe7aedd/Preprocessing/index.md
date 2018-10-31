# Pre-Processor Documentation

  * Need to install [PyDicom](https://pydicom.github.io/pydicom/stable/index.html)
  
  ### Files Placement
  ~~~
  PreProcessing\
    |--DICOM_Files\
      |--(patient ID, ex. 4015008183865)\
        |-- (a lot of DICOM files for that patient)
      ...
    |-- Program\
      |-- pacs_to_python.py
      |-- main.py
      |-- augument_and_upload.py
  ~~~
  
  **Explanation**: 
Inside the `PreProcessing` folder, there are two folders : `DICOM_Files` and `Program`. 

The `DICOM_Files` folder contains folders for each individual patient, and the name of those folders are the patient's ID. Inside each folder, there are the DICOM files for the particular scan we're interested in. For my case, that would be 464 layers of MRI Scans + 464 layer of drawn contours. All the files are DICOM files and the two differ in the name. For the MRI files, the name would begin with `MR` whereas the contour files begin with `PSg`. 

The `Program` folder contains three pieces of code:
 `main.py` is the code that controls the entire pre-processing process. Run this code to begin the entire pre-processing process. What happens behind the scenes is controlled by parameters set in this file.
 `pacs_to_python.py` is the code that takes the raw DICOM_Files (straight from the PACS) --> crop the contour region --> and ouputs a Numpy Matrix for that cropped contour.
 `augument_and_upload.py` takes the cropped contour, and performs data augmentation from it. In addition, if we are interested in backing up out data, this piece of code can upload it to Dropbox as backup. 
 
 ### Download Link
  * [main.py](mxtsai.github.io/bd2486d6f8d350c74adadff462efdb024f114f15/ResearchFiles/Preprocessing/main.py) 
  * [pacs_to_python.py](mxtsai.github.io/bd2486d6f8d350c74adadff462efdb024f114f15/ResearchFiles/Preprocessing/pacs_to_python.py) 
  * [augument_and_upload.py](mxtsai.github.io/bd2486d6f8d350c74adadff462efdb024f114f15/ResearchFiles/Preprocessing/augument_and_upload.py)  
 
  
