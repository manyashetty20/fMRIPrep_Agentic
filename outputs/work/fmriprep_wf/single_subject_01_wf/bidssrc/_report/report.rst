Node: single_subject_01_wf (bidssrc (bids)
==========================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.bidssrc
 Exec ID : bidssrc


Original Inputs
---------------


* subject_data : {'fmap': [], 'bold': ['/data/sub-01/func/sub-01_task-flanker_run-1_bold.nii.gz', '/data/sub-01/func/sub-01_task-flanker_run-2_bold.nii.gz'], 'sbref': [], 'flair': [], 't2w': [], 't1w': ['/data/sub-01/anat/sub-01_T1w.nii.gz'], 'roi': []}
* subject_id : 01


Execution Inputs
----------------


* subject_data : {'fmap': [], 'bold': ['/data/sub-01/func/sub-01_task-flanker_run-1_bold.nii.gz', '/data/sub-01/func/sub-01_task-flanker_run-2_bold.nii.gz'], 'sbref': [], 'flair': [], 't2w': [], 't1w': ['/data/sub-01/anat/sub-01_T1w.nii.gz'], 'roi': []}
* subject_id : 01


Execution Outputs
-----------------


* bold : ['/data/sub-01/func/sub-01_task-flanker_run-1_bold.nii.gz', '/data/sub-01/func/sub-01_task-flanker_run-2_bold.nii.gz']
* flair : <undefined>
* fmap : <undefined>
* out_dict : <undefined>
* roi : <undefined>
* sbref : <undefined>
* t1w : /data/sub-01/anat/sub-01_T1w.nii.gz
* t2w : <undefined>


Runtime info
------------


* duration : 0.026938
* hostname : 979c42b372d0
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/bidssrc


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
* OMP_NUM_THREADS : 1
* OS : Linux
* PATH : /usr/local/miniconda/bin:/opt/ICA-AROMA:/usr/lib/ants:/usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* POSSUMDIR : /usr/share/fsl/5.0
* PYTHONNOUSERSITE : 1
* PYTHONWARNINGS : ignore
* SUBJECTS_DIR : /opt/freesurfer/subjects

