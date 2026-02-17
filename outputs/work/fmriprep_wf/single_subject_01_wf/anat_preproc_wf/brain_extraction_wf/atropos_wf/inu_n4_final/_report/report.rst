Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (atropos_wf (inu_n4_final (ants)
=================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.atropos_wf.inu_n4_final
 Exec ID : inu_n4_final


Original Inputs
---------------


* args : <undefined>
* bias_image : <undefined>
* bspline_fitting_distance : 200.0
* bspline_order : <undefined>
* convergence_threshold : 1e-07
* copy_header : True
* dimension : 3
* environ : {'NSLOTS': '8'}
* histogram_sharpening : <undefined>
* input_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz']
* mask_image : <undefined>
* n_iterations : [50, 50, 50, 50, 50]
* num_threads : 8
* output_image : <undefined>
* rescale_intensities : True
* save_bias : True
* shrink_factor : 4
* weight_image : <undefined>


Execution Inputs
----------------


* args : <undefined>
* bias_image : <undefined>
* bspline_fitting_distance : 200.0
* bspline_order : <undefined>
* convergence_threshold : 1e-07
* copy_header : True
* dimension : 3
* environ : {'NSLOTS': '8'}
* histogram_sharpening : <undefined>
* input_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz']
* mask_image : <undefined>
* n_iterations : [50, 50, 50, 50, 50]
* num_threads : 8
* output_image : <undefined>
* rescale_intensities : True
* save_bias : True
* shrink_factor : 4
* weight_image : <undefined>


Execution Outputs
-----------------


* bias_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/inu_n4_final/mapflow/_inu_n4_final0/sub-01_T1w_ras_valid_bias.nii.gz']
* output_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/inu_n4_final/mapflow/_inu_n4_final0/sub-01_T1w_ras_valid_corrected.nii.gz']


Subnode reports
---------------


 subnode 0 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/inu_n4_final/mapflow/_inu_n4_final0/_report/report.rst

