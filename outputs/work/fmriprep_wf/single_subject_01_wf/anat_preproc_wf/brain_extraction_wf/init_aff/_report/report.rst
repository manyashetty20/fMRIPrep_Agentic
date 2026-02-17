Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (init_aff (ants)
=================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.init_aff
 Exec ID : init_aff


Original Inputs
---------------


* args : <undefined>
* convergence : (10, 1e-06, 10)
* dimension : 3
* environ : {'NSLOTS': '8'}
* fixed_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/res_tmpl/tpl-OASIS30ANTs_res-01_T1w_regrid.nii.gz
* fixed_image_mask : /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz
* metric : ('Mattes', 32, 'Regular', 0.25)
* moving_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/res_target/sub-01_T1w_ras_valid_maths_corrected_regrid.nii.gz
* moving_image_mask : <undefined>
* num_threads : 8
* output_transform : initialization.mat
* principal_axes : False
* search_factor : (15.0, 0.1)
* search_grid : (40.0, (0.0, 40.0, 40.0))
* transform : ('Affine', 0.1)
* verbose : True


Execution Inputs
----------------


* args : <undefined>
* convergence : (10, 1e-06, 10)
* dimension : 3
* environ : {'NSLOTS': '8'}
* fixed_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/res_tmpl/tpl-OASIS30ANTs_res-01_T1w_regrid.nii.gz
* fixed_image_mask : /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz
* metric : ('Mattes', 32, 'Regular', 0.25)
* moving_image : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/res_target/sub-01_T1w_ras_valid_maths_corrected_regrid.nii.gz
* moving_image_mask : <undefined>
* num_threads : 8
* output_transform : initialization.mat
* principal_axes : False
* search_factor : (15.0, 0.1)
* search_grid : (40.0, (0.0, 40.0, 40.0))
* transform : ('Affine', 0.1)
* verbose : True


Execution Outputs
-----------------


* output_transform : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/init_aff/initialization.mat


Runtime info
------------


* cmdline : antsAI -c [10,1e-06,10] -d 3 -x /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz -m Mattes[/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/res_tmpl/tpl-OASIS30ANTs_res-01_T1w_regrid.nii.gz,/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/res_target/sub-01_T1w_ras_valid_maths_corrected_regrid.nii.gz,32,Regular,0.25] -o initialization.mat -p 0 -s [15,0.1] -g [40.0,0x40x40] -t Affine[0.1] -v 1
* duration : 198.402529
* hostname : 979c42b372d0
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/init_aff


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 Using the Mattes MI metric (number of bins = 32)
Starting optimizer with 243 starting points


Terminal - standard error
~~~~~~~~~~~~~~~~~~~~~~~~~


 


Environment
~~~~~~~~~~~


* AFNI_IMSAVE_WARNINGS : NO
* AFNI_MODELPATH : /usr/lib/afni/models
* AFNI_PLUGINPATH : /usr/lib/afni/plugins
* AFNI_TTATLAS_DATASET : /usr/share/afni/atlases
* ANTSPATH : /usr/lib/ants
* ANTS_RANDOM_SEED : 29680
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
* HOSTNAME : 979c42b372d0
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

