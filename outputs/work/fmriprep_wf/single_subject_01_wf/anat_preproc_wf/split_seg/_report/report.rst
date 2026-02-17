Node: single_subject_01_wf (anat_preproc_wf (split_seg (utility)
================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.split_seg
 Exec ID : split_seg


Original Inputs
---------------


* function_str : def _split_segments(in_file):
    from pathlib import Path
    import numpy as np
    import nibabel as nb

    segimg = nb.load(in_file)
    data = np.int16(segimg.dataobj)
    hdr = segimg.header.copy()
    hdr.set_data_dtype('uint8')

    out_files = []
    for i, label in enumerate(("GM", "WM", "CSF"), 1):
        out_fname = str(Path.cwd() / f"aseg_label-{label}_mask.nii.gz")
        segimg.__class__(data == i, segimg.affine, hdr).to_filename(out_fname)
        out_files.append(out_fname)

    return out_files

* in_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/lut_t1w_dseg/seg_dseg.nii.gz


Execution Inputs
----------------


* function_str : def _split_segments(in_file):
    from pathlib import Path
    import numpy as np
    import nibabel as nb

    segimg = nb.load(in_file)
    data = np.int16(segimg.dataobj)
    hdr = segimg.header.copy()
    hdr.set_data_dtype('uint8')

    out_files = []
    for i, label in enumerate(("GM", "WM", "CSF"), 1):
        out_fname = str(Path.cwd() / f"aseg_label-{label}_mask.nii.gz")
        segimg.__class__(data == i, segimg.affine, hdr).to_filename(out_fname)
        out_files.append(out_fname)

    return out_files

* in_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/lut_t1w_dseg/seg_dseg.nii.gz


Execution Outputs
-----------------


* out : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-GM_mask.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-WM_mask.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg/aseg_label-CSF_mask.nii.gz']


Runtime info
------------


* duration : 0.024865
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/split_seg


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

