

#---------------------------------
# New invocation of recon-all Mon Feb 16 18:18:06 UTC 2026 
#--------------------------------------------
#@# Tessellate lh Mon Feb 16 18:18:14 UTC 2026

 mri_pretess ../mri/filled.mgz 255 ../mri/norm.mgz ../mri/filled-pretess255.mgz 


 mri_tessellate ../mri/filled-pretess255.mgz 255 ../surf/lh.orig.nofix 


 rm -f ../mri/filled-pretess255.mgz 


 mris_extract_main_component ../surf/lh.orig.nofix ../surf/lh.orig.nofix 

#--------------------------------------------
#@# Smooth1 lh Mon Feb 16 18:18:21 UTC 2026

 mris_smooth -nw -seed 1234 ../surf/lh.orig.nofix ../surf/lh.smoothwm.nofix 

#--------------------------------------------
#@# Inflation1 lh Mon Feb 16 18:18:23 UTC 2026

 mris_inflate -no-save-sulc ../surf/lh.smoothwm.nofix ../surf/lh.inflated.nofix 

#--------------------------------------------
#@# QSphere lh Mon Feb 16 18:18:28 UTC 2026

 mris_sphere -q -seed 1234 ../surf/lh.inflated.nofix ../surf/lh.qsphere.nofix 

#--------------------------------------------
#@# Fix Topology Copy lh Mon Feb 16 18:18:59 UTC 2026

 cp ../surf/lh.orig.nofix ../surf/lh.orig 


 cp ../surf/lh.inflated.nofix ../surf/lh.inflated 

#@# Fix Topology lh Mon Feb 16 18:18:59 UTC 2026

 mris_fix_topology -rusage /out/freesurfer/sub-01/touch/rusage.mris_fix_topology.lh.dat -mgz -sphere qsphere.nofix -ga -seed 1234 sub-01 lh 


 mris_euler_number ../surf/lh.orig 


 mris_remove_intersection ../surf/lh.orig ../surf/lh.orig 


 rm ../surf/lh.inflated 

#--------------------------------------------
#@# Make White Surf lh Mon Feb 16 18:57:59 UTC 2026

 mris_make_surfaces -aseg ../mri/aseg.presurf -white white.preaparc -noaparc -whiteonly -mgz -T1 brain.finalsurfs sub-01 lh 

#--------------------------------------------
#@# Smooth2 lh Mon Feb 16 18:59:00 UTC 2026

 mris_smooth -n 3 -nw -seed 1234 ../surf/lh.white.preaparc ../surf/lh.smoothwm 

#--------------------------------------------
#@# Inflation2 lh Mon Feb 16 18:59:01 UTC 2026

 mris_inflate -rusage /out/freesurfer/sub-01/touch/rusage.mris_inflate.lh.dat ../surf/lh.smoothwm ../surf/lh.inflated 

#--------------------------------------------
#@# Curv .H and .K lh Mon Feb 16 18:59:04 UTC 2026

 mris_curvature -w lh.white.preaparc 


 mris_curvature -thresh .999 -n -a 5 -w -distances 10 10 lh.inflated 


#-----------------------------------------
#@# Curvature Stats lh Mon Feb 16 18:59:13 UTC 2026

 mris_curvature_stats -m --writeCurvatureFiles -G -o ../stats/lh.curv.stats -F smoothwm sub-01 lh curv sulc 

#--------------------------------------------
#@# Sphere lh Mon Feb 16 18:59:13 UTC 2026

 mris_sphere -rusage /out/freesurfer/sub-01/touch/rusage.mris_sphere.lh.dat -seed 1234 ../surf/lh.inflated ../surf/lh.sphere 

#--------------------------------------------
#@# Surf Reg lh Mon Feb 16 19:01:24 UTC 2026

 mris_register -curv -rusage /out/freesurfer/sub-01/touch/rusage.mris_register.lh.dat ../surf/lh.sphere /opt/freesurfer/average/lh.folding.atlas.acfb40.noaparc.i12.2016-08-02.tif ../surf/lh.sphere.reg 

#--------------------------------------------
#@# Jacobian white lh Mon Feb 16 19:05:21 UTC 2026

 mris_jacobian ../surf/lh.white.preaparc ../surf/lh.sphere.reg ../surf/lh.jacobian_white 

#--------------------------------------------
#@# AvgCurv lh Mon Feb 16 19:05:22 UTC 2026

 mrisp_paint -a 5 /opt/freesurfer/average/lh.folding.atlas.acfb40.noaparc.i12.2016-08-02.tif#6 ../surf/lh.sphere.reg ../surf/lh.avg_curv 

#-----------------------------------------
#@# Cortical Parc lh Mon Feb 16 19:05:22 UTC 2026

 mris_ca_label -l ../label/lh.cortex.label -aseg ../mri/aseg.presurf.mgz -seed 1234 sub-01 lh ../surf/lh.sphere.reg /opt/freesurfer/average/lh.DKaparc.atlas.acfb40.noaparc.i12.2016-08-02.gcs ../label/lh.aparc.annot 

#--------------------------------------------
#@# Make Pial Surf lh Mon Feb 16 19:05:25 UTC 2026

 mris_make_surfaces -orig_white white.preaparc -orig_pial white.preaparc -aseg ../mri/aseg.presurf -mgz -T1 brain.finalsurfs sub-01 lh 

#--------------------------------------------
#@# Surf Volume lh Mon Feb 16 19:06:32 UTC 2026
#-----------------------------------------
#@# Cortical Parc 2 lh Mon Feb 16 19:06:33 UTC 2026

 mris_ca_label -l ../label/lh.cortex.label -aseg ../mri/aseg.presurf.mgz -seed 1234 sub-01 lh ../surf/lh.sphere.reg /opt/freesurfer/average/lh.CDaparc.atlas.acfb40.noaparc.i12.2016-08-02.gcs ../label/lh.aparc.a2009s.annot 

#-----------------------------------------
#@# Cortical Parc 3 lh Mon Feb 16 19:06:36 UTC 2026

 mris_ca_label -l ../label/lh.cortex.label -aseg ../mri/aseg.presurf.mgz -seed 1234 sub-01 lh ../surf/lh.sphere.reg /opt/freesurfer/average/lh.DKTaparc.atlas.acfb40.noaparc.i12.2016-08-02.gcs ../label/lh.aparc.DKTatlas.annot 

#-----------------------------------------
#@# WM/GM Contrast lh Mon Feb 16 19:06:38 UTC 2026

 pctsurfcon --s sub-01 --lh-only 



#---------------------------------
# New invocation of recon-all Mon Feb 16 20:47:09 UTC 2026 
#-----------------------------------------
#@# Parcellation Stats lh Mon Feb 16 20:47:12 UTC 2026

 mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label -f ../stats/lh.aparc.stats -b -a ../label/lh.aparc.annot -c ../label/aparc.annot.ctab sub-01 lh white 


 mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label -f ../stats/lh.aparc.pial.stats -b -a ../label/lh.aparc.annot -c ../label/aparc.annot.ctab sub-01 lh pial 

#-----------------------------------------
#@# Parcellation Stats 2 lh Mon Feb 16 20:47:24 UTC 2026

 mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label -f ../stats/lh.aparc.a2009s.stats -b -a ../label/lh.aparc.a2009s.annot -c ../label/aparc.annot.a2009s.ctab sub-01 lh white 

#-----------------------------------------
#@# Parcellation Stats 3 lh Mon Feb 16 20:47:30 UTC 2026

 mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label -f ../stats/lh.aparc.DKTatlas.stats -b -a ../label/lh.aparc.DKTatlas.annot -c ../label/aparc.annot.DKTatlas.ctab sub-01 lh white 

#--------------------------------------------
#@# BA_exvivo Labels lh Mon Feb 16 20:47:36 UTC 2026

 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA1_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA1_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA2_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA2_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA3a_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA3a_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA3b_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA3b_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA4a_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA4a_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA4p_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA4p_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA6_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA6_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA44_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA44_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA45_exvivo.label --trgsubject sub-01 --trglabel ./lh.BA45_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.V1_exvivo.label --trgsubject sub-01 --trglabel ./lh.V1_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.V2_exvivo.label --trgsubject sub-01 --trglabel ./lh.V2_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.MT_exvivo.label --trgsubject sub-01 --trglabel ./lh.MT_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.entorhinal_exvivo.label --trgsubject sub-01 --trglabel ./lh.entorhinal_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.perirhinal_exvivo.label --trgsubject sub-01 --trglabel ./lh.perirhinal_exvivo.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA1_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA1_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA2_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA2_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA3a_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA3a_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA3b_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA3b_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA4a_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA4a_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA4p_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA4p_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA6_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA6_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA44_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA44_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.BA45_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.BA45_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.V1_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.V1_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.V2_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.V2_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.MT_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.MT_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.entorhinal_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.entorhinal_exvivo.thresh.label --hemi lh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/lh.perirhinal_exvivo.thresh.label --trgsubject sub-01 --trglabel ./lh.perirhinal_exvivo.thresh.label --hemi lh --regmethod surface 


 mris_label2annot --s sub-01 --hemi lh --ctab /opt/freesurfer/average/colortable_BA.txt --l lh.BA1_exvivo.label --l lh.BA2_exvivo.label --l lh.BA3a_exvivo.label --l lh.BA3b_exvivo.label --l lh.BA4a_exvivo.label --l lh.BA4p_exvivo.label --l lh.BA6_exvivo.label --l lh.BA44_exvivo.label --l lh.BA45_exvivo.label --l lh.V1_exvivo.label --l lh.V2_exvivo.label --l lh.MT_exvivo.label --l lh.entorhinal_exvivo.label --l lh.perirhinal_exvivo.label --a BA_exvivo --maxstatwinner --noverbose 


 mris_label2annot --s sub-01 --hemi lh --ctab /opt/freesurfer/average/colortable_BA.txt --l lh.BA1_exvivo.thresh.label --l lh.BA2_exvivo.thresh.label --l lh.BA3a_exvivo.thresh.label --l lh.BA3b_exvivo.thresh.label --l lh.BA4a_exvivo.thresh.label --l lh.BA4p_exvivo.thresh.label --l lh.BA6_exvivo.thresh.label --l lh.BA44_exvivo.thresh.label --l lh.BA45_exvivo.thresh.label --l lh.V1_exvivo.thresh.label --l lh.V2_exvivo.thresh.label --l lh.MT_exvivo.thresh.label --l lh.entorhinal_exvivo.thresh.label --l lh.perirhinal_exvivo.thresh.label --a BA_exvivo.thresh --maxstatwinner --noverbose 


 mris_anatomical_stats -th3 -mgz -f ../stats/lh.BA_exvivo.stats -b -a ./lh.BA_exvivo.annot -c ./BA_exvivo.ctab sub-01 lh white 


 mris_anatomical_stats -th3 -mgz -f ../stats/lh.BA_exvivo.thresh.stats -b -a ./lh.BA_exvivo.thresh.annot -c ./BA_exvivo.thresh.ctab sub-01 lh white 

