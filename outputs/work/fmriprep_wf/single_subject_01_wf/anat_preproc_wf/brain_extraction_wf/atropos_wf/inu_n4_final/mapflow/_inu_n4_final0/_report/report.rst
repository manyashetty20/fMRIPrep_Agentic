Node: ants
==========


 Hierarchy : _inu_n4_final0
 Exec ID : _inu_n4_final0


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
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz
* mask_image : <undefined>
* n_iterations : [50, 50, 50, 50, 50]
* num_threads : 8
* output_image : <undefined>
* rescale_intensities : True
* save_bias : True
* shrink_factor : 4
* weight_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/apply_wm_prior/prodmap.nii.gz


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
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz
* mask_image : <undefined>
* n_iterations : [50, 50, 50, 50, 50]
* num_threads : 8
* output_image : <undefined>
* rescale_intensities : True
* save_bias : True
* shrink_factor : 4
* weight_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/apply_wm_prior/prodmap.nii.gz


Execution Outputs
-----------------


* bias_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/inu_n4_final/mapflow/_inu_n4_final0/sub-01_T1w_ras_valid_bias.nii.gz
* output_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/inu_n4_final/mapflow/_inu_n4_final0/sub-01_T1w_ras_valid_corrected.nii.gz


Runtime info
------------


* cmdline : N4BiasFieldCorrection --bspline-fitting [ 200 ] -d 3 --input-image /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz --convergence [ 50x50x50x50x50, 1e-07 ] --output [ sub-01_T1w_ras_valid_corrected.nii.gz, sub-01_T1w_ras_valid_bias.nii.gz ] -r --shrink-factor 4 --weight-image /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/apply_wm_prior/prodmap.nii.gz
* duration : 6.23397
* hostname : 87a7076871ed
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/inu_n4_final/mapflow/_inu_n4_final0


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
* NSLOTS : 8
* OMP_NUM_THREADS : 1
* OS : Linux
* PATH : /usr/local/miniconda/bin:/opt/ICA-AROMA:/usr/lib/ants:/usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* POSSUMDIR : /usr/share/fsl/5.0
* PYTHONNOUSERSITE : 1
* PYTHONWARNINGS : ignore
* SUBJECTS_DIR : /opt/freesurfer/subjects

