Node: single_subject_01_wf (anat_preproc_wf (surface_recon_wf (segs_to_native_aparc_aseg (resample (freesurfer)
===============================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.surface_recon_wf.segs_to_native_aparc_aseg.resample
 Exec ID : resample


Original Inputs
---------------


* args : <undefined>
* environ : {'SUBJECTS_DIR': '/opt/freesurfer/subjects'}
* fs_target : <undefined>
* fsl_reg_file : <undefined>
* interp : <undefined>
* inverse : <undefined>
* invert_morph : <undefined>
* lta_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta
* lta_inv_file : <undefined>
* m3z_file : <undefined>
* mni_152_reg : <undefined>
* no_ded_m3z_path : <undefined>
* no_resample : <undefined>
* reg_file : <undefined>
* reg_header : <undefined>
* source_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aparc_aseg/resample/aparc+aseg.mgz
* subject : <undefined>
* subjects_dir : /opt/freesurfer/subjects
* tal : <undefined>
* tal_resolution : <undefined>
* target_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/copy_xform/sub-01_T1w_ras_valid_corrected_xform.nii.gz
* transformed_file : seg.nii.gz
* xfm_reg_file : <undefined>


Execution Inputs
----------------


* args : <undefined>
* environ : {'SUBJECTS_DIR': '/opt/freesurfer/subjects'}
* fs_target : <undefined>
* fsl_reg_file : <undefined>
* interp : <undefined>
* inverse : <undefined>
* invert_morph : <undefined>
* lta_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta
* lta_inv_file : <undefined>
* m3z_file : <undefined>
* mni_152_reg : <undefined>
* no_ded_m3z_path : <undefined>
* no_resample : <undefined>
* reg_file : <undefined>
* reg_header : <undefined>
* source_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aparc_aseg/resample/aparc+aseg.mgz
* subject : <undefined>
* subjects_dir : /opt/freesurfer/subjects
* tal : <undefined>
* tal_resolution : <undefined>
* target_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/copy_xform/sub-01_T1w_ras_valid_corrected_xform.nii.gz
* transformed_file : seg.nii.gz
* xfm_reg_file : <undefined>


Execution Outputs
-----------------


* transformed_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aparc_aseg/resample/seg.nii.gz


Runtime info
------------


* cmdline : mri_vol2vol --lta /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta --mov /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aparc_aseg/resample/aparc+aseg.mgz --targ /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/copy_xform/sub-01_T1w_ras_valid_corrected_xform.nii.gz --o seg.nii.gz
* duration : 1.177955
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aparc_aseg/resample


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 
Matrix from LTA:
-1.00000   0.00022  -0.00128   0.01246;
 0.00128  -0.00025  -1.00000  -0.11415;
 0.00022   1.00000  -0.00025  -0.16328;
 0.00000   0.00000   0.00000   1.00000;

/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aparc_aseg/resample/aparc+aseg.mgz /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/copy_xform/sub-01_T1w_ras_valid_corrected_xform.nii.gz
movvol /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aparc_aseg/resample/aparc+aseg.mgz
targvol /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/copy_xform/sub-01_T1w_ras_valid_corrected_xform.nii.gz
outvol seg.nii.gz
regfile /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta
invert 0
tal    0
talres 2
regheader 0
noresample 0
interp  trilinear (1)
precision  float (3)
Gdiag_no  -1
Synth      0
SynthSeed  1772165322

Final tkRAS-to-tkRAS Matrix is:
-1.00000   0.00022  -0.00128   0.01247;
 0.00128  -0.00025  -1.00000  -0.11412;
 0.00022   1.00000  -0.00025  -0.16329;
 0.00000   0.00000   0.00000   1.00000;


Vox2Vox Matrix is:
-1.00000  -0.00128  -0.00022   160.03534;
 0.00022  -0.00025  -1.00000   160.16432;
-0.00128   1.00000  -0.00025   95.93480;
 0.00000   0.00000   0.00000   1.00000;

Resampling
Output registration matrix is identity

mri_vol2vol done


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
* OMP_NUM_THREADS : 1
* OS : Linux
* PATH : /usr/local/miniconda/bin:/opt/ICA-AROMA:/usr/lib/ants:/usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* POSSUMDIR : /usr/share/fsl/5.0
* PYTHONNOUSERSITE : 1
* PYTHONWARNINGS : ignore
* SUBJECTS_DIR : /opt/freesurfer/subjects

