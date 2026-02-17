Node: single_subject_01_wf (anat_preproc_wf (anat_derivatives_wf (ds_std_tpms)
==============================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.anat_derivatives_wf.ds_std_tpms
 Exec ID : ds_std_tpms.a0


Original Inputs
---------------


* acquisition : <undefined>
* atlas : <undefined>
* base_directory : /out
* ceagent : <undefined>
* check_hdr : True
* cohort : <undefined>
* compress : [True]
* data_dtype : <undefined>
* datatype : <undefined>
* density : <undefined>
* desc : <undefined>
* direction : <undefined>
* dismiss_entities : <undefined>
* echo : <undefined>
* extension : <undefined>
* fmap : <undefined>
* from : <undefined>
* hemi : <undefined>
* in_file : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms0/aseg_label-GM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms1/aseg_label-WM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms2/aseg_label-CSF_mask_trans.nii.gz']
* label : ('GM', 'WM', 'CSF')
* meta_dict : <undefined>
* modality : <undefined>
* mode : <undefined>
* model : <undefined>
* proc : <undefined>
* reconstruction : <undefined>
* recording : <undefined>
* resolution : native
* roi : <undefined>
* run : <undefined>
* scans : <undefined>
* session : <undefined>
* source_file : ['/data/sub-01/anat/sub-01_T1w.nii.gz']
* space : MNI152NLin2009cAsym
* subject : <undefined>
* subset : <undefined>
* suffix : probseg
* task : <undefined>
* to : <undefined>


Execution Inputs
----------------


* acquisition : <undefined>
* atlas : <undefined>
* base_directory : /out
* ceagent : <undefined>
* check_hdr : True
* cohort : <undefined>
* compress : [True]
* data_dtype : <undefined>
* datatype : <undefined>
* density : <undefined>
* desc : <undefined>
* direction : <undefined>
* dismiss_entities : <undefined>
* echo : <undefined>
* extension : <undefined>
* fmap : <undefined>
* from : <undefined>
* hemi : <undefined>
* in_file : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms0/aseg_label-GM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms1/aseg_label-WM_mask_trans.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/anat2std_tpms/mapflow/_anat2std_tpms2/aseg_label-CSF_mask_trans.nii.gz']
* label : ('GM', 'WM', 'CSF')
* meta_dict : <undefined>
* modality : <undefined>
* mode : <undefined>
* model : <undefined>
* proc : <undefined>
* reconstruction : <undefined>
* recording : <undefined>
* resolution : native
* roi : <undefined>
* run : <undefined>
* scans : <undefined>
* session : <undefined>
* source_file : ['/data/sub-01/anat/sub-01_T1w.nii.gz']
* space : MNI152NLin2009cAsym
* subject : <undefined>
* subset : <undefined>
* suffix : probseg
* task : <undefined>
* to : <undefined>


Execution Outputs
-----------------


* compression : [True, True, True]
* fixed_hdr : [True, True, True]
* out_file : ['/out/fmriprep/sub-01/anat/sub-01_space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz', '/out/fmriprep/sub-01/anat/sub-01_space-MNI152NLin2009cAsym_label-WM_probseg.nii.gz', '/out/fmriprep/sub-01/anat/sub-01_space-MNI152NLin2009cAsym_label-CSF_probseg.nii.gz']
* out_meta : <undefined>


Runtime info
------------


* duration : 1.723944
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/ds_std_tpms


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

