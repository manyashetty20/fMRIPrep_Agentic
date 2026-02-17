import nibabel as nib
import os

def create_toy_brain():
    input_path = "./data/bids_input/sub-01/anat/sub-01_T1w.nii.gz"
    toy_path = "./data/bids_input/sub-01/anat/sub-01_T1w_toy.nii.gz"
    
    # Load the real brain
    img = nib.load(input_path)
    data = img.get_fdata()
    
    # Crop it to a 64x64x64 cube (very small!)
    # This reduces the data by about 80%
    toy_data = data[50:114, 50:114, 50:114]
    
    # Save the toy version
    toy_img = nib.Nifti1Image(toy_data, img.affine, img.header)
    nib.save(toy_img, toy_path)
    
    # Backup the original and replace it with the toy
    os.rename(input_path, input_path + ".bak")
    os.rename(toy_path, input_path)
    print("✅ Toy brain created! It is now 1/10th the size.")

create_toy_brain()