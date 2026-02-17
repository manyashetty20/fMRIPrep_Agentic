Node: single_subject_01_wf (anat_preproc_wf (surface_recon_wf (autorecon_resume_wf (autorecon3 (freesurfer)
===========================================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.surface_recon_wf.autorecon_resume_wf.autorecon3
 Exec ID : autorecon3


Original Inputs
---------------


* FLAIR_file : <undefined>
* T1_files : <undefined>
* T2_file : <undefined>
* args : <undefined>
* big_ventricles : <undefined>
* brainstem : <undefined>
* directive : autorecon3
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
* directive : autorecon3
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


* cmdline : recon-all -autorecon3 -openmp 8 -subjid sub-01 -sd /out/freesurfer -nosphere -nosurfreg -nojacobian_white -noavgcurv -nocortparc -nopial -noparcstats -nocortparc2 -noparcstats2 -nocortparc3 -noparcstats3 -nopctsurfcon -nocortribbon -nobalabels
* duration : 819.416642
* hostname : efad4839b3da
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/autorecon_resume_wf/autorecon3


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 Subject Stamp: freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1-f53a55a
Current Stamp: freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1-f53a55a
INFO: SUBJECTS_DIR is /out/freesurfer
Actual FREESURFER_HOME /opt/freesurfer
-rw-r--r-- 1 root root 308141 Feb 16 20:47 /out/freesurfer/sub-01/scripts/recon-all.log
Linux efad4839b3da 6.12.54-linuxkit #1 SMP Tue Nov  4 21:21:47 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
'/opt/freesurfer/bin/recon-all' -> '/out/freesurfer/sub-01/scripts/recon-all.local-copy'
#-----------------------------------------
#@# Relabel Hypointensities Mon Feb 16 20:50:31 UTC 2026
/out/freesurfer/sub-01/mri

 mri_relabel_hypointensities aseg.presurf.mgz ../surf aseg.presurf.hypos.mgz 

reading input surface ../surf/lh.white...
relabeling lh hypointensities...
1297 voxels changed to hypointensity...
reading input surface ../surf/rh.white...
relabeling rh hypointensities...
567 voxels changed to hypointensity...
1838 hypointense voxels neighboring cortex changed
#-----------------------------------------
#@# AParc-to-ASeg aparc Mon Feb 16 20:50:39 UTC 2026
/out/freesurfer/sub-01

 mri_aparc2aseg --s sub-01 --volmask --aseg aseg.presurf.hypos --relabel mri/norm.mgz mri/transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca mri/aseg.auto_noCCseg.label_intensities.txt 

relabeling unlikely voxels interior to white matter surface:
	norm: mri/norm.mgz
	 XFORM: mri/transforms/talairach.m3z
	GCA: /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca
	label intensities: mri/aseg.auto_noCCseg.label_intensities.txt
SUBJECTS_DIR /out/freesurfer
subject sub-01
outvol /out/freesurfer/sub-01/mri/aparc+aseg.mgz
useribbon 0
baseoffset 0
RipUnknown 0

Reading lh white surface 
 /out/freesurfer/sub-01/surf/lh.white

Reading lh pial surface 
 /out/freesurfer/sub-01/surf/lh.pial

Loading lh annotations from /out/freesurfer/sub-01/label/lh.aparc.annot
reading colortable from annotation file...
colortable with 36 entries read (originally /autofs/space/tanha_002/users/greve/fsdev.build/average/colortable_desikan_killiany.txt)

Reading rh white surface 
 /out/freesurfer/sub-01/surf/rh.white

Reading rh pial surface 
 /out/freesurfer/sub-01/surf/rh.pial

Loading rh annotations from /out/freesurfer/sub-01/label/rh.aparc.annot
reading colortable from annotation file...
colortable with 36 entries read (originally /autofs/space/tanha_002/users/greve/fsdev.build/average/colortable_desikan_killiany.txt)
Have color table for lh white annotation
Have color table for rh white annotation
Loading ribbon segmentation from /out/freesurfer/sub-01/mri/ribbon.mgz

Building hash of lh white

Building hash of lh pial

Building hash of rh white

Building hash of rh pial

Loading aseg from /out/freesurfer/sub-01/mri/aseg.presurf.hypos.mgz
ASeg Vox2RAS: -----------
-1.00000   0.00000   0.00000   128.00000;
 0.00000   0.00000   1.00000  -128.00000;
 0.00000  -1.00000   0.00000   128.00000;
 0.00000   0.00000   0.00000   1.00000;
-------------------------

Labeling Slice
relabeling unlikely voxels in interior of white matter
setting orig areas to linear transform determinant scaled 1.14
reading 45 labels from mri/aseg.auto_noCCseg.label_intensities.txt
rescaling Left_Cerebral_White_Matter from 107 --> 102
rescaling Left_Cerebral_Cortex from 61 --> 83
rescaling Left_Lateral_Ventricle from 13 --> 20
rescaling Left_Inf_Lat_Vent from 34 --> 27
rescaling Left_Cerebellum_White_Matter from 86 --> 84
rescaling Left_Cerebellum_Cortex from 60 --> 63
rescaling Left_Thalamus from 94 --> 115
rescaling Left_Thalamus_Proper from 84 --> 108
rescaling Left_Caudate from 75 --> 83
rescaling Left_Putamen from 80 --> 91
rescaling Left_Pallidum from 98 --> 100
rescaling Third_Ventricle from 25 --> 24
rescaling Fourth_Ventricle from 22 --> 14
rescaling Brain_Stem from 81 --> 95
rescaling Left_Hippocampus from 57 --> 72
rescaling Left_Amygdala from 56 --> 69
rescaling CSF from 32 --> 36
rescaling Left_Accumbens_area from 62 --> 76
rescaling Right_Cerebral_White_Matter from 105 --> 104
rescaling Right_Cerebral_Cortex from 58 --> 60
rescaling Right_Lateral_Ventricle from 13 --> 13
rescaling Right_Inf_Lat_Vent from 25 --> 23
rescaling Right_Cerebellum_White_Matter from 87 --> 84
rescaling Right_Cerebellum_Cortex from 59 --> 49
rescaling Right_Thalamus_Proper from 85 --> 105
rescaling Right_Caudate from 62 --> 81
rescaling Right_Putamen from 80 --> 91
rescaling Right_Pallidum from 97 --> 100
rescaling Right_Hippocampus from 53 --> 68
rescaling Right_Amygdala from 55 --> 69
rescaling Right_Accumbens_area from 65 --> 80
rescaling Fifth_Ventricle from 40 --> 32
rescaling WM_hypointensities from 78 --> 76
rescaling non_WM_hypointensities from 40 --> 54
  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19 
 20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39 
 40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59 
 60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79 
 80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 
100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 
120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 
140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 
160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 
180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 
200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 
220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 
240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 nctx = 46902
Used brute-force search on 0 voxels
relabeling unlikely voxels in interior of white matter
average std[0] = 7.3
pass 1: 56 changed.
pass 2: 16 changed.
pass 3: 5 changed.
pass 4: 1 changed.
pass 5: 0 changed.
nchanged = 0
Writing output aseg to /out/freesurfer/sub-01/mri/aparc+aseg.mgz
#-----------------------------------------
#@# AParc-to-ASeg a2009s Mon Feb 16 20:53:55 UTC 2026
/out/freesurfer/sub-01

 mri_aparc2aseg --s sub-01 --volmask --aseg aseg.presurf.hypos --relabel mri/norm.mgz mri/transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca mri/aseg.auto_noCCseg.label_intensities.txt --a2009s 

relabeling unlikely voxels interior to white matter surface:
	norm: mri/norm.mgz
	 XFORM: mri/transforms/talairach.m3z
	GCA: /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca
	label intensities: mri/aseg.auto_noCCseg.label_intensities.txt
SUBJECTS_DIR /out/freesurfer
subject sub-01
outvol /out/freesurfer/sub-01/mri/aparc.a2009s+aseg.mgz
useribbon 0
baseoffset 10100
RipUnknown 0

Reading lh white surface 
 /out/freesurfer/sub-01/surf/lh.white

Reading lh pial surface 
 /out/freesurfer/sub-01/surf/lh.pial

Loading lh annotations from /out/freesurfer/sub-01/label/lh.aparc.a2009s.annot
reading colortable from annotation file...
colortable with 76 entries read (originally Simple_surface_labels2008.txt)

Reading rh white surface 
 /out/freesurfer/sub-01/surf/rh.white

Reading rh pial surface 
 /out/freesurfer/sub-01/surf/rh.pial

Loading rh annotations from /out/freesurfer/sub-01/label/rh.aparc.a2009s.annot
reading colortable from annotation file...
colortable with 76 entries read (originally Simple_surface_labels2008.txt)
Have color table for lh white annotation
Have color table for rh white annotation
Loading ribbon segmentation from /out/freesurfer/sub-01/mri/ribbon.mgz

Building hash of lh white

Building hash of lh pial

Building hash of rh white

Building hash of rh pial

Loading aseg from /out/freesurfer/sub-01/mri/aseg.presurf.hypos.mgz
ASeg Vox2RAS: -----------
-1.00000   0.00000   0.00000   128.00000;
 0.00000   0.00000   1.00000  -128.00000;
 0.00000  -1.00000   0.00000   128.00000;
 0.00000   0.00000   0.00000   1.00000;
-------------------------

Labeling Slice
relabeling unlikely voxels in interior of white matter
setting orig areas to linear transform determinant scaled 1.14
reading 45 labels from mri/aseg.auto_noCCseg.label_intensities.txt
rescaling Left_Cerebral_White_Matter from 107 --> 102
rescaling Left_Cerebral_Cortex from 61 --> 83
rescaling Left_Lateral_Ventricle from 13 --> 20
rescaling Left_Inf_Lat_Vent from 34 --> 27
rescaling Left_Cerebellum_White_Matter from 86 --> 84
rescaling Left_Cerebellum_Cortex from 60 --> 63
rescaling Left_Thalamus from 94 --> 115
rescaling Left_Thalamus_Proper from 84 --> 108
rescaling Left_Caudate from 75 --> 83
rescaling Left_Putamen from 80 --> 91
rescaling Left_Pallidum from 98 --> 100
rescaling Third_Ventricle from 25 --> 24
rescaling Fourth_Ventricle from 22 --> 14
rescaling Brain_Stem from 81 --> 95
rescaling Left_Hippocampus from 57 --> 72
rescaling Left_Amygdala from 56 --> 69
rescaling CSF from 32 --> 36
rescaling Left_Accumbens_area from 62 --> 76
rescaling Right_Cerebral_White_Matter from 105 --> 104
rescaling Right_Cerebral_Cortex from 58 --> 60
rescaling Right_Lateral_Ventricle from 13 --> 13
rescaling Right_Inf_Lat_Vent from 25 --> 23
rescaling Right_Cerebellum_White_Matter from 87 --> 84
rescaling Right_Cerebellum_Cortex from 59 --> 49
rescaling Right_Thalamus_Proper from 85 --> 105
rescaling Right_Caudate from 62 --> 81
rescaling Right_Putamen from 80 --> 91
rescaling Right_Pallidum from 97 --> 100
rescaling Right_Hippocampus from 53 --> 68
rescaling Right_Amygdala from 55 --> 69
rescaling Right_Accumbens_area from 65 --> 80
rescaling Fifth_Ventricle from 40 --> 32
rescaling WM_hypointensities from 78 --> 76
rescaling non_WM_hypointensities from 40 --> 54
  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19 
 20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39 
 40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59 
 60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79 
 80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 
100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 
120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 
140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 
160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 
180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 
200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 
220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 
240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 nctx = 46961
Used brute-force search on 0 voxels
relabeling unlikely voxels in interior of white matter
average std[0] = 7.3
pass 1: 56 changed.
pass 2: 16 changed.
pass 3: 5 changed.
pass 4: 1 changed.
pass 5: 0 changed.
nchanged = 0
Writing output aseg to /out/freesurfer/sub-01/mri/aparc.a2009s+aseg.mgz
#-----------------------------------------
#@# AParc-to-ASeg DKTatlas Mon Feb 16 20:57:18 UTC 2026
/out/freesurfer/sub-01

 mri_aparc2aseg --s sub-01 --volmask --aseg aseg.presurf.hypos --relabel mri/norm.mgz mri/transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca mri/aseg.auto_noCCseg.label_intensities.txt --annot aparc.DKTatlas --o mri/aparc.DKTatlas+aseg.mgz 

relabeling unlikely voxels interior to white matter surface:
	norm: mri/norm.mgz
	 XFORM: mri/transforms/talairach.m3z
	GCA: /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca
	label intensities: mri/aseg.auto_noCCseg.label_intensities.txt
SUBJECTS_DIR /out/freesurfer
subject sub-01
outvol mri/aparc.DKTatlas+aseg.mgz
useribbon 0
baseoffset 0
RipUnknown 0

Reading lh white surface 
 /out/freesurfer/sub-01/surf/lh.white

Reading lh pial surface 
 /out/freesurfer/sub-01/surf/lh.pial

Loading lh annotations from /out/freesurfer/sub-01/label/lh.aparc.DKTatlas.annot
reading colortable from annotation file...
colortable with 36 entries read (originally /autofs/space/tanha_002/users/greve/fsdev.build/average/colortable_desikan_killiany.txt)

Reading rh white surface 
 /out/freesurfer/sub-01/surf/rh.white

Reading rh pial surface 
 /out/freesurfer/sub-01/surf/rh.pial

Loading rh annotations from /out/freesurfer/sub-01/label/rh.aparc.DKTatlas.annot
reading colortable from annotation file...
colortable with 36 entries read (originally /autofs/space/tanha_002/users/greve/fsdev.build/average/colortable_desikan_killiany.txt)
Have color table for lh white annotation
Have color table for rh white annotation
Loading ribbon segmentation from /out/freesurfer/sub-01/mri/ribbon.mgz

Building hash of lh white

Building hash of lh pial

Building hash of rh white

Building hash of rh pial

Loading aseg from /out/freesurfer/sub-01/mri/aseg.presurf.hypos.mgz
ASeg Vox2RAS: -----------
-1.00000   0.00000   0.00000   128.00000;
 0.00000   0.00000   1.00000  -128.00000;
 0.00000  -1.00000   0.00000   128.00000;
 0.00000   0.00000   0.00000   1.00000;
-------------------------

Labeling Slice
relabeling unlikely voxels in interior of white matter
setting orig areas to linear transform determinant scaled 1.14
reading 45 labels from mri/aseg.auto_noCCseg.label_intensities.txt
rescaling Left_Cerebral_White_Matter from 107 --> 102
rescaling Left_Cerebral_Cortex from 61 --> 83
rescaling Left_Lateral_Ventricle from 13 --> 20
rescaling Left_Inf_Lat_Vent from 34 --> 27
rescaling Left_Cerebellum_White_Matter from 86 --> 84
rescaling Left_Cerebellum_Cortex from 60 --> 63
rescaling Left_Thalamus from 94 --> 115
rescaling Left_Thalamus_Proper from 84 --> 108
rescaling Left_Caudate from 75 --> 83
rescaling Left_Putamen from 80 --> 91
rescaling Left_Pallidum from 98 --> 100
rescaling Third_Ventricle from 25 --> 24
rescaling Fourth_Ventricle from 22 --> 14
rescaling Brain_Stem from 81 --> 95
rescaling Left_Hippocampus from 57 --> 72
rescaling Left_Amygdala from 56 --> 69
rescaling CSF from 32 --> 36
rescaling Left_Accumbens_area from 62 --> 76
rescaling Right_Cerebral_White_Matter from 105 --> 104
rescaling Right_Cerebral_Cortex from 58 --> 60
rescaling Right_Lateral_Ventricle from 13 --> 13
rescaling Right_Inf_Lat_Vent from 25 --> 23
rescaling Right_Cerebellum_White_Matter from 87 --> 84
rescaling Right_Cerebellum_Cortex from 59 --> 49
rescaling Right_Thalamus_Proper from 85 --> 105
rescaling Right_Caudate from 62 --> 81
rescaling Right_Putamen from 80 --> 91
rescaling Right_Pallidum from 97 --> 100
rescaling Right_Hippocampus from 53 --> 68
rescaling Right_Amygdala from 55 --> 69
rescaling Right_Accumbens_area from 65 --> 80
rescaling Fifth_Ventricle from 40 --> 32
rescaling WM_hypointensities from 78 --> 76
rescaling non_WM_hypointensities from 40 --> 54
  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19 
 20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39 
 40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59 
 60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79 
 80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 
100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 
120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 
140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 
160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 
180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 
200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 
220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 
240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 nctx = 46961
Used brute-force search on 0 voxels
relabeling unlikely voxels in interior of white matter
average std[0] = 7.3
pass 1: 56 changed.
pass 2: 16 changed.
pass 3: 5 changed.
pass 4: 1 changed.
pass 5: 0 changed.
nchanged = 0
Writing output aseg to mri/aparc.DKTatlas+aseg.mgz
#-----------------------------------------
#@# APas-to-ASeg Mon Feb 16 21:00:37 UTC 2026
/out/freesurfer/sub-01/mri

 apas2aseg --i aparc+aseg.mgz --o aseg.mgz 

Mon Feb 16 21:00:37 UTC 2026

setenv SUBJECTS_DIR /out/freesurfer
cd /out/freesurfer/sub-01/mri
/opt/freesurfer/bin/apas2aseg --i aparc+aseg.mgz --o aseg.mgz

freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1-f53a55a
$Id: apas2aseg,v 1.2 2016/02/12 21:43:14 zkaufman Exp $
Linux efad4839b3da 6.12.54-linuxkit #1 SMP Tue Nov  4 21:21:47 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
mri_binarize --i aparc+aseg.mgz --o aseg.mgz --replace 1000 3 --replace 2000 42 --replace 1001 3 --replace 2001 42 --replace 1002 3 --replace 2002 42 --replace 1003 3 --replace 2003 42 --replace 1004 3 --replace 2004 42 --replace 1005 3 --replace 2005 42 --replace 1006 3 --replace 2006 42 --replace 1007 3 --replace 2007 42 --replace 1008 3 --replace 2008 42 --replace 1009 3 --replace 2009 42 --replace 1010 3 --replace 2010 42 --replace 1011 3 --replace 2011 42 --replace 1012 3 --replace 2012 42 --replace 1013 3 --replace 2013 42 --replace 1014 3 --replace 2014 42 --replace 1015 3 --replace 2015 42 --replace 1016 3 --replace 2016 42 --replace 1017 3 --replace 2017 42 --replace 1018 3 --replace 2018 42 --replace 1019 3 --replace 2019 42 --replace 1020 3 --replace 2020 42 --replace 1021 3 --replace 2021 42 --replace 1022 3 --replace 2022 42 --replace 1023 3 --replace 2023 42 --replace 1024 3 --replace 2024 42 --replace 1025 3 --replace 2025 42 --replace 1026 3 --replace 2026 42 --replace 1027 3 --replace 2027 42 --replace 1028 3 --replace 2028 42 --replace 1029 3 --replace 2029 42 --replace 1030 3 --replace 2030 42 --replace 1031 3 --replace 2031 42 --replace 1032 3 --replace 2032 42 --replace 1033 3 --replace 2033 42 --replace 1034 3 --replace 2034 42 --replace 1035 3 --replace 2035 42

$Id: mri_binarize.c,v 1.43 2016/06/09 20:46:21 greve Exp $
cwd /out/freesurfer/sub-01/mri
cmdline mri_binarize.bin --i aparc+aseg.mgz --o aseg.mgz --replace 1000 3 --replace 2000 42 --replace 1001 3 --replace 2001 42 --replace 1002 3 --replace 2002 42 --replace 1003 3 --replace 2003 42 --replace 1004 3 --replace 2004 42 --replace 1005 3 --replace 2005 42 --replace 1006 3 --replace 2006 42 --replace 1007 3 --replace 2007 42 --replace 1008 3 --replace 2008 42 --replace 1009 3 --replace 2009 42 --replace 1010 3 --replace 2010 42 --replace 1011 3 --replace 2011 42 --replace 1012 3 --replace 2012 42 --replace 1013 3 --replace 2013 42 --replace 1014 3 --replace 2014 42 --replace 1015 3 --replace 2015 42 --replace 1016 3 --replace 2016 42 --replace 1017 3 --replace 2017 42 --replace 1018 3 --replace 2018 42 --replace 1019 3 --replace 2019 42 --replace 1020 3 --replace 2020 42 --replace 1021 3 --replace 2021 42 --replace 1022 3 --replace 2022 42 --replace 1023 3 --replace 2023 42 --replace 1024 3 --replace 2024 42 --replace 1025 3 --replace 2025 42 --replace 1026 3 --replace 2026 42 --replace 1027 3 --replace 2027 42 --replace 1028 3 --replace 2028 42 --replace 1029 3 --replace 2029 42 --replace 1030 3 --replace 2030 42 --replace 1031 3 --replace 2031 42 --replace 1032 3 --replace 2032 42 --replace 1033 3 --replace 2033 42 --replace 1034 3 --replace 2034 42 --replace 1035 3 --replace 2035 42 
sysname  Linux
hostname efad4839b3da
machine  x86_64
user     root

input      aparc+aseg.mgz
frame      0
nErode3d   0
nErode2d   0
output     aseg.mgz
Binarizing based on threshold
min        -infinity
max        +infinity
binval        1
binvalnot     0
fstart = 0, fend = 0, nframes = 1
Replacing 72
 1:  1000    3
 2:  2000   42
 3:  1001    3
 4:  2001   42
 5:  1002    3
 6:  2002   42
 7:  1003    3
 8:  2003   42
 9:  1004    3
10:  2004   42
11:  1005    3
12:  2005   42
13:  1006    3
14:  2006   42
15:  1007    3
16:  2007   42
17:  1008    3
18:  2008   42
19:  1009    3
20:  2009   42
21:  1010    3
22:  2010   42
23:  1011    3
24:  2011   42
25:  1012    3
26:  2012   42
27:  1013    3
28:  2013   42
29:  1014    3
30:  2014   42
31:  1015    3
32:  2015   42
33:  1016    3
34:  2016   42
35:  1017    3
36:  2017   42
37:  1018    3
38:  2018   42
39:  1019    3
40:  2019   42
41:  1020    3
42:  2020   42
43:  1021    3
44:  2021   42
45:  1022    3
46:  2022   42
47:  1023    3
48:  2023   42
49:  1024    3
50:  2024   42
51:  1025    3
52:  2025   42
53:  1026    3
54:  2026   42
55:  1027    3
56:  2027   42
57:  1028    3
58:  2028   42
59:  1029    3
60:  2029   42
61:  1030    3
62:  2030   42
63:  1031    3
64:  2031   42
65:  1032    3
66:  2032   42
67:  1033    3
68:  2033   42
69:  1034    3
70:  2034   42
71:  1035    3
72:  2035   42
Found 0 values in range
Counting number of voxels in first frame
Found 0 voxels in final mask
Count: 0 0.000000 16777216 0.000000
mri_binarize done
 
Started at Mon Feb 16 21:00:37 UTC 2026 
Ended   at Mon Feb 16 21:00:42 UTC 2026
Apas2aseg-Run-Time-Sec 5
 
apas2aseg Done
#--------------------------------------------
#@# ASeg Stats Mon Feb 16 21:00:42 UTC 2026
/out/freesurfer/sub-01

 mri_segstats --seg mri/aseg.mgz --sum stats/aseg.stats --pv mri/norm.mgz --empty --brainmask mri/brainmask.mgz --brain-vol-from-seg --excludeid 0 --excl-ctxgmwm --supratent --subcortgray --in mri/norm.mgz --in-intensity-name norm --in-intensity-units MR --etiv --surf-wm-vol --surf-ctx-vol --totalgray --euler --ctab /opt/freesurfer/ASegStatsLUT.txt --subject sub-01 


$Id: mri_segstats.c,v 1.121 2016/05/31 17:27:11 greve Exp $
cwd 
cmdline mri_segstats --seg mri/aseg.mgz --sum stats/aseg.stats --pv mri/norm.mgz --empty --brainmask mri/brainmask.mgz --brain-vol-from-seg --excludeid 0 --excl-ctxgmwm --supratent --subcortgray --in mri/norm.mgz --in-intensity-name norm --in-intensity-units MR --etiv --surf-wm-vol --surf-ctx-vol --totalgray --euler --ctab /opt/freesurfer/ASegStatsLUT.txt --subject sub-01 
sysname  Linux
hostname efad4839b3da
machine  x86_64
user     root
UseRobust  0
atlas_icv (eTIV) = 120544 mm^3    (det: 16.160946 )
Computing euler number
orig.nofix lheno = -118, rheno = -62
orig.nofix lhholes =   60, rhholes = 32
Loading mri/aseg.mgz
Getting Brain Volume Statistics
lhCtxGM: 16316.327 15835.000  diff=  481.3  pctdiff= 2.950
rhCtxGM: 30120.634 29939.000  diff=  181.6  pctdiff= 0.603
lhCtxWM: 21969.726 22859.000  diff= -889.3  pctdiff=-4.048
rhCtxWM: 21129.806 21159.000  diff=  -29.2  pctdiff=-0.138
SubCortGMVol   6695.000
SupraTentVol  100537.493 (98089.000) diff=2448.493 pctdiff=2.435
SupraTentVolNotVent  99155.493 (96707.000) diff=2448.493 pctdiff=2.469
BrainSegVol  110978.000 (110862.000) diff=116.000 pctdiff=0.105
BrainSegVolNotVent  109402.000 (109139.493) diff=262.507 pctdiff=0.240
BrainSegVolNotVent  109402.000
CerebellumVol 12688.000
VentChorVol    1382.000
3rd4th5thCSF    194.000
CSFVol    81.000, OptChiasmVol     4.000
MaskVol 177473.000
Loading mri/norm.mgz
Loading mri/norm.mgz
Voxel Volume is 1 mm^3
Generating list of segmentation ids
Found  50 segmentations
Computing statistics for each segmentation

Reporting on  45 segmentations
Using PrintSegStat
mri_segstats done
#-----------------------------------------
#@# WMParc Mon Feb 16 21:01:23 UTC 2026
/out/freesurfer/sub-01

 mri_aparc2aseg --s sub-01 --labelwm --hypo-as-wm --rip-unknown --volmask --o mri/wmparc.mgz --ctxseg aparc+aseg.mgz 

SUBJECTS_DIR /out/freesurfer
subject sub-01
outvol mri/wmparc.mgz
useribbon 0
baseoffset 0
labeling wm
labeling hypo-intensities as wm
dmaxctx 5.000000
RipUnknown 1
CtxSeg /out/freesurfer/sub-01/mri/aparc+aseg.mgz

Reading lh white surface 
 /out/freesurfer/sub-01/surf/lh.white

Reading lh pial surface 
 /out/freesurfer/sub-01/surf/lh.pial

Loading lh annotations from /out/freesurfer/sub-01/label/lh.aparc.annot
reading colortable from annotation file...
colortable with 36 entries read (originally /autofs/space/tanha_002/users/greve/fsdev.build/average/colortable_desikan_killiany.txt)

Reading rh white surface 
 /out/freesurfer/sub-01/surf/rh.white

Reading rh pial surface 
 /out/freesurfer/sub-01/surf/rh.pial

Loading rh annotations from /out/freesurfer/sub-01/label/rh.aparc.annot
reading colortable from annotation file...
colortable with 36 entries read (originally /autofs/space/tanha_002/users/greve/fsdev.build/average/colortable_desikan_killiany.txt)
Have color table for lh white annotation
Have color table for rh white annotation
Loading ribbon segmentation from /out/freesurfer/sub-01/mri/ribbon.mgz
Loading filled from /out/freesurfer/sub-01/mri/ribbon.mgz
Ripping vertices labeled as unkown
Ripped 2979 vertices from left hemi
Ripped 2060 vertices from right hemi

Building hash of lh white

Building hash of lh pial

Building hash of rh white

Building hash of rh pial

Loading aseg from /out/freesurfer/sub-01/mri/aseg.mgz
Loading Ctx Seg File /out/freesurfer/sub-01/mri/aparc+aseg.mgz
ASeg Vox2RAS: -----------
-1.00000   0.00000   0.00000   128.00000;
 0.00000   0.00000   1.00000  -128.00000;
 0.00000  -1.00000   0.00000   128.00000;
 0.00000   0.00000   0.00000   1.00000;
-------------------------

Labeling Slice
  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19 
 20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39 
 40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59 
 60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79 
 80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 
100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 
120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 
140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 
160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 
180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 
200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 
220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 
240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 nctx = 89868
Used brute-force search on 0 voxels
Fixing Parahip LH WM
  Found 3 clusters
     0 k 12.000000
     1 k 20.000000
     2 k 1.000000
Fixing Parahip RH WM
  Found 14 clusters
     0 k 1.000000
     1 k 645.000000
     2 k 1.000000
     3 k 6.000000
     4 k 1.000000
     5 k 1.000000
     6 k 5.000000
     7 k 3.000000
     8 k 4.000000
     9 k 2.000000
     10 k 1.000000
     11 k 1.000000
     12 k 1.000000
     13 k 1.000000
Writing output aseg to mri/wmparc.mgz

 mri_segstats --seg mri/wmparc.mgz --sum stats/wmparc.stats --pv mri/norm.mgz --excludeid 0 --brainmask mri/brainmask.mgz --in mri/norm.mgz --in-intensity-name norm --in-intensity-units MR --subject sub-01 --surf-wm-vol --ctab /opt/freesurfer/WMParcStatsLUT.txt --etiv 


$Id: mri_segstats.c,v 1.121 2016/05/31 17:27:11 greve Exp $
cwd 
cmdline mri_segstats --seg mri/wmparc.mgz --sum stats/wmparc.stats --pv mri/norm.mgz --excludeid 0 --brainmask mri/brainmask.mgz --in mri/norm.mgz --in-intensity-name norm --in-intensity-units MR --subject sub-01 --surf-wm-vol --ctab /opt/freesurfer/WMParcStatsLUT.txt --etiv 
sysname  Linux
hostname efad4839b3da
machine  x86_64
user     root
UseRobust  0
atlas_icv (eTIV) = 120544 mm^3    (det: 16.160946 )
Loading mri/wmparc.mgz
Getting Brain Volume Statistics
lhCtxGM: 16316.327 15835.000  diff=  481.3  pctdiff= 2.950
rhCtxGM: 30120.634 29939.000  diff=  181.6  pctdiff= 0.603
lhCtxWM: 21969.726 22859.000  diff= -889.3  pctdiff=-4.048
rhCtxWM: 21129.806 21159.000  diff=  -29.2  pctdiff=-0.138
SubCortGMVol   6695.000
SupraTentVol  100537.493 (98089.000) diff=2448.493 pctdiff=2.435
SupraTentVolNotVent  99155.493 (96707.000) diff=2448.493 pctdiff=2.469
BrainSegVol  110978.000 (110862.000) diff=116.000 pctdiff=0.105
BrainSegVolNotVent  109402.000 (109139.493) diff=262.507 pctdiff=0.240
BrainSegVolNotVent  109402.000
CerebellumVol 12688.000
VentChorVol    1382.000
3rd4th5thCSF    194.000
CSFVol    81.000, OptChiasmVol     4.000
MaskVol 177473.000
Loading mri/norm.mgz
Loading mri/norm.mgz
Voxel Volume is 1 mm^3
Generating list of segmentation ids
Found 390 segmentations
Computing statistics for each segmentation

Reporting on  65 segmentations
Using PrintSegStat
mri_segstats done

Started at Mon Feb 16 20:50:28 UTC 2026 
Ended   at Mon Feb 16 21:04:06 UTC 2026
#@#%# recon-all-run-time-hours 0.227
recon-all -s sub-01 finished without error at Mon Feb 16 21:04:06 UTC 2026
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

