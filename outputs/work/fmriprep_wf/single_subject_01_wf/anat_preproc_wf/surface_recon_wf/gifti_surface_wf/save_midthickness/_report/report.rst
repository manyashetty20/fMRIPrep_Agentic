Node: single_subject_01_wf (anat_preproc_wf (surface_recon_wf (gifti_surface_wf (save_midthickness (io)
=======================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.surface_recon_wf.gifti_surface_wf.save_midthickness
 Exec ID : save_midthickness


Original Inputs
---------------


* _outputs : {'surf.@graymid': ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/midthickness/mapflow/_midthickness0/rh.midthickness', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/midthickness/mapflow/_midthickness1/lh.midthickness']}
* base_directory : /out/freesurfer
* bucket : <undefined>
* container : sub-01
* creds_path : <undefined>
* encrypt_bucket_keys : <undefined>
* local_copy : <undefined>
* parameterization : False
* regexp_substitutions : <undefined>
* remove_dest_dir : False
* strip_dir : <undefined>
* substitutions : <undefined>


Execution Inputs
----------------


* _outputs : {'surf.@graymid': ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/midthickness/mapflow/_midthickness0/rh.midthickness', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/midthickness/mapflow/_midthickness1/lh.midthickness']}
* base_directory : /out/freesurfer
* bucket : <undefined>
* container : sub-01
* creds_path : <undefined>
* encrypt_bucket_keys : <undefined>
* local_copy : <undefined>
* parameterization : False
* regexp_substitutions : <undefined>
* remove_dest_dir : False
* strip_dir : <undefined>
* substitutions : <undefined>


Execution Outputs
-----------------


* out_file : ['/out/freesurfer/sub-01/surf/rh.midthickness', '/out/freesurfer/sub-01/surf/lh.midthickness']


Runtime info
------------


* duration : 0.004568
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/save_midthickness


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

