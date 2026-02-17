Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (atropos_wf (14_sel_labels2 (utility)
======================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.atropos_wf.14_sel_labels2
 Exec ID : 14_sel_labels2


Original Inputs
---------------


* function_str : def _select_labels(in_segm, labels):
    from os import getcwd
    import numpy as np
    import nibabel as nb
    from nipype.utils.filemanip import fname_presuffix

    out_files = []

    cwd = getcwd()
    nii = nb.load(in_segm)
    label_data = np.asanyarray(nii.dataobj).astype("uint8")
    for label in labels:
        newnii = nii.__class__(np.uint8(label_data == label), nii.affine, nii.header)
        newnii.set_data_dtype("uint8")
        out_file = fname_presuffix(in_segm, suffix="_class-%02d" % label, newpath=cwd)
        newnii.to_filename(out_file)
        out_files.append(out_file)
    return out_files

* in_segm : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/13_add_gm_wm/09_relabel_wm_maths.nii.gz
* labels : [2, 3]


Execution Inputs
----------------


* function_str : def _select_labels(in_segm, labels):
    from os import getcwd
    import numpy as np
    import nibabel as nb
    from nipype.utils.filemanip import fname_presuffix

    out_files = []

    cwd = getcwd()
    nii = nb.load(in_segm)
    label_data = np.asanyarray(nii.dataobj).astype("uint8")
    for label in labels:
        newnii = nii.__class__(np.uint8(label_data == label), nii.affine, nii.header)
        newnii.set_data_dtype("uint8")
        out_file = fname_presuffix(in_segm, suffix="_class-%02d" % label, newpath=cwd)
        newnii.to_filename(out_file)
        out_files.append(out_file)
    return out_files

* in_segm : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/13_add_gm_wm/09_relabel_wm_maths.nii.gz
* labels : [2, 3]


Execution Outputs
-----------------


* out_gm : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/14_sel_labels2/09_relabel_wm_maths_class-02.nii.gz
* out_wm : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/14_sel_labels2/09_relabel_wm_maths_class-03.nii.gz


Runtime info
------------


* duration : 0.047562
* hostname : 87a7076871ed
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/atropos_wf/14_sel_labels2


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

