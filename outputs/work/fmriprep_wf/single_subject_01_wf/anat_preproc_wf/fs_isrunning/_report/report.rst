Node: single_subject_01_wf (anat_preproc_wf (fs_isrunning (utility)
===================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.fs_isrunning
 Exec ID : fs_isrunning


Original Inputs
---------------


* function_str : def fs_isRunning(subjects_dir, subject_id, mtime_tol=86400, logger=None):
    """
    Checks FreeSurfer subjects dir for presence of recon-all blocking ``IsRunning`` files,
    and optionally removes any based on the modification time.

    Parameters
    ----------
    subjects_dir : os.PathLike or None
        Existing FreeSurfer subjects directory
    subject_id : str
        Subject label
    mtime_tol : int
        Tolerance time (in seconds) between current time and last modification of ``recon-all.log``

    Returns
    -------
    subjects_dir : os.PathLike or None

    """
    from pathlib import Path
    import time

    if subjects_dir is None:
        return subjects_dir
    subj_dir = Path(subjects_dir) / subject_id
    if not subj_dir.exists():
        return subjects_dir

    isrunning = tuple(subj_dir.glob("scripts/IsRunning*"))
    if not isrunning:
        return subjects_dir
    reconlog = subj_dir / "scripts" / "recon-all.log"
    # if recon log doesn't exist, just clear IsRunning
    mtime = reconlog.stat().st_mtime if reconlog.exists() else 0
    if (time.time() - mtime) < mtime_tol:
        raise RuntimeError(f"""\
The FreeSurfer's subject folder <{subj_dir}> contains IsRunning files that \
may pertain to a current or past execution: {isrunning}.
FreeSurfer cannot run if these are present, to avoid interfering with a running \
process. Please, make sure no other process is running ``recon-all`` on this subject \
and proceed to delete the files listed above.""")
    for fl in isrunning:
        fl.unlink()
    if logger:
        logger.warn(f'Removed "IsRunning*" files found under {subj_dir}')
    return subjects_dir

* logger : <Logger nipype.workflow (INFO)>
* mtime_tol : <undefined>
* subject_id : sub-01
* subjects_dir : /out/freesurfer


Execution Inputs
----------------


* function_str : def fs_isRunning(subjects_dir, subject_id, mtime_tol=86400, logger=None):
    """
    Checks FreeSurfer subjects dir for presence of recon-all blocking ``IsRunning`` files,
    and optionally removes any based on the modification time.

    Parameters
    ----------
    subjects_dir : os.PathLike or None
        Existing FreeSurfer subjects directory
    subject_id : str
        Subject label
    mtime_tol : int
        Tolerance time (in seconds) between current time and last modification of ``recon-all.log``

    Returns
    -------
    subjects_dir : os.PathLike or None

    """
    from pathlib import Path
    import time

    if subjects_dir is None:
        return subjects_dir
    subj_dir = Path(subjects_dir) / subject_id
    if not subj_dir.exists():
        return subjects_dir

    isrunning = tuple(subj_dir.glob("scripts/IsRunning*"))
    if not isrunning:
        return subjects_dir
    reconlog = subj_dir / "scripts" / "recon-all.log"
    # if recon log doesn't exist, just clear IsRunning
    mtime = reconlog.stat().st_mtime if reconlog.exists() else 0
    if (time.time() - mtime) < mtime_tol:
        raise RuntimeError(f"""\
The FreeSurfer's subject folder <{subj_dir}> contains IsRunning files that \
may pertain to a current or past execution: {isrunning}.
FreeSurfer cannot run if these are present, to avoid interfering with a running \
process. Please, make sure no other process is running ``recon-all`` on this subject \
and proceed to delete the files listed above.""")
    for fl in isrunning:
        fl.unlink()
    if logger:
        logger.warn(f'Removed "IsRunning*" files found under {subj_dir}')
    return subjects_dir

* logger : <Logger nipype.workflow (INFO)>
* mtime_tol : <undefined>
* subject_id : sub-01
* subjects_dir : /out/freesurfer


Execution Outputs
-----------------


* out : /out/freesurfer


Runtime info
------------


* duration : 0.011005
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/fs_isrunning


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

