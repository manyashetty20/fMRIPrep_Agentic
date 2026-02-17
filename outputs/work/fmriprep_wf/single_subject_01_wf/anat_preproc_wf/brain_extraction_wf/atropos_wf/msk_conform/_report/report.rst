Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (atropos_wf (msk_conform (utility)
===================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.atropos_wf.msk_conform
 Exec ID : msk_conform


Original Inputs
---------------


* function_str : def _conform_mask(in_mask, in_reference):
    """Ensures the mask headers make sense and match those of the T1w"""
    from pathlib import Path
    import numpy as np
    import nibabel as nb
    from nipype.utils.filemanip import fname_presuffix

    ref = nb.load(in_reference)
    nii = nb.load(in_mask)
    hdr = nii.header.copy()
    hdr.set_data_dtype("int16")
    hdr.set_slope_inter(1, 0)

    qform, qcode = ref.header.get_qform(coded=True)
    if qcode is not None:
        hdr.set_qform(qform, int(qcode))

    sform, scode = ref.header.get_sform(coded=True)
    if scode is not None:
        hdr.set_sform(sform, int(scode))

    if "_maths" in in_mask:  # Cut the name at first _maths occurrence
        ext = "".join(Path(in_mask).suffixes)
        basename = Path(in_mask).name
        in_mask = basename.split("_maths")[0] + ext

    out_file = fname_presuffix(in_mask, suffix="_mask", newpath=str(Path()))
    nii.__class__(
        np.asanyarray(nii.dataobj).astype("int16"), ref.affine, hdr
    ).to_filename(out_file)
    return out_file

* in_mask : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/23_depad_mask/09_relabel_wm_maths_class-03_maths_maths_maths_maths_maths_maths_maths_maths_maths.nii.gz
* in_reference : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz


Execution Inputs
----------------


* function_str : def _conform_mask(in_mask, in_reference):
    """Ensures the mask headers make sense and match those of the T1w"""
    from pathlib import Path
    import numpy as np
    import nibabel as nb
    from nipype.utils.filemanip import fname_presuffix

    ref = nb.load(in_reference)
    nii = nb.load(in_mask)
    hdr = nii.header.copy()
    hdr.set_data_dtype("int16")
    hdr.set_slope_inter(1, 0)

    qform, qcode = ref.header.get_qform(coded=True)
    if qcode is not None:
        hdr.set_qform(qform, int(qcode))

    sform, scode = ref.header.get_sform(coded=True)
    if scode is not None:
        hdr.set_sform(sform, int(scode))

    if "_maths" in in_mask:  # Cut the name at first _maths occurrence
        ext = "".join(Path(in_mask).suffixes)
        basename = Path(in_mask).name
        in_mask = basename.split("_maths")[0] + ext

    out_file = fname_presuffix(in_mask, suffix="_mask", newpath=str(Path()))
    nii.__class__(
        np.asanyarray(nii.dataobj).astype("int16"), ref.affine, hdr
    ).to_filename(out_file)
    return out_file

* in_mask : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/23_depad_mask/09_relabel_wm_maths_class-03_maths_maths_maths_maths_maths_maths_maths_maths_maths.nii.gz
* in_reference : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz


Execution Outputs
-----------------


* out : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/msk_conform/09_relabel_wm_mask.nii.gz


Runtime info
------------


* duration : 0.056443
* hostname : 87a7076871ed
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/msk_conform


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
* OMP_NUM_THREADS : 1
* OS : Linux
* PATH : /usr/local/miniconda/bin:/opt/ICA-AROMA:/usr/lib/ants:/usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* POSSUMDIR : /usr/share/fsl/5.0
* PYTHONNOUSERSITE : 1
* PYTHONWARNINGS : ignore
* SUBJECTS_DIR : /opt/freesurfer/subjects

