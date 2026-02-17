Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (map_wmmask (fixes)
====================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.map_wmmask
 Exec ID : map_wmmask


Original Inputs
---------------


* args : <undefined>
* default_value : 0.0
* dimension : <undefined>
* environ : {'NSLOTS': '1'}
* float : False
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/full_wm/summap.nii.gz
* input_image_type : <undefined>
* interpolation : Gaussian
* interpolation_parameters : <undefined>
* invert_transform_flags : [True, False]
* num_threads : 1
* out_postfix : _trans
* output_image : <undefined>
* print_out_composite_warp_file : <undefined>
* reference_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz
* transforms : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template0GenericAffine.mat', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template1InverseWarp.nii.gz']


Execution Inputs
----------------


* args : <undefined>
* default_value : 0.0
* dimension : <undefined>
* environ : {'NSLOTS': '1'}
* float : False
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/full_wm/summap.nii.gz
* input_image_type : <undefined>
* interpolation : Gaussian
* interpolation_parameters : <undefined>
* invert_transform_flags : [True, False]
* num_threads : 1
* out_postfix : _trans
* output_image : <undefined>
* print_out_composite_warp_file : <undefined>
* reference_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz
* transforms : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template0GenericAffine.mat', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template1InverseWarp.nii.gz']


Execution Outputs
-----------------


* output_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/map_wmmask/summap_trans.nii.gz


Runtime info
------------


* cmdline : antsApplyTransforms --default-value 0 --float 0 --input /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/full_wm/summap.nii.gz --interpolation Gaussian --output summap_trans.nii.gz --reference-image /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz --transform [ /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template0GenericAffine.mat, 1 ] --transform /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template1InverseWarp.nii.gz
* duration : 5.354125
* hostname : 87a7076871ed
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/map_wmmask


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
* ANTS_RANDOM_SEED : 28249
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
* HOSTNAME : 87a7076871ed
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

