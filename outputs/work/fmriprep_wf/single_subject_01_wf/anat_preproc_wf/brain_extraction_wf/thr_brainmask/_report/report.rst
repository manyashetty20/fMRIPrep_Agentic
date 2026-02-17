Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (thr_brainmask (ants)
======================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.thr_brainmask
 Exec ID : thr_brainmask


Original Inputs
---------------


* args : <undefined>
* copy_header : True
* dimension : 3
* environ : {'NSLOTS': '1'}
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/map_brainmask/tpl-OASIS30ANTs_res-01_label-brain_probseg_trans.nii.gz
* input_mask : <undefined>
* inside_value : 1.0
* mode : <undefined>
* num_threads : 1
* num_thresholds : <undefined>
* output_image : <undefined>
* outside_value : 0.0
* th_high : 1.0
* th_low : 0.5


Execution Inputs
----------------


* args : <undefined>
* copy_header : True
* dimension : 3
* environ : {'NSLOTS': '1'}
* input_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/map_brainmask/tpl-OASIS30ANTs_res-01_label-brain_probseg_trans.nii.gz
* input_mask : <undefined>
* inside_value : 1.0
* mode : <undefined>
* num_threads : 1
* num_thresholds : <undefined>
* output_image : <undefined>
* outside_value : 0.0
* th_high : 1.0
* th_low : 0.5


Execution Outputs
-----------------


* output_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/thr_brainmask/tpl-OASIS30ANTs_res-01_label-brain_probseg_trans_resampled.nii.gz


Runtime info
------------


* cmdline : ThresholdImage 3 /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/map_brainmask/tpl-OASIS30ANTs_res-01_label-brain_probseg_trans.nii.gz tpl-OASIS30ANTs_res-01_label-brain_probseg_trans_resampled.nii.gz 0.500000 1.000000 1.000000 0.000000
* duration : 0.375961
* hostname : 87a7076871ed
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/thr_brainmask


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 


Terminal - standard error
~~~~~~~~~~~~~~~~~~~~~~~~~


  file 1.000000 does not exist . 


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

