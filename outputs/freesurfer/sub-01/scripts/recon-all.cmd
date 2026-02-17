

#---------------------------------
# New invocation of recon-all Mon Feb 16 10:05:33 UTC 2026 

 mri_convert /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz /out/freesurfer/sub-01/mri/orig/001.mgz 

#--------------------------------------------
#@# MotionCor Mon Feb 16 10:05:52 UTC 2026

 cp /out/freesurfer/sub-01/mri/orig/001.mgz /out/freesurfer/sub-01/mri/rawavg.mgz 


 mri_convert /out/freesurfer/sub-01/mri/rawavg.mgz /out/freesurfer/sub-01/mri/orig.mgz --conform 


 mri_add_xform_to_header -c /out/freesurfer/sub-01/mri/transforms/talairach.xfm /out/freesurfer/sub-01/mri/orig.mgz /out/freesurfer/sub-01/mri/orig.mgz 

#--------------------------------------------
#@# Talairach Mon Feb 16 10:06:08 UTC 2026

 mri_nu_correct.mni --no-rescale --i orig.mgz --o orig_nu.mgz --n 1 --proto-iters 1000 --distance 50 


 talairach_avi --i orig_nu.mgz --xfm transforms/talairach.auto.xfm 

talairach_avi log file is transforms/talairach_avi.log...

 cp transforms/talairach.auto.xfm transforms/talairach.xfm 

#--------------------------------------------
#@# Talairach Failure Detection Mon Feb 16 10:13:45 UTC 2026

 talairach_afd -T 0.005 -xfm transforms/talairach.xfm 

#--------------------------------------------
#@# Talairach Mon Feb 16 10:13:45 UTC 2026

 mri_nu_correct.mni --no-rescale --i orig.mgz --o orig_nu.mgz --n 1 --proto-iters 1000 --distance 50 


 talairach_avi --i orig_nu.mgz --xfm transforms/talairach.auto.xfm --atlas 3T18yoSchwartzReactN32_as_orig 

talairach_avi log file is transforms/talairach_avi.log...

 cp transforms/talairach.auto.xfm transforms/talairach.xfm 

#--------------------------------------------
#@# Talairach Failure Detection Mon Feb 16 10:17:18 UTC 2026

 talairach_afd -T 0.005 -xfm transforms/talairach.xfm 

#--------------------------------------------
#@# Talairach Mon Feb 16 10:17:19 UTC 2026

 mri_nu_correct.mni --no-rescale --i orig.mgz --o orig_nu.mgz --n 1 --proto-iters 1000 --distance 50 


 talairach --i orig_nu.mgz --xfm transforms/talairach.auto.xfm 


 cp transforms/talairach.auto.xfm transforms/talairach.xfm 

#--------------------------------------------
#@# Talairach Failure Detection Mon Feb 16 10:20:28 UTC 2026

 talairach_afd -T 0.005 -xfm transforms/talairach.xfm 



#---------------------------------
# New invocation of recon-all Mon Feb 16 10:31:03 UTC 2026 
#--------------------------------------------
#@# Nu Intensity Correction Mon Feb 16 10:31:10 UTC 2026

 mri_nu_correct.mni --i orig.mgz --o nu.mgz --uchar transforms/talairach.xfm --n 2 


 mri_add_xform_to_header -c /out/freesurfer/sub-01/mri/transforms/talairach.xfm nu.mgz nu.mgz 

#--------------------------------------------
#@# Intensity Normalization Mon Feb 16 10:34:51 UTC 2026

 mri_normalize -g 1 -mprage nu.mgz T1.mgz 



#---------------------------------
# New invocation of recon-all Mon Feb 16 10:38:43 UTC 2026 
#-------------------------------------
#@# EM Registration Mon Feb 16 10:38:49 UTC 2026

 mri_em_register -rusage /out/freesurfer/sub-01/touch/rusage.mri_em_register.dat -uns 3 -mask brainmask.mgz nu.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.lta 



#---------------------------------
# New invocation of recon-all Mon Feb 16 12:51:01 UTC 2026 
#-------------------------------------
#@# EM Registration Mon Feb 16 12:51:12 UTC 2026

 mri_em_register -rusage /out/freesurfer/sub-01/touch/rusage.mri_em_register.dat -uns 3 -mask brainmask.mgz nu.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.lta 

#--------------------------------------
#@# CA Normalize Mon Feb 16 13:27:38 UTC 2026

 mri_ca_normalize -c ctrl_pts.mgz -mask brainmask.mgz nu.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.lta norm.mgz 

#--------------------------------------
#@# CA Reg Mon Feb 16 13:31:02 UTC 2026

 mri_ca_register -rusage /out/freesurfer/sub-01/touch/rusage.mri_ca_register.dat -nobigventricles -T transforms/talairach.lta -align-after -mask brainmask.mgz norm.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.m3z 

#--------------------------------------
#@# CA Normalize Mon Feb 16 14:52:27 UTC 2026

 mri_ca_normalize -c ctrl_pts.mgz -mask brainmask.mgz nu.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.lta norm.mgz 

#--------------------------------------
#@# CA Reg Mon Feb 16 14:54:12 UTC 2026

 mri_ca_register -rusage /out/freesurfer/sub-01/touch/rusage.mri_ca_register.dat -nobigventricles -T transforms/talairach.lta -align-after -mask brainmask.mgz norm.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.m3z 

#--------------------------------------
#@# SubCort Seg Mon Feb 16 16:26:02 UTC 2026

 mri_ca_label -relabel_unlikely 9 .3 -prior 0.5 -align norm.mgz transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca aseg.auto_noCCseg.mgz 

#--------------------------------------
#@# SubCort Seg Mon Feb 16 17:00:30 UTC 2026

 mri_ca_label -relabel_unlikely 9 .3 -prior 0.5 -align norm.mgz transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca aseg.auto_noCCseg.mgz 


 mri_cc -aseg aseg.auto_noCCseg.mgz -o aseg.auto.mgz -lta /out/freesurfer/sub-01/mri/transforms/cc_up.lta sub-01 

#--------------------------------------
#@# Merge ASeg Mon Feb 16 17:25:45 UTC 2026

 cp aseg.auto.mgz aseg.presurf.mgz 

#--------------------------------------------
#@# Intensity Normalization2 Mon Feb 16 17:25:45 UTC 2026

 mri_normalize -mprage -aseg aseg.presurf.mgz -mask brainmask.mgz norm.mgz brain.mgz 

#--------------------------------------------
#@# Mask BFS Mon Feb 16 17:28:13 UTC 2026

 mri_mask -T 5 brain.mgz brainmask.mgz brain.finalsurfs.mgz 

#--------------------------------------------
#@# WM Segmentation Mon Feb 16 17:28:14 UTC 2026

 mri_segment -mprage brain.mgz wm.seg.mgz 


 mri_edit_wm_with_aseg -keep-in wm.seg.mgz brain.mgz aseg.presurf.mgz wm.asegedit.mgz 


 mri_pretess wm.asegedit.mgz wm norm.mgz wm.mgz 

#--------------------------------------------
#@# Fill Mon Feb 16 17:29:51 UTC 2026

 mri_fill -a ../scripts/ponscc.cut.log -xform transforms/talairach.lta -segmentation aseg.auto_noCCseg.mgz wm.mgz filled.mgz 



#---------------------------------
# New invocation of recon-all Mon Feb 16 17:33:37 UTC 2026 
#--------------------------------------
#@# SubCort Seg Mon Feb 16 17:33:40 UTC 2026

 mri_seg_diff --seg1 aseg.auto.mgz --seg2 aseg.presurf.mgz --diff aseg.manedit.mgz 


 mri_ca_label -relabel_unlikely 9 .3 -prior 0.5 -align norm.mgz transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca aseg.auto_noCCseg.mgz 


 mri_cc -aseg aseg.auto_noCCseg.mgz -o aseg.auto.mgz -lta /out/freesurfer/sub-01/mri/transforms/cc_up.lta sub-01 

#--------------------------------------
#@# Merge ASeg Mon Feb 16 18:18:01 UTC 2026

 cp aseg.auto.mgz aseg.presurf.mgz 



#---------------------------------
# New invocation of recon-all Mon Feb 16 20:46:33 UTC 2026 
#--------------------------------------------
#@# Cortical ribbon mask Mon Feb 16 20:46:36 UTC 2026

 mris_volmask --aseg_name aseg.presurf --label_left_white 2 --label_left_ribbon 3 --label_right_white 41 --label_right_ribbon 42 --save_ribbon sub-01 



#---------------------------------
# New invocation of recon-all Mon Feb 16 20:50:28 UTC 2026 
#-----------------------------------------
#@# Relabel Hypointensities Mon Feb 16 20:50:31 UTC 2026

 mri_relabel_hypointensities aseg.presurf.mgz ../surf aseg.presurf.hypos.mgz 

#-----------------------------------------
#@# AParc-to-ASeg aparc Mon Feb 16 20:50:39 UTC 2026

 mri_aparc2aseg --s sub-01 --volmask --aseg aseg.presurf.hypos --relabel mri/norm.mgz mri/transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca mri/aseg.auto_noCCseg.label_intensities.txt 

#-----------------------------------------
#@# AParc-to-ASeg a2009s Mon Feb 16 20:53:55 UTC 2026

 mri_aparc2aseg --s sub-01 --volmask --aseg aseg.presurf.hypos --relabel mri/norm.mgz mri/transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca mri/aseg.auto_noCCseg.label_intensities.txt --a2009s 

#-----------------------------------------
#@# AParc-to-ASeg DKTatlas Mon Feb 16 20:57:18 UTC 2026

 mri_aparc2aseg --s sub-01 --volmask --aseg aseg.presurf.hypos --relabel mri/norm.mgz mri/transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca mri/aseg.auto_noCCseg.label_intensities.txt --annot aparc.DKTatlas --o mri/aparc.DKTatlas+aseg.mgz 

#-----------------------------------------
#@# APas-to-ASeg Mon Feb 16 21:00:37 UTC 2026

 apas2aseg --i aparc+aseg.mgz --o aseg.mgz 

#--------------------------------------------
#@# ASeg Stats Mon Feb 16 21:00:42 UTC 2026

 mri_segstats --seg mri/aseg.mgz --sum stats/aseg.stats --pv mri/norm.mgz --empty --brainmask mri/brainmask.mgz --brain-vol-from-seg --excludeid 0 --excl-ctxgmwm --supratent --subcortgray --in mri/norm.mgz --in-intensity-name norm --in-intensity-units MR --etiv --surf-wm-vol --surf-ctx-vol --totalgray --euler --ctab /opt/freesurfer/ASegStatsLUT.txt --subject sub-01 

#-----------------------------------------
#@# WMParc Mon Feb 16 21:01:23 UTC 2026

 mri_aparc2aseg --s sub-01 --labelwm --hypo-as-wm --rip-unknown --volmask --o mri/wmparc.mgz --ctxseg aparc+aseg.mgz 


 mri_segstats --seg mri/wmparc.mgz --sum stats/wmparc.stats --pv mri/norm.mgz --excludeid 0 --brainmask mri/brainmask.mgz --in mri/norm.mgz --in-intensity-name norm --in-intensity-units MR --subject sub-01 --surf-wm-vol --ctab /opt/freesurfer/WMParcStatsLUT.txt --etiv 

