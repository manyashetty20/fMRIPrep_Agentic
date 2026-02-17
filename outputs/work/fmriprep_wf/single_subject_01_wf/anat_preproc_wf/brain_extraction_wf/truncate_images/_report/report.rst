Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (truncate_images (ants)
========================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.truncate_images
 Exec ID : truncate_images


Original Inputs
---------------


* args : <undefined>
* copy_header : True
* dimension : 3
* environ : {'NSLOTS': '1'}
* num_threads : 1
* op1 : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz']
* op2 : 0.01 0.999 256
* operation : TruncateImageIntensity
* output_image : <undefined>


Execution Inputs
----------------


* args : <undefined>
* copy_header : True
* dimension : 3
* environ : {'NSLOTS': '1'}
* num_threads : 1
* op1 : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz']
* op2 : 0.01 0.999 256
* operation : TruncateImageIntensity
* output_image : <undefined>


Execution Outputs
-----------------


* output_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/truncate_images/mapflow/_truncate_images0/sub-01_T1w_ras_valid_maths.nii.gz']


Subnode reports
---------------


 subnode 0 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/truncate_images/mapflow/_truncate_images0/_report/report.rst

