Node: single_subject_01_wf (anat_preproc_wf (surface_recon_wf (autorecon_resume_wf (autorecon2_vol (freesurfer)
===============================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.surface_recon_wf.autorecon_resume_wf.autorecon2_vol
 Exec ID : autorecon2_vol


Original Inputs
---------------


* FLAIR_file : <undefined>
* T1_files : <undefined>
* T2_file : <undefined>
* args : <undefined>
* big_ventricles : <undefined>
* brainstem : <undefined>
* directive : autorecon2-volonly
* environ : {}
* expert : <undefined>
* flags : <undefined>
* hemi : <undefined>
* hippocampal_subfields_T1 : <undefined>
* hippocampal_subfields_T2 : <undefined>
* hires : <undefined>
* mprage : <undefined>
* mri_aparc2aseg : <undefined>
* mri_ca_label : <undefined>
* mri_ca_normalize : <undefined>
* mri_ca_register : <undefined>
* mri_edit_wm_with_aseg : <undefined>
* mri_em_register : <undefined>
* mri_fill : <undefined>
* mri_mask : <undefined>
* mri_normalize : <undefined>
* mri_pretess : <undefined>
* mri_remove_neck : <undefined>
* mri_segment : <undefined>
* mri_segstats : <undefined>
* mri_tessellate : <undefined>
* mri_watershed : <undefined>
* mris_anatomical_stats : <undefined>
* mris_ca_label : <undefined>
* mris_fix_topology : <undefined>
* mris_inflate : <undefined>
* mris_make_surfaces : <undefined>
* mris_register : <undefined>
* mris_smooth : <undefined>
* mris_sphere : <undefined>
* mris_surf2vol : <undefined>
* mrisp_paint : <undefined>
* openmp : 8
* parallel : <undefined>
* steps : <undefined>
* subject_id : sub-01
* subjects_dir : /out/freesurfer
* talairach : <undefined>
* use_FLAIR : <undefined>
* use_T2 : <undefined>
* xopts : <undefined>


Execution Inputs
----------------


* FLAIR_file : <undefined>
* T1_files : <undefined>
* T2_file : <undefined>
* args : <undefined>
* big_ventricles : <undefined>
* brainstem : <undefined>
* directive : autorecon2-volonly
* environ : {}
* expert : <undefined>
* flags : <undefined>
* hemi : <undefined>
* hippocampal_subfields_T1 : <undefined>
* hippocampal_subfields_T2 : <undefined>
* hires : <undefined>
* mprage : <undefined>
* mri_aparc2aseg : <undefined>
* mri_ca_label : <undefined>
* mri_ca_normalize : <undefined>
* mri_ca_register : <undefined>
* mri_edit_wm_with_aseg : <undefined>
* mri_em_register : <undefined>
* mri_fill : <undefined>
* mri_mask : <undefined>
* mri_normalize : <undefined>
* mri_pretess : <undefined>
* mri_remove_neck : <undefined>
* mri_segment : <undefined>
* mri_segstats : <undefined>
* mri_tessellate : <undefined>
* mri_watershed : <undefined>
* mris_anatomical_stats : <undefined>
* mris_ca_label : <undefined>
* mris_fix_topology : <undefined>
* mris_inflate : <undefined>
* mris_make_surfaces : <undefined>
* mris_register : <undefined>
* mris_smooth : <undefined>
* mris_sphere : <undefined>
* mris_surf2vol : <undefined>
* mrisp_paint : <undefined>
* openmp : 8
* parallel : <undefined>
* steps : <undefined>
* subject_id : sub-01
* subjects_dir : /out/freesurfer
* talairach : <undefined>
* use_FLAIR : <undefined>
* use_T2 : <undefined>
* xopts : <undefined>


Execution Outputs
-----------------


* BA_stats : <undefined>
* T1 : <undefined>
* annot : <undefined>
* aparc_a2009s_stats : <undefined>
* aparc_aseg : <undefined>
* aparc_stats : <undefined>
* area_pial : <undefined>
* aseg : <undefined>
* aseg_stats : <undefined>
* avg_curv : <undefined>
* brain : <undefined>
* brainmask : <undefined>
* curv : <undefined>
* curv_pial : <undefined>
* curv_stats : <undefined>
* entorhinal_exvivo_stats : <undefined>
* filled : <undefined>
* graymid : <undefined>
* inflated : <undefined>
* jacobian_white : <undefined>
* label : <undefined>
* norm : <undefined>
* nu : <undefined>
* orig : <undefined>
* pial : <undefined>
* rawavg : <undefined>
* ribbon : <undefined>
* smoothwm : <undefined>
* sphere : <undefined>
* sphere_reg : <undefined>
* subject_id : sub-01
* subjects_dir : /out/freesurfer
* sulc : <undefined>
* thickness : <undefined>
* volume : <undefined>
* white : <undefined>
* wm : <undefined>
* wmparc : <undefined>
* wmparc_stats : <undefined>


Runtime info
------------


* cmdline : recon-all -autorecon2-volonly -openmp 8 -subjid sub-01 -sd /out/freesurfer -nogcareg -nocanorm -nocareg -nonormalization2 -nomaskbfs -nosegmentation -nofill
* duration : 2665.126633
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/autorecon_resume_wf/autorecon2_vol


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 Subject Stamp: freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1-f53a55a
Current Stamp: freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1-f53a55a
INFO: SUBJECTS_DIR is /out/freesurfer
Actual FREESURFER_HOME /opt/freesurfer
-rw-r--r-- 1 root root 258000 Feb 16 17:30 /out/freesurfer/sub-01/scripts/recon-all.log
Linux efad4839b3da 6.12.54-linuxkit #1 SMP Tue Nov  4 21:21:47 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
'/opt/freesurfer/bin/recon-all' -> '/out/freesurfer/sub-01/scripts/recon-all.local-copy'
#--------------------------------------
#@# SubCort Seg Mon Feb 16 17:33:40 UTC 2026

 mri_seg_diff --seg1 aseg.auto.mgz --seg2 aseg.presurf.mgz --diff aseg.manedit.mgz 


$Id: mri_seg_diff.c,v 1.5 2011/03/02 00:04:24 nicks Exp $
cwd /out/freesurfer/sub-01/mri
cmdline mri_seg_diff --seg1 aseg.auto.mgz --seg2 aseg.presurf.mgz --diff aseg.manedit.mgz 
sysname  Linux
hostname efad4839b3da
machine  x86_64
user     root
Seg1     aseg.auto.mgz
Seg2     aseg.presurf.mgz
Diff     aseg.manedit.mgz
InDiff   (null)
Merged   (null)
ForceDiff 0
Computing difference between segmentations
No difference found.

 mri_ca_label -relabel_unlikely 9 .3 -prior 0.5 -align norm.mgz transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca aseg.auto_noCCseg.mgz 

sysname  Linux
hostname efad4839b3da
machine  x86_64

setenv SUBJECTS_DIR /out/freesurfer
cd /out/freesurfer/sub-01/mri
mri_ca_label -relabel_unlikely 9 .3 -prior 0.5 -align norm.mgz transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca aseg.auto_noCCseg.mgz 


== Number of threads available to mri_ca_label for OpenMP = 8 == 
relabeling unlikely voxels with window_size = 9 and prior threshold 0.30
using Gibbs prior factor = 0.500
renormalizing sequences with structure alignment, equivalent to:
	-renormalize
	-renormalize_mean 0.500
	-regularize 0.500
reading 1 input volumes
reading classifier array from /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca
reading input volume from norm.mgz
average std[0] = 7.3
reading transform from transforms/talairach.m3z
setting orig areas to linear transform determinant scaled 1.14
Atlas used for the 3D morph was /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca
average std = 7.3   using min determinant for regularization = 5.3
0 singular and 0 ill-conditioned covariance matrices regularized
labeling volume...
renormalizing by structure alignment....
renormalizing input #0
gca peak = 0.16259 (20)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.17677 (13)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.28129 (95)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.16930 (96)
mri peak = 0.08167 (87)
gca peak = 0.24553 (55)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.30264 (59)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.07580 (103)
mri peak = 0.10353 (105)
Right_Cerebral_White_Matter (41): linear fit = 1.01 x + 0.0 (324 voxels, overlap=0.778)
Right_Cerebral_White_Matter (41): linear fit = 1.01 x + 0.0 (324 voxels, peak = 105), gca=104.5
gca peak = 0.07714 (104)
mri peak = 0.07744 (98)
Left_Cerebral_White_Matter (2): linear fit = 0.98 x + 0.0 (631 voxels, overlap=0.858)
Left_Cerebral_White_Matter (2): linear fit = 0.98 x + 0.0 (631 voxels, peak = 101), gca=101.4
gca peak = 0.09712 (58)
mri peak = 0.04021 (58)
Left_Cerebral_Cortex (3): linear fit = 1.36 x + 0.0 (75 voxels, overlap=0.417)
Left_Cerebral_Cortex (3): linear fit = 1.36 x + 0.0 (75 voxels, peak = 79), gca=78.6
gca peak = 0.11620 (58)
mri peak = 0.06825 (61)
Right_Cerebral_Cortex (42): linear fit = 1.04 x + 0.0 (277 voxels, overlap=0.835)
Right_Cerebral_Cortex (42): linear fit = 1.04 x + 0.0 (277 voxels, peak = 61), gca=60.6
gca peak = 0.30970 (66)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.15280 (69)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.13902 (56)
mri peak = 0.05326 (70)
Left_Cerebellum_Cortex (8): linear fit = 1.13 x + 0.0 (418 voxels, overlap=0.669)
Left_Cerebellum_Cortex (8): linear fit = 1.13 x + 0.0 (418 voxels, peak = 64), gca=63.6
gca peak = 0.14777 (55)
mri peak = 0.05882 (50)
Right_Cerebellum_Cortex (47): linear fit = 0.88 x + 0.0 (628 voxels, overlap=0.774)
Right_Cerebellum_Cortex (47): linear fit = 0.88 x + 0.0 (628 voxels, peak = 49), gca=48.7
gca peak = 0.16765 (84)
mri peak = 0.15489 (67)
gca peak = 0.18739 (84)
mri peak = 0.07975 (55)
gca peak = 0.29869 (57)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.33601 (57)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.11131 (90)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.11793 (83)
mri peak = 0.08346 (90)
gca peak = 0.08324 (81)
mri peak = 0.17391 (92)
Left_Putamen (12): linear fit = 1.22 x + 0.0 (377 voxels, overlap=0.008)
Left_Putamen (12): linear fit = 1.22 x + 0.0 (377 voxels, peak = 98), gca=98.4
gca peak = 0.10360 (77)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.08424 (78)
mri peak = 0.09836 (93)
Brain_Stem (16): linear fit = 1.18 x + 0.0 (254 voxels, overlap=0.049)
Brain_Stem (16): linear fit = 1.18 x + 0.0 (254 voxels, peak = 92), gca=92.4
gca peak = 0.12631 (89)
mri peak = 0.11543 (98)
gca peak = 0.14500 (87)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.14975 (24)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.19357 (14)
uniform distribution in MR - rejecting arbitrary fit
gca peak Unknown = 0.94835 ( 0)
gca peak Left_Lateral_Ventricle = 0.16259 (20)
gca peak Left_Inf_Lat_Vent = 0.16825 (27)
gca peak Left_Cerebellum_White_Matter = 0.16765 (84)
gca peak Left_Thalamus = 1.00000 (94)
gca peak Left_Thalamus_Proper = 0.11131 (90)
gca peak Left_Caudate = 0.15280 (69)
gca peak Left_Pallidum = 0.16930 (96)
gca peak Third_Ventricle = 0.14975 (24)
gca peak Fourth_Ventricle = 0.19357 (14)
gca peak Left_Hippocampus = 0.30264 (59)
gca peak Left_Amygdala = 0.29869 (57)
gca peak CSF = 0.23379 (36)
gca peak Left_Accumbens_area = 0.70037 (62)
gca peak Left_VentralDC = 0.14500 (87)
gca peak Left_undetermined = 1.00000 (26)
gca peak Left_vessel = 0.75997 (52)
gca peak Left_choroid_plexus = 0.12089 (35)
gca peak Right_Lateral_Ventricle = 0.17677 (13)
gca peak Right_Inf_Lat_Vent = 0.24655 (23)
gca peak Right_Cerebellum_White_Matter = 0.18739 (84)
gca peak Right_Thalamus_Proper = 0.11793 (83)
gca peak Right_Caudate = 0.30970 (66)
gca peak Right_Putamen = 0.10360 (77)
gca peak Right_Pallidum = 0.28129 (95)
gca peak Right_Hippocampus = 0.24553 (55)
gca peak Right_Amygdala = 0.33601 (57)
gca peak Right_Accumbens_area = 0.45042 (65)
gca peak Right_VentralDC = 0.12631 (89)
gca peak Right_vessel = 0.82168 (52)
gca peak Right_choroid_plexus = 0.14516 (37)
gca peak Fifth_Ventricle = 0.65475 (32)
gca peak WM_hypointensities = 0.07854 (76)
gca peak non_WM_hypointensities = 0.08491 (43)
gca peak Optic_Chiasm = 0.71127 (75)
not using caudate to estimate GM means
setting label Right_Putamen based on Left_Putamen = 1.22 x +  0: 98
estimating mean gm scale to be 1.20 x + 0.0
estimating mean wm scale to be 1.00 x + 0.0
estimating mean csf scale to be 1.00 x + 0.0
Left_Putamen too bright - rescaling by 0.942 (from 1.215) to 92.7 (was 98.4)
Left_Pallidum too bright - rescaling by 0.867 (from 1.200) to 99.9 (was 115.2)
Right_Putamen too bright - rescaling by 0.942 (from 1.215) to 92.7 (was 98.4)
Right_Pallidum too bright - rescaling by 0.876 (from 1.200) to 99.9 (was 114.0)
saving intensity scales to aseg.auto_noCCseg.label_intensities.txt
renormalizing by structure alignment....
renormalizing input #0
gca peak = 0.16259 (20)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.17677 (13)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.24186 (98)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.17724 (100)
mri peak = 0.08167 (87)
gca peak = 0.22508 (67)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.24896 (71)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.07753 (104)
mri peak = 0.10353 (105)
Right_Cerebral_White_Matter (41): linear fit = 1.00 x + 0.0 (324 voxels, overlap=0.834)
Right_Cerebral_White_Matter (41): linear fit = 1.00 x + 0.0 (324 voxels, peak = 104), gca=104.0
gca peak = 0.08002 (102)
mri peak = 0.07744 (98)
Left_Cerebral_White_Matter (2): linear fit = 1.00 x + 0.0 (631 voxels, overlap=0.895)
Left_Cerebral_White_Matter (2): linear fit = 1.00 x + 0.0 (631 voxels, peak = 102), gca=102.0
gca peak = 0.07169 (79)
mri peak = 0.04021 (58)
Left_Cerebral_Cortex (3): linear fit = 1.04 x + 0.0 (75 voxels, overlap=0.386)
Left_Cerebral_Cortex (3): linear fit = 1.04 x + 0.0 (75 voxels, peak = 83), gca=82.6
gca peak = 0.11294 (61)
mri peak = 0.06825 (61)
Right_Cerebral_Cortex (42): linear fit = 0.99 x + 0.0 (277 voxels, overlap=0.879)
Right_Cerebral_Cortex (42): linear fit = 0.99 x + 0.0 (277 voxels, peak = 60), gca=60.1
gca peak = 0.24453 (80)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.15637 (82)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.12548 (63)
mri peak = 0.05326 (70)
Left_Cerebellum_Cortex (8): linear fit = 1.00 x + 0.0 (418 voxels, overlap=0.888)
Left_Cerebellum_Cortex (8): linear fit = 1.00 x + 0.0 (418 voxels, peak = 63), gca=63.0
gca peak = 0.16238 (49)
mri peak = 0.05882 (50)
Right_Cerebellum_Cortex (47): linear fit = 1.00 x + 0.0 (628 voxels, overlap=0.995)
Right_Cerebellum_Cortex (47): linear fit = 1.00 x + 0.0 (628 voxels, peak = 49), gca=49.0
gca peak = 0.16676 (84)
mri peak = 0.15489 (67)
gca peak = 0.15979 (84)
mri peak = 0.07975 (55)
gca peak = 0.32470 (68)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.36403 (68)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.10557 (106)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.09239 (103)
mri peak = 0.08346 (90)
gca peak = 0.08438 (86)
mri peak = 0.17391 (92)
Left_Putamen (12): linear fit = 1.05 x + 0.0 (377 voxels, overlap=0.364)
Left_Putamen (12): linear fit = 1.05 x + 0.0 (377 voxels, peak = 91), gca=90.7
gca peak = 0.08525 (88)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.07883 (93)
mri peak = 0.09836 (93)
Brain_Stem (16): linear fit = 1.02 x + 0.0 (254 voxels, overlap=0.684)
Brain_Stem (16): linear fit = 1.02 x + 0.0 (254 voxels, peak = 95), gca=95.3
gca peak = 0.10036 (86)
mri peak = 0.11543 (98)
gca peak = 0.11512 (87)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.14975 (24)
uniform distribution in MR - rejecting arbitrary fit
gca peak = 0.19357 (14)
uniform distribution in MR - rejecting arbitrary fit
gca peak Unknown = 0.94835 ( 0)
gca peak Left_Lateral_Ventricle = 0.16259 (20)
gca peak Left_Inf_Lat_Vent = 0.16825 (27)
gca peak Left_Cerebellum_White_Matter = 0.16676 (84)
gca peak Left_Thalamus = 1.00000 (113)
gca peak Left_Thalamus_Proper = 0.10557 (106)
gca peak Left_Caudate = 0.15637 (82)
gca peak Left_Pallidum = 0.17724 (100)
gca peak Third_Ventricle = 0.14975 (24)
gca peak Fourth_Ventricle = 0.19357 (14)
gca peak Left_Hippocampus = 0.24896 (71)
gca peak Left_Amygdala = 0.32470 (68)
gca peak CSF = 0.23379 (36)
gca peak Left_Accumbens_area = 0.63945 (75)
gca peak Left_VentralDC = 0.11512 (87)
gca peak Left_undetermined = 1.00000 (26)
gca peak Left_vessel = 0.75997 (52)
gca peak Left_choroid_plexus = 0.12089 (35)
gca peak Right_Lateral_Ventricle = 0.17677 (13)
gca peak Right_Inf_Lat_Vent = 0.24655 (23)
gca peak Right_Cerebellum_White_Matter = 0.15979 (84)
gca peak Right_Thalamus_Proper = 0.09239 (103)
gca peak Right_Caudate = 0.24453 (80)
gca peak Right_Putamen = 0.08525 (88)
gca peak Right_Pallidum = 0.24186 (98)
gca peak Right_Hippocampus = 0.22508 (67)
gca peak Right_Amygdala = 0.36403 (68)
gca peak Right_Accumbens_area = 0.26330 (79)
gca peak Right_VentralDC = 0.10036 (86)
gca peak Right_vessel = 0.82168 (52)
gca peak Right_choroid_plexus = 0.14516 (37)
gca peak Fifth_Ventricle = 0.65475 (32)
gca peak WM_hypointensities = 0.07971 (76)
gca peak non_WM_hypointensities = 0.11534 (54)
gca peak Optic_Chiasm = 0.69231 (75)
not using caudate to estimate GM means
setting label Right_Putamen based on Left_Putamen = 1.05 x +  0: 91
estimating mean gm scale to be 1.01 x + 0.0
estimating mean wm scale to be 1.00 x + 0.0
estimating mean csf scale to be 1.00 x + 0.0
Left_Pallidum too bright - rescaling by 0.984 (from 1.015) to 99.9 (was 101.5)
Right_Pallidum too bright - rescaling by 1.004 (from 1.015) to 99.9 (was 99.5)
saving intensity scales to aseg.auto_noCCseg.label_intensities.txt
saving sequentially combined intensity scales to aseg.auto_noCCseg.label_intensities.txt
16344 voxels changed in iteration 0 of unlikely voxel relabeling
117 voxels changed in iteration 1 of unlikely voxel relabeling
4 voxels changed in iteration 2 of unlikely voxel relabeling
0 voxels changed in iteration 3 of unlikely voxel relabeling
9066 gm and wm labels changed (%34 to gray, %66 to white out of all changed labels)
89 hippocampal voxels changed.
0 amygdala voxels changed.
pass 1: 17684 changed. image ll: -1.946, PF=0.500
pass 2: 4462 changed.
8564 voxels changed in iteration 0 of unlikely voxel relabeling
47 voxels changed in iteration 1 of unlikely voxel relabeling
0 voxels changed in iteration 2 of unlikely voxel relabeling
1726 voxels changed in iteration 0 of unlikely voxel relabeling
2 voxels changed in iteration 1 of unlikely voxel relabeling
0 voxels changed in iteration 2 of unlikely voxel relabeling
1567 voxels changed in iteration 0 of unlikely voxel relabeling
53 voxels changed in iteration 1 of unlikely voxel relabeling
0 voxels changed in iteration 2 of unlikely voxel relabeling
1549 voxels changed in iteration 0 of unlikely voxel relabeling
19 voxels changed in iteration 1 of unlikely voxel relabeling
0 voxels changed in iteration 2 of unlikely voxel relabeling
MRItoUCHAR: min=0, max=85
MRItoUCHAR: converting to UCHAR
writing labeled volume to aseg.auto_noCCseg.mgz
mri_ca_label utimesec    2656.502305
mri_ca_label stimesec    5.391138
mri_ca_label ru_maxrss   2776548
mri_ca_label ru_ixrss    0
mri_ca_label ru_idrss    0
mri_ca_label ru_isrss    0
mri_ca_label ru_minflt   595432
mri_ca_label ru_majflt   31
mri_ca_label ru_nswap    0
mri_ca_label ru_inblock  37992
mri_ca_label ru_oublock  111
mri_ca_label ru_msgsnd   0
mri_ca_label ru_msgrcv   0
mri_ca_label ru_nsignals 0
mri_ca_label ru_nvcsw    2509
mri_ca_label ru_nivcsw   15366
auto-labeling took 41 minutes and 55 seconds.

 mri_cc -aseg aseg.auto_noCCseg.mgz -o aseg.auto.mgz -lta /out/freesurfer/sub-01/mri/transforms/cc_up.lta sub-01 

will read input aseg from aseg.auto_noCCseg.mgz
writing aseg with cc labels to aseg.auto.mgz
will write lta as /out/freesurfer/sub-01/mri/transforms/cc_up.lta
reading aseg from /out/freesurfer/sub-01/mri/aseg.auto_noCCseg.mgz
reading norm from /out/freesurfer/sub-01/mri/norm.mgz
21334 voxels in left wm, 41319 in right wm, xrange [107, 142]
searching rotation angles z=[ 8 22], y=[30 44]

searching scale 1 Z rot 8.0  
searching scale 1 Z rot 8.2  
searching scale 1 Z rot 8.5  
searching scale 1 Z rot 8.7  
searching scale 1 Z rot 9.0  
searching scale 1 Z rot 9.2  
searching scale 1 Z rot 9.5  
searching scale 1 Z rot 9.7  
searching scale 1 Z rot 10.0  
searching scale 1 Z rot 10.2  
searching scale 1 Z rot 10.5  
searching scale 1 Z rot 10.7  
searching scale 1 Z rot 11.0  
searching scale 1 Z rot 11.2  
searching scale 1 Z rot 11.5  
searching scale 1 Z rot 11.7  
searching scale 1 Z rot 12.0  
searching scale 1 Z rot 12.2  
searching scale 1 Z rot 12.5  
searching scale 1 Z rot 12.7  
searching scale 1 Z rot 13.0  
searching scale 1 Z rot 13.2  
searching scale 1 Z rot 13.5  
searching scale 1 Z rot 13.7  
searching scale 1 Z rot 14.0  
searching scale 1 Z rot 14.2  
searching scale 1 Z rot 14.5  
searching scale 1 Z rot 14.7  
searching scale 1 Z rot 15.0  
searching scale 1 Z rot 15.2  
searching scale 1 Z rot 15.5  
searching scale 1 Z rot 15.7  
searching scale 1 Z rot 16.0  
searching scale 1 Z rot 16.2  
searching scale 1 Z rot 16.5  
searching scale 1 Z rot 16.7  
searching scale 1 Z rot 17.0  
searching scale 1 Z rot 17.2  
searching scale 1 Z rot 17.5  
searching scale 1 Z rot 17.7  
searching scale 1 Z rot 18.0  
searching scale 1 Z rot 18.2  
searching scale 1 Z rot 18.5  
searching scale 1 Z rot 18.7  
searching scale 1 Z rot 19.0  global minimum found at slice 125.0, rotations (40.64, 12.25)
final transformation (x=125.0, yr=40.642, zr=12.249):
 0.74152  -0.21215   0.63651  -24.73534;
 0.16098   0.97724   0.13818  -17.72052;
-0.65133   0.00000   0.75879   110.01535;
 0.00000   0.00000   0.00000   1.00000;
updating x range to be [118, 135] in xformed coordinates
best xformed slice 130
cc center is found at 130 110 131
eigenvectors:
 0.02627  -0.06905   0.99727;
 0.08245  -0.99406  -0.07100;
 0.99625   0.08409  -0.02042;
writing aseg with callosum to /out/freesurfer/sub-01/mri/aseg.auto.mgz...
corpus callosum segmentation took 2.4 minutes
#--------------------------------------
#@# Merge ASeg Mon Feb 16 18:18:01 UTC 2026

 cp aseg.auto.mgz aseg.presurf.mgz 


Started at Mon Feb 16 17:33:37 UTC 2026 
Ended   at Mon Feb 16 18:18:01 UTC 2026
#@#%# recon-all-run-time-hours 0.740
recon-all -s sub-01 finished without error at Mon Feb 16 18:18:01 UTC 2026
done


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

