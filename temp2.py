import nibabel as nib
import numpy

imgFile = '/users/jbwexler/Downloads/VBM_patients_increase_1.nii.gz'
img = nib.load(imgFile)
imgData = img.get_data()

isZero = (imgData == 0).sum()/float(imgData.size)
print isZero