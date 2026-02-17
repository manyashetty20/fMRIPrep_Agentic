Node: single_subject_01_wf (anat_preproc_wf (anat_derivatives_wf (anat2std_tpms (fixes)
=======================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.anat_derivatives_wf.anat2std_tpms
 Exec ID : anat2std_tpms.a0


Original Inputs
---------------


* args : <undefined>
* default_value : 0.0
* dimension : 3
* environ : {'NSLOTS': '1'}
* float : True
* input_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-GM_mask.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-WM_mask.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-CSF_mask.nii.gz']
* input_image_type : <undefined>
* interpolation : Gaussian
* interpolation_parameters : <undefined>
* invert_transform_flags : <undefined>
* num_threads : 1
* out_postfix : _trans
* output_image : <undefined>
* print_out_composite_warp_file : <undefined>
* reference_image : <undefined>
* transforms : <undefined>


Execution Inputs
----------------


* args : <undefined>
* default_value : 0.0
* dimension : 3
* environ : {'NSLOTS': '1'}
* float : True
* input_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-GM_mask.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-WM_mask.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-CSF_mask.nii.gz']
* input_image_type : <undefined>
* interpolation : Gaussian
* interpolation_parameters : <undefined>
* invert_transform_flags : <undefined>
* num_threads : 1
* out_postfix : _trans
* output_image : <undefined>
* print_out_composite_warp_file : <undefined>
* reference_image : <undefined>
* transforms : <undefined>


Execution Outputs
-----------------


* output_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms0/aseg_label-GM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms1/aseg_label-WM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms2/aseg_label-CSF_mask_trans.nii.gz']


Subnode reports
---------------


 subnode 0 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms0/_report/report.rst
 subnode 1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms1/_report/report.rst
 subnode 2 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms2/_report/report.rst

