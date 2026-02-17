

#---------------------------------
# New invocation of recon-all Mon Feb 16 19:06:43 UTC 2026 
#--------------------------------------------
#@# Tessellate rh Mon Feb 16 19:06:46 UTC 2026

 mri_pretess ../mri/filled.mgz 127 ../mri/norm.mgz ../mri/filled-pretess127.mgz 


 mri_tessellate ../mri/filled-pretess127.mgz 127 ../surf/rh.orig.nofix 


 rm -f ../mri/filled-pretess127.mgz 


 mris_extract_main_component ../surf/rh.orig.nofix ../surf/rh.orig.nofix 

#--------------------------------------------
#@# Smooth1 rh Mon Feb 16 19:06:49 UTC 2026

 mris_smooth -nw -seed 1234 ../surf/rh.orig.nofix ../surf/rh.smoothwm.nofix 

#--------------------------------------------
#@# Inflation1 rh Mon Feb 16 19:06:49 UTC 2026

 mris_inflate -no-save-sulc ../surf/rh.smoothwm.nofix ../surf/rh.inflated.nofix 

#--------------------------------------------
#@# QSphere rh Mon Feb 16 19:06:52 UTC 2026

 mris_sphere -q -seed 1234 ../surf/rh.inflated.nofix ../surf/rh.qsphere.nofix 

#--------------------------------------------
#@# Fix Topology Copy rh Mon Feb 16 19:07:10 UTC 2026

 cp ../surf/rh.orig.nofix ../surf/rh.orig 


 cp ../surf/rh.inflated.nofix ../surf/rh.inflated 

#@# Fix Topology rh Mon Feb 16 19:07:10 UTC 2026

 mris_fix_topology -rusage /out/freesurfer/sub-01/touch/rusage.mris_fix_topology.rh.dat -mgz -sphere qsphere.nofix -ga -seed 1234 sub-01 rh 


 mris_euler_number ../surf/rh.orig 


 mris_remove_intersection ../surf/rh.orig ../surf/rh.orig 


 rm ../surf/rh.inflated 

#--------------------------------------------
#@# Make White Surf rh Mon Feb 16 20:37:18 UTC 2026

 mris_make_surfaces -aseg ../mri/aseg.presurf -white white.preaparc -noaparc -whiteonly -mgz -T1 brain.finalsurfs sub-01 rh 

#--------------------------------------------
#@# Smooth2 rh Mon Feb 16 20:37:49 UTC 2026

 mris_smooth -n 3 -nw -seed 1234 ../surf/rh.white.preaparc ../surf/rh.smoothwm 

#--------------------------------------------
#@# Inflation2 rh Mon Feb 16 20:37:50 UTC 2026

 mris_inflate -rusage /out/freesurfer/sub-01/touch/rusage.mris_inflate.rh.dat ../surf/rh.smoothwm ../surf/rh.inflated 

#--------------------------------------------
#@# Curv .H and .K rh Mon Feb 16 20:37:52 UTC 2026

 mris_curvature -w rh.white.preaparc 


 mris_curvature -thresh .999 -n -a 5 -w -distances 10 10 rh.inflated 


#-----------------------------------------
#@# Curvature Stats rh Mon Feb 16 20:38:02 UTC 2026

 mris_curvature_stats -m --writeCurvatureFiles -G -o ../stats/rh.curv.stats -F smoothwm sub-01 rh curv sulc 

#--------------------------------------------
#@# Sphere rh Mon Feb 16 20:38:03 UTC 2026

 mris_sphere -rusage /out/freesurfer/sub-01/touch/rusage.mris_sphere.rh.dat -seed 1234 ../surf/rh.inflated ../surf/rh.sphere 

#--------------------------------------------
#@# Surf Reg rh Mon Feb 16 20:40:30 UTC 2026

 mris_register -curv -rusage /out/freesurfer/sub-01/touch/rusage.mris_register.rh.dat ../surf/rh.sphere /opt/freesurfer/average/rh.folding.atlas.acfb40.noaparc.i12.2016-08-02.tif ../surf/rh.sphere.reg 

#--------------------------------------------
#@# Jacobian white rh Mon Feb 16 20:44:46 UTC 2026

 mris_jacobian ../surf/rh.white.preaparc ../surf/rh.sphere.reg ../surf/rh.jacobian_white 

#--------------------------------------------
#@# AvgCurv rh Mon Feb 16 20:44:46 UTC 2026

 mrisp_paint -a 5 /opt/freesurfer/average/rh.folding.atlas.acfb40.noaparc.i12.2016-08-02.tif#6 ../surf/rh.sphere.reg ../surf/rh.avg_curv 

#-----------------------------------------
#@# Cortical Parc rh Mon Feb 16 20:44:47 UTC 2026

 mris_ca_label -l ../label/rh.cortex.label -aseg ../mri/aseg.presurf.mgz -seed 1234 sub-01 rh ../surf/rh.sphere.reg /opt/freesurfer/average/rh.DKaparc.atlas.acfb40.noaparc.i12.2016-08-02.gcs ../label/rh.aparc.annot 

#--------------------------------------------
#@# Make Pial Surf rh Mon Feb 16 20:44:50 UTC 2026

 mris_make_surfaces -orig_white white.preaparc -orig_pial white.preaparc -aseg ../mri/aseg.presurf -mgz -T1 brain.finalsurfs sub-01 rh 

#--------------------------------------------
#@# Surf Volume rh Mon Feb 16 20:46:19 UTC 2026
#-----------------------------------------
#@# Cortical Parc 2 rh Mon Feb 16 20:46:20 UTC 2026

 mris_ca_label -l ../label/rh.cortex.label -aseg ../mri/aseg.presurf.mgz -seed 1234 sub-01 rh ../surf/rh.sphere.reg /opt/freesurfer/average/rh.CDaparc.atlas.acfb40.noaparc.i12.2016-08-02.gcs ../label/rh.aparc.a2009s.annot 

#-----------------------------------------
#@# Cortical Parc 3 rh Mon Feb 16 20:46:23 UTC 2026

 mris_ca_label -l ../label/rh.cortex.label -aseg ../mri/aseg.presurf.mgz -seed 1234 sub-01 rh ../surf/rh.sphere.reg /opt/freesurfer/average/rh.DKTaparc.atlas.acfb40.noaparc.i12.2016-08-02.gcs ../label/rh.aparc.DKTatlas.annot 

#-----------------------------------------
#@# WM/GM Contrast rh Mon Feb 16 20:46:26 UTC 2026

 pctsurfcon --s sub-01 --rh-only 



#---------------------------------
# New invocation of recon-all Mon Feb 16 20:48:46 UTC 2026 
#-----------------------------------------
#@# Parcellation Stats rh Mon Feb 16 20:48:49 UTC 2026

 mris_anatomical_stats -th3 -mgz -cortex ../label/rh.cortex.label -f ../stats/rh.aparc.stats -b -a ../label/rh.aparc.annot -c ../label/aparc.annot.ctab sub-01 rh white 


 mris_anatomical_stats -th3 -mgz -cortex ../label/rh.cortex.label -f ../stats/rh.aparc.pial.stats -b -a ../label/rh.aparc.annot -c ../label/aparc.annot.ctab sub-01 rh pial 

#-----------------------------------------
#@# Parcellation Stats 2 rh Mon Feb 16 20:49:01 UTC 2026

 mris_anatomical_stats -th3 -mgz -cortex ../label/rh.cortex.label -f ../stats/rh.aparc.a2009s.stats -b -a ../label/rh.aparc.a2009s.annot -c ../label/aparc.annot.a2009s.ctab sub-01 rh white 

#-----------------------------------------
#@# Parcellation Stats 3 rh Mon Feb 16 20:49:07 UTC 2026

 mris_anatomical_stats -th3 -mgz -cortex ../label/rh.cortex.label -f ../stats/rh.aparc.DKTatlas.stats -b -a ../label/rh.aparc.DKTatlas.annot -c ../label/aparc.annot.DKTatlas.ctab sub-01 rh white 

#--------------------------------------------
#@# BA_exvivo Labels rh Mon Feb 16 20:49:14 UTC 2026

 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA1_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA1_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA2_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA2_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA3a_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA3a_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA3b_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA3b_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA4a_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA4a_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA4p_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA4p_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA6_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA6_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA44_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA44_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA45_exvivo.label --trgsubject sub-01 --trglabel ./rh.BA45_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.V1_exvivo.label --trgsubject sub-01 --trglabel ./rh.V1_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.V2_exvivo.label --trgsubject sub-01 --trglabel ./rh.V2_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.MT_exvivo.label --trgsubject sub-01 --trglabel ./rh.MT_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.entorhinal_exvivo.label --trgsubject sub-01 --trglabel ./rh.entorhinal_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.perirhinal_exvivo.label --trgsubject sub-01 --trglabel ./rh.perirhinal_exvivo.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA1_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA1_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA2_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA2_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA3a_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA3a_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA3b_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA3b_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA4a_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA4a_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA4p_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA4p_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA6_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA6_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA44_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA44_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.BA45_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.BA45_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.V1_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.V1_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.V2_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.V2_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.MT_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.MT_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.entorhinal_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.entorhinal_exvivo.thresh.label --hemi rh --regmethod surface 


 mri_label2label --srcsubject fsaverage --srclabel /out/freesurfer/fsaverage/label/rh.perirhinal_exvivo.thresh.label --trgsubject sub-01 --trglabel ./rh.perirhinal_exvivo.thresh.label --hemi rh --regmethod surface 


 mris_label2annot --s sub-01 --hemi rh --ctab /opt/freesurfer/average/colortable_BA.txt --l rh.BA1_exvivo.label --l rh.BA2_exvivo.label --l rh.BA3a_exvivo.label --l rh.BA3b_exvivo.label --l rh.BA4a_exvivo.label --l rh.BA4p_exvivo.label --l rh.BA6_exvivo.label --l rh.BA44_exvivo.label --l rh.BA45_exvivo.label --l rh.V1_exvivo.label --l rh.V2_exvivo.label --l rh.MT_exvivo.label --l rh.entorhinal_exvivo.label --l rh.perirhinal_exvivo.label --a BA_exvivo --maxstatwinner --noverbose 


 mris_label2annot --s sub-01 --hemi rh --ctab /opt/freesurfer/average/colortable_BA.txt --l rh.BA1_exvivo.thresh.label --l rh.BA2_exvivo.thresh.label --l rh.BA3a_exvivo.thresh.label --l rh.BA3b_exvivo.thresh.label --l rh.BA4a_exvivo.thresh.label --l rh.BA4p_exvivo.thresh.label --l rh.BA6_exvivo.thresh.label --l rh.BA44_exvivo.thresh.label --l rh.BA45_exvivo.thresh.label --l rh.V1_exvivo.thresh.label --l rh.V2_exvivo.thresh.label --l rh.MT_exvivo.thresh.label --l rh.entorhinal_exvivo.thresh.label --l rh.perirhinal_exvivo.thresh.label --a BA_exvivo.thresh --maxstatwinner --noverbose 


 mris_anatomical_stats -th3 -mgz -f ../stats/rh.BA_exvivo.stats -b -a ./rh.BA_exvivo.annot -c ./BA_exvivo.ctab sub-01 rh white 


 mris_anatomical_stats -th3 -mgz -f ../stats/rh.BA_exvivo.thresh.stats -b -a ./rh.BA_exvivo.thresh.annot -c ./BA_exvivo.thresh.ctab sub-01 rh white 

