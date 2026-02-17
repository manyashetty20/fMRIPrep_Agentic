Node: single_subject_01_wf (anat_preproc_wf (anat_derivatives_wf (ds_surfs)
===========================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.anat_derivatives_wf.ds_surfs
 Exec ID : ds_surfs


Original Inputs
---------------


* acquisition : <undefined>
* atlas : <undefined>
* base_directory : /out
* ceagent : <undefined>
* check_hdr : True
* cohort : <undefined>
* compress : <undefined>
* data_dtype : <undefined>
* datatype : <undefined>
* density : <undefined>
* desc : <undefined>
* direction : <undefined>
* dismiss_entities : <undefined>
* echo : <undefined>
* extension : .surf.gii
* fmap : <undefined>
* from : <undefined>
* hemi : ['R', 'L', 'L', 'R', 'L', 'R', 'R', 'L']
* in_file : [['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs0/rh.smoothwm_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs1/lh.smoothwm_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs2/lh.pial_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs3/rh.pial_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs4/lh.inflated_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs5/rh.inflated_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs6/rh.midthickness_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs7/lh.midthickness_converted.gii']]
* label : <undefined>
* meta_dict : <undefined>
* modality : <undefined>
* mode : <undefined>
* model : <undefined>
* proc : <undefined>
* reconstruction : <undefined>
* recording : <undefined>
* resolution : <undefined>
* roi : <undefined>
* run : <undefined>
* scans : <undefined>
* session : <undefined>
* source_file : <undefined>
* space : <undefined>
* subject : <undefined>
* subset : <undefined>
* suffix : ['smoothwm', 'smoothwm', 'pial', 'pial', 'inflated', 'inflated', 'midthickness', 'midthickness']
* task : <undefined>
* to : <undefined>


Execution Inputs
----------------


* acquisition : <undefined>
* atlas : <undefined>
* base_directory : /out
* ceagent : <undefined>
* check_hdr : True
* cohort : <undefined>
* compress : <undefined>
* data_dtype : <undefined>
* datatype : <undefined>
* density : <undefined>
* desc : <undefined>
* direction : <undefined>
* dismiss_entities : <undefined>
* echo : <undefined>
* extension : .surf.gii
* fmap : <undefined>
* from : <undefined>
* hemi : ['R', 'L', 'L', 'R', 'L', 'R', 'R', 'L']
* in_file : [['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs0/rh.smoothwm_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs1/lh.smoothwm_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs2/lh.pial_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs3/rh.pial_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs4/lh.inflated_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs5/rh.inflated_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs6/rh.midthickness_converted.gii'], ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/gifti_surface_wf/fix_surfs/mapflow/_fix_surfs7/lh.midthickness_converted.gii']]
* label : <undefined>
* meta_dict : <undefined>
* modality : <undefined>
* mode : <undefined>
* model : <undefined>
* proc : <undefined>
* reconstruction : <undefined>
* recording : <undefined>
* resolution : <undefined>
* roi : <undefined>
* run : <undefined>
* scans : <undefined>
* session : <undefined>
* source_file : <undefined>
* space : <undefined>
* subject : <undefined>
* subset : <undefined>
* suffix : ['smoothwm', 'smoothwm', 'pial', 'pial', 'inflated', 'inflated', 'midthickness', 'midthickness']
* task : <undefined>
* to : <undefined>


Execution Outputs
-----------------


* compression : [False, False, False, False, False, False, False, False]
* fixed_hdr : [[False], [False], [False], [False], [False], [False], [False], [False]]
* out_file : ['/out/fmriprep/sub-01/anat/sub-01_hemi-R_smoothwm.surf.gii', '/out/fmriprep/sub-01/anat/sub-01_hemi-L_smoothwm.surf.gii', '/out/fmriprep/sub-01/anat/sub-01_hemi-L_pial.surf.gii', '/out/fmriprep/sub-01/anat/sub-01_hemi-R_pial.surf.gii', '/out/fmriprep/sub-01/anat/sub-01_hemi-L_inflated.surf.gii', '/out/fmriprep/sub-01/anat/sub-01_hemi-R_inflated.surf.gii', '/out/fmriprep/sub-01/anat/sub-01_hemi-R_midthickness.surf.gii', '/out/fmriprep/sub-01/anat/sub-01_hemi-L_midthickness.surf.gii']
* out_meta : <undefined>


Subnode reports
---------------


 subnode 0 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs0/_report/report.rst
 subnode 1 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs1/_report/report.rst
 subnode 2 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs2/_report/report.rst
 subnode 3 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs3/_report/report.rst
 subnode 4 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs4/_report/report.rst
 subnode 5 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs5/_report/report.rst
 subnode 6 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs6/_report/report.rst
 subnode 7 : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_derivatives_wf/ds_surfs/mapflow/_ds_surfs7/_report/report.rst

