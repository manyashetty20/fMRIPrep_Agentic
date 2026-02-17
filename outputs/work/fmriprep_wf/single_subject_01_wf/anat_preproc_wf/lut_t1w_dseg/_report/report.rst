Node: single_subject_01_wf (anat_preproc_wf (lut_t1w_dseg (utility)
===================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.lut_t1w_dseg
 Exec ID : lut_t1w_dseg


Original Inputs
---------------


* function_str : def apply_lut(in_dseg, lut, newpath=None):
    """Map the input discrete segmentation to a new label set (lookup table, LUT)."""
    import numpy as np
    import nibabel as nb
    from nipype.utils.filemanip import fname_presuffix

    if newpath is None:
        from os import getcwd
        newpath = getcwd()

    out_file = fname_presuffix(in_dseg, suffix='_dseg', newpath=newpath)
    lut = np.array(lut, dtype='int16')

    segm = nb.load(in_dseg)
    hdr = segm.header.copy()
    hdr.set_data_dtype('int16')
    segm.__class__(lut[np.asanyarray(segm.dataobj, dtype=int)].astype('int16'),
                   segm.affine, hdr).to_filename(out_file)

    return out_file

* in_dseg : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aseg/resample/seg.nii.gz
* lut : (0, 0, 2, 1, 3, 3, 0, 2, 1, 1, 1, 1, 1, 1, 3, 3, 2, 1, 1, 1, 1, 0, 0, 0, 3, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 3, 3, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2)
* newpath : <undefined>


Execution Inputs
----------------


* function_str : def apply_lut(in_dseg, lut, newpath=None):
    """Map the input discrete segmentation to a new label set (lookup table, LUT)."""
    import numpy as np
    import nibabel as nb
    from nipype.utils.filemanip import fname_presuffix

    if newpath is None:
        from os import getcwd
        newpath = getcwd()

    out_file = fname_presuffix(in_dseg, suffix='_dseg', newpath=newpath)
    lut = np.array(lut, dtype='int16')

    segm = nb.load(in_dseg)
    hdr = segm.header.copy()
    hdr.set_data_dtype('int16')
    segm.__class__(lut[np.asanyarray(segm.dataobj, dtype=int)].astype('int16'),
                   segm.affine, hdr).to_filename(out_file)

    return out_file

* in_dseg : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/segs_to_native_aseg/resample/seg.nii.gz
* lut : (0, 0, 2, 1, 3, 3, 0, 2, 1, 1, 1, 1, 1, 1, 3, 3, 2, 1, 1, 1, 1, 0, 0, 0, 3, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 3, 3, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2)
* newpath : <undefined>


Execution Outputs
-----------------


* out : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/lut_t1w_dseg/seg_dseg.nii.gz


Runtime info
------------


* duration : 0.049128
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/lut_t1w_dseg


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

