Node: single_subject_01_wf (anat_preproc_wf (surface_recon_wf (gifti_surface_wf (fix_surfs (surf)
=================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.surface_recon_wf.gifti_surface_wf.fix_surfs
 Exec ID : fix_surfs


Original Inputs
---------------


* in_file : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii0/rh.smoothwm_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii1/lh.smoothwm_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii2/lh.pial_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii3/rh.pial_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii4/lh.inflated_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii5/rh.inflated_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii6/rh.midthickness_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii7/lh.midthickness_converted.gii']
* transform_file : <undefined>


Execution Inputs
----------------


* in_file : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii0/rh.smoothwm_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii1/lh.smoothwm_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii2/lh.pial_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii3/rh.pial_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii4/lh.inflated_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii5/rh.inflated_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii6/rh.midthickness_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fs2gii/mapflow/_fs2gii7/lh.midthickness_converted.gii']
* transform_file : <undefined>


Execution Outputs
-----------------


* out_file : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs0/rh.smoothwm_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs1/lh.smoothwm_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs2/lh.pial_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs3/rh.pial_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs4/lh.inflated_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs5/rh.inflated_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs6/rh.midthickness_converted.gii', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs7/lh.midthickness_converted.gii']


Subnode reports
---------------


 subnode 0 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs0/_report/report.rst
 subnode 1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs1/_report/report.rst
 subnode 2 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs2/_report/report.rst
 subnode 3 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs3/_report/report.rst
 subnode 4 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs4/_report/report.rst
 subnode 5 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs5/_report/report.rst
 subnode 6 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs6/_report/report.rst
 subnode 7 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs7/_report/report.rst

