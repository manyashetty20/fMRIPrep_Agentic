Node: fixes
===========


 Hierarchy : _anat2std_tpms1
 Exec ID : _anat2std_tpms1


Original Inputs
---------------


* args : <undefined>
* default_value : 0.0
* dimension : 3
* environ : {'NSLOTS': '1'}
* float : True
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-WM_mask.nii.gz
* input_image_type : <undefined>
* interpolation : Gaussian
* interpolation_parameters : <undefined>
* invert_transform_flags : <undefined>
* num_threads : 1
* out_postfix : _trans
* output_image : <undefined>
* print_out_composite_warp_file : <undefined>
* reference_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/gen_ref/tpl-MNI152NLin2009cAsym_res-01_T1w_reference.nii.gz
* transforms : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniComposite.h5']


Execution Inputs
----------------


* args : <undefined>
* default_value : 0.0
* dimension : 3
* environ : {'NSLOTS': '1'}
* float : True
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-WM_mask.nii.gz
* input_image_type : <undefined>
* interpolation : Gaussian
* interpolation_parameters : <undefined>
* invert_transform_flags : <undefined>
* num_threads : 1
* out_postfix : _trans
* output_image : <undefined>
* print_out_composite_warp_file : <undefined>
* reference_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/gen_ref/tpl-MNI152NLin2009cAsym_res-01_T1w_reference.nii.gz
* transforms : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniComposite.h5']


Execution Outputs
-----------------


* output_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms1/aseg_label-WM_mask_trans.nii.gz


Runtime info
------------


* cmdline : antsApplyTransforms --default-value 0 --dimensionality 3 --float 1 --input /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-WM_mask.nii.gz --interpolation Gaussian --output aseg_label-WM_mask_trans.nii.gz --reference-image /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/gen_ref/tpl-MNI152NLin2009cAsym_res-01_T1w_reference.nii.gz --transform /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniComposite.h5
* duration : 1.4268399999999999
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms1


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 


Terminal - standard error
~~~~~~~~~~~~~~~~~~~~~~~~~


 


Environment
~~~~~~~~~~~


* AFNI_IMSAVE_WARNINGS : NO
* AFNI_MODELPATH : /usr/lib/afni/models
* AFNI_PLUGINPATH : /usr/lib/afni/plugins
* AFNI_TTATLAS_DATASET : /usr/share/afni/atlases
* ANTSPATH : /usr/lib/ants
* ANTS_RANDOM_SEED : 8256
* AROMA_VERSION : 0.4.5
* CPATH : /usr/local/miniconda/include/:
* FIX_VERTEX_AREA : 
* FREESURFER_HOME : /opt/freesurfer
* FSF_OUTPUT_FORMAT : nii.gz
* FSLDIR : /usr/share/fsl/5.0
* FSLMULTIFILEQUIT : TRUE
* FSLOUTPUTTYPE : NIFTI_GZ
* FSLTCLSH : /usr/bin/tclsh
* FSLWISH : /usr/bin/wish
* FSL_DIR : /usr/share/fsl/5.0
* FS_LICENSE : /opt/freesurfer/license.txt
* FS_OVERRIDE : 0
* FUNCTIONALS_DIR : /opt/freesurfer/sessions
* HOME : /home/fmriprep
* HOSTNAME : efad4839b3da
* IS_DOCKER_8395080871 : 1
* KMP_INIT_AT_FORK : FALSE
* LANG : C.UTF-8
* LC_ALL : C.UTF-8
* LD_LIBRARY_PATH : /usr/lib/fsl/5.0:
* LOCAL_DIR : /opt/freesurfer/local
* MINC_BIN_DIR : /opt/freesurfer/mni/bin
* MINC_LIB_DIR : /opt/freesurfer/mni/lib
* MKL_NUM_THREADS : 1
* MKL_THREADING_LAYER : INTEL
* MNI_DATAPATH : /opt/freesurfer/mni/data
* MNI_DIR : /opt/freesurfer/mni
* MNI_PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* NIPYPE_NO_ET : 1
* NO_ET : 1
* NSLOTS : 1
* OMP_NUM_THREADS : 1
* OS : Linux
* PATH : /usr/local/miniconda/bin:/opt/ICA-AROMA:/usr/lib/ants:/usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* POSSUMDIR : /usr/share/fsl/5.0
* PYTHONNOUSERSITE : 1
* PYTHONWARNINGS : ignore
* SUBJECTS_DIR : /opt/freesurfer/subjects

