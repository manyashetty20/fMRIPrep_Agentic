Node: single_subject_01_wf (anat_preproc_wf (anat_reports_wf (norm_msk (utility)
================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.anat_reports_wf.norm_msk
 Exec ID : norm_msk.a0


Original Inputs
---------------


* after : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/tpl_moving/sub-01_T1w_ras_valid_corrected_xform_trans.nii.gz
* after_mask : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_mask/sub-01_T1w_ras_valid_corrected_xform_rbrainmask_trans.nii.gz
* before : /home/fmriprep/.cache/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_T1w.nii.gz
* function_str : def _rpt_masks(mask_file, before, after, after_mask=None):
    from os.path import abspath
    import nibabel as nb
    msk = nb.load(mask_file).get_fdata() > 0
    bnii = nb.load(before)
    nb.Nifti1Image(bnii.get_fdata() * msk,
                   bnii.affine, bnii.header).to_filename('before.nii.gz')
    if after_mask is not None:
        msk = nb.load(after_mask).get_fdata() > 0

    anii = nb.load(after)
    nb.Nifti1Image(anii.get_fdata() * msk,
                   anii.affine, anii.header).to_filename('after.nii.gz')
    return abspath('before.nii.gz'), abspath('after.nii.gz')

* mask_file : /home/fmriprep/.cache/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_desc-brain_mask.nii.gz


Execution Inputs
----------------


* after : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/tpl_moving/sub-01_T1w_ras_valid_corrected_xform_trans.nii.gz
* after_mask : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_norm_wf/_template_MNI152NLin2009cAsym/std_mask/sub-01_T1w_ras_valid_corrected_xform_rbrainmask_trans.nii.gz
* before : /home/fmriprep/.cache/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_T1w.nii.gz
* function_str : def _rpt_masks(mask_file, before, after, after_mask=None):
    from os.path import abspath
    import nibabel as nb
    msk = nb.load(mask_file).get_fdata() > 0
    bnii = nb.load(before)
    nb.Nifti1Image(bnii.get_fdata() * msk,
                   bnii.affine, bnii.header).to_filename('before.nii.gz')
    if after_mask is not None:
        msk = nb.load(after_mask).get_fdata() > 0

    anii = nb.load(after)
    nb.Nifti1Image(anii.get_fdata() * msk,
                   anii.affine, anii.header).to_filename('after.nii.gz')
    return abspath('before.nii.gz'), abspath('after.nii.gz')

* mask_file : /home/fmriprep/.cache/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_desc-brain_mask.nii.gz


Execution Outputs
-----------------


* after : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_reports_wf/_template_MNI152NLin2009cAsym/norm_msk/after.nii.gz
* before : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_reports_wf/_template_MNI152NLin2009cAsym/norm_msk/before.nii.gz


Runtime info
------------


* duration : 0.547075
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_reports_wf/_template_MNI152NLin2009cAsym/norm_msk


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

