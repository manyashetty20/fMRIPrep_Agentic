Node: single_subject_01_wf (anat_preproc_wf (anat_norm_wf (outputnode (utility)
===============================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.anat_norm_wf.outputnode
 Exec ID : outputnode


Original Inputs
---------------


* anat2std_xfm : <undefined>
* anat2std_xfmJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniComposite.h5
* standardized : <undefined>
* standardizedJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/tpl_moving/sub-01_T1w_ras_valid_corrected_xform_trans.nii.gz
* std2anat_xfm : <undefined>
* std2anat_xfmJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniInverseComposite.h5
* std_dseg : <undefined>
* std_dsegJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_dseg/seg_dseg_trans.nii.gz
* std_mask : <undefined>
* std_maskJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_mask/sub-01_T1w_ras_valid_corrected_xform_rbrainmask_trans.nii.gz
* std_tpms : <undefined>
* std_tpmsJ1 : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_tpms/mapflow/_std_tpms0/aseg_label-GM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_tpms/mapflow/_std_tpms1/aseg_label-WM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_tpms/mapflow/_std_tpms2/aseg_label-CSF_mask_trans.nii.gz']
* template : <undefined>
* templateJ1 : MNI152NLin2009cAsym
* template_spec : <undefined>
* template_specJ1 : {}


Execution Inputs
----------------


* anat2std_xfm : <undefined>
* anat2std_xfmJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniComposite.h5
* standardized : <undefined>
* standardizedJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/tpl_moving/sub-01_T1w_ras_valid_corrected_xform_trans.nii.gz
* std2anat_xfm : <undefined>
* std2anat_xfmJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniInverseComposite.h5
* std_dseg : <undefined>
* std_dsegJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_dseg/seg_dseg_trans.nii.gz
* std_mask : <undefined>
* std_maskJ1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_mask/sub-01_T1w_ras_valid_corrected_xform_rbrainmask_trans.nii.gz
* std_tpms : <undefined>
* std_tpmsJ1 : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_tpms/mapflow/_std_tpms0/aseg_label-GM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_tpms/mapflow/_std_tpms1/aseg_label-WM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_tpms/mapflow/_std_tpms2/aseg_label-CSF_mask_trans.nii.gz']
* template : <undefined>
* templateJ1 : MNI152NLin2009cAsym
* template_spec : <undefined>
* template_specJ1 : {}


Execution Outputs
-----------------


* anat2std_xfm : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniComposite.h5']
* standardized : <undefined>
* std2anat_xfm : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/registration/ants_t1_to_mniInverseComposite.h5']
* std_dseg : <undefined>
* std_mask : <undefined>
* std_tpms : <undefined>
* template : ['MNI152NLin2009cAsym']
* template_spec : <undefined>


Runtime info
------------


* duration : 0.001268
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/outputnode


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
* OMP_NUM_THREADS : 1
* OS : Linux
* PATH : /usr/local/miniconda/bin:/opt/ICA-AROMA:/usr/lib/ants:/usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* POSSUMDIR : /usr/share/fsl/5.0
* PYTHONNOUSERSITE : 1
* PYTHONWARNINGS : ignore
* SUBJECTS_DIR : /opt/freesurfer/subjects

