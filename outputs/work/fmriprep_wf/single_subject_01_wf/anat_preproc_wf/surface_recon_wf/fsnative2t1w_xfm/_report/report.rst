Node: single_subject_01_wf (anat_preproc_wf (surface_recon_wf (fsnative2t1w_xfm (freesurfer)
============================================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.surface_recon_wf.fsnative2t1w_xfm
 Exec ID : fsnative2t1w_xfm


Original Inputs
---------------


* args : <undefined>
* auto_sens : True
* environ : {'SUBJECTS_DIR': '/opt/freesurfer/subjects'}
* est_int_scale : True
* force_double : <undefined>
* force_float : <undefined>
* half_source : <undefined>
* half_source_xfm : <undefined>
* half_targ : <undefined>
* half_targ_xfm : <undefined>
* half_weights : <undefined>
* high_iterations : <undefined>
* in_xfm_file : <undefined>
* init_orient : <undefined>
* iteration_thresh : <undefined>
* least_squares : <undefined>
* mask_source : <undefined>
* mask_target : <undefined>
* max_iterations : <undefined>
* no_init : <undefined>
* no_multi : <undefined>
* out_reg_file : True
* outlier_limit : <undefined>
* outlier_sens : <undefined>
* registered_file : <undefined>
* source_file : /out/freesurfer/sub-01/mri/T1.mgz
* subjects_dir : /opt/freesurfer/subjects
* subsample_thresh : <undefined>
* target_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz
* trans_only : <undefined>
* weights_file : <undefined>
* write_vo2vox : <undefined>


Execution Inputs
----------------


* args : <undefined>
* auto_sens : True
* environ : {'SUBJECTS_DIR': '/opt/freesurfer/subjects'}
* est_int_scale : True
* force_double : <undefined>
* force_float : <undefined>
* half_source : <undefined>
* half_source_xfm : <undefined>
* half_targ : <undefined>
* half_targ_xfm : <undefined>
* half_weights : <undefined>
* high_iterations : <undefined>
* in_xfm_file : <undefined>
* init_orient : <undefined>
* iteration_thresh : <undefined>
* least_squares : <undefined>
* mask_source : <undefined>
* mask_target : <undefined>
* max_iterations : <undefined>
* no_init : <undefined>
* no_multi : <undefined>
* out_reg_file : True
* outlier_limit : <undefined>
* outlier_sens : <undefined>
* registered_file : <undefined>
* source_file : /out/freesurfer/sub-01/mri/T1.mgz
* subjects_dir : /opt/freesurfer/subjects
* subsample_thresh : <undefined>
* target_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz
* trans_only : <undefined>
* weights_file : <undefined>
* write_vo2vox : <undefined>


Execution Outputs
-----------------


* half_source : <undefined>
* half_source_xfm : <undefined>
* half_targ : <undefined>
* half_targ_xfm : <undefined>
* half_weights : <undefined>
* out_reg_file : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta
* registered_file : <undefined>
* weights_file : <undefined>


Runtime info
------------


* cmdline : mri_robust_register --satit --iscale --lta /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta --mov /out/freesurfer/sub-01/mri/T1.mgz --dst /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz
* duration : 59.005641
* hostname : 87a7076871ed
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 $Id: mri_robust_register.cpp,v 1.77 2016/01/20 23:36:17 greve Exp $

--satit: Will iterate with different SAT to ensure outliers below wlimit!
--iscale: Enableing intensity scaling!
--lta: Output transform as /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta . 
--mov: Using /out/freesurfer/sub-01/mri/T1.mgz as movable/source volume.
--dst: Using /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz as target volume.

reading source '/out/freesurfer/sub-01/mri/T1.mgz'...
reading target '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/anat_validate/sub-01_T1w_ras_valid.nii.gz'...

Registration::setSourceAndTarget(MRI s, MRI t, keeptype = TRUE )
   Type Source : 0  Type Target : 3  ensure both FLOAT (3)
   Reordering axes in mov to better fit dst... ( -1 -3 2 )
MRIreorder() -----------
xdim=-1 ydim=-3 zdim=2
src 256 256 256, 1.000000 1.000000 1.000000
dst 256 256 256, 1.000000 1.000000 1.000000
 Determinant after swap : 1
   Mov: (1, 1, 1)mm  and dim (256, 256, 256)
   Dst: (1, 1, 1)mm  and dim (64, 64, 64)
   Asserting both images: 1mm isotropic 
    - reslicing Mov ...
       -- changing data type from 0 to 3 (noscale = 0)...
    - reslicing Dst ...
       -- Original : (1, 1, 1)mm and (64, 64, 64) voxels.
       -- Resampled: (1, 1, 1)mm and (256, 256, 256) voxels.
       -- Reslicing using cubic bspline 
MRItoBSpline degree 3


 Registration::findSaturation 
   - computing centroids 
   - computing initial transform
     -- using translation info
   - Get Gaussian Pyramid Limits ( min size: 16 max size: -1 ) 
   - Build Gaussian Pyramid ( Limits min steps: 0 max steps: 3 ) 
   - Build Gaussian Pyramid ( Limits min steps: 0 max steps: 3 ) 

   - Max Resolution used: 2
     -- gpS ( 64 , 64 , 64 )
     -- gpT ( 64 , 64 , 64 )
   - running loop to estimate saturation parameter:
     -- Iteration: 1  trying sat: 16
         min sat: 16 ( 0.54495 ), max sat: 0 ( -1 ), sat diff: -16, (wlimit=0.16)
     -- Iteration: 2  trying sat: 32
         min sat: 32 ( 0.507114 ), max sat: 0 ( -1 ), sat diff: -32, (wlimit=0.16)
     -- Iteration: 3  trying sat: 64
         min sat: 64 ( 0.473128 ), max sat: 0 ( -1 ), sat diff: -64, (wlimit=0.16)
     -- Iteration: 4  trying sat: 128
         min sat: 128 ( 0.437735 ), max sat: 0 ( -1 ), sat diff: -128, (wlimit=0.16)
     -- Iteration: 5  trying sat: 256
         min sat: 256 ( 0.411936 ), max sat: 0 ( -1 ), sat diff: -256, (wlimit=0.16)
     -- Iteration: 6  trying sat: 512
         min sat: 512 ( 0.382257 ), max sat: 0 ( -1 ), sat diff: -512, (wlimit=0.16)
     -- Iteration: 7  trying sat: 1024
         min sat: 1024 ( 0.330505 ), max sat: 0 ( -1 ), sat diff: -1024, (wlimit=0.16)
     -- Iteration: 8  trying sat: 2048
         min sat: 2048 ( 0.277088 ), max sat: 0 ( -1 ), sat diff: -2048, (wlimit=0.16)
     -- Iteration: 9  trying sat: 4096
         min sat: 4096 ( 0.206184 ), max sat: 0 ( -1 ), sat diff: -4096, (wlimit=0.16)
     -- Iteration: 10  trying sat: 8192
         min sat: 4096 ( 0.206184 ), max sat: 8192 ( 0.143109 ), sat diff: 4096, (wlimit=0.16)
     -- Iteration: 11  trying sat: 6144
         min sat: 6144 ( 0.170661 ), max sat: 8192 ( 0.143109 ), sat diff: 2048, (wlimit=0.16)
     -- Iteration: 12  trying sat: 7168
         min sat: 6144 ( 0.170661 ), max sat: 7168 ( 0.154656 ), sat diff: 1024, (wlimit=0.16)
     -- Iteration: 13  trying sat: 6656
         min sat: 6656 ( 0.162194 ), max sat: 7168 ( 0.154656 ), sat diff: 512, (wlimit=0.16)
     -- Iteration: 14  trying sat: 6912
         min sat: 6656 ( 0.162194 ), max sat: 6912 ( 0.15816 ), sat diff: 256, (wlimit=0.16)
     -- Iteration: 15  trying sat: 6784
         min sat: 6784 ( 0.160332 ), max sat: 6912 ( 0.15816 ), sat diff: 128, (wlimit=0.16)
     -- Iteration: 16  trying sat: 6848
         min sat: 6784 ( 0.160332 ), max sat: 6848 ( 0.15926 ), sat diff: 64, (wlimit=0.16)
     -- Iteration: 17  trying sat: 6816
         min sat: 6784 ( 0.160332 ), max sat: 6816 ( 0.159856 ), sat diff: 32, (wlimit=0.16)
     -- Iteration: 18  trying sat: 6800
         min sat: 6800 ( 0.16022 ), max sat: 6816 ( 0.159856 ), sat diff: 16, (wlimit=0.16)
     -- Iteration: 19  trying sat: 6808
         min sat: 6808 ( 0.160018 ), max sat: 6816 ( 0.159856 ), sat diff: 8, (wlimit=0.16)
     -- Iteration: 20  trying sat: 6812
         min sat: 6808 ( 0.160018 ), max sat: 6812 ( 0.159915 ), sat diff: 4, (wlimit=0.16)
     -- Iteration: 21  trying sat: 6810
         min sat: 6808 ( 0.160018 ), max sat: 6810 ( 0.159964 ), sat diff: 2, (wlimit=0.16)
     -- Iteration: 22  trying sat: 6809
         min sat: 6809 ( 0.160009 ), max sat: 6810 ( 0.159964 ), sat diff: 1, (wlimit=0.16)
     -- Iteration: 23  trying sat: 6809.5
   - final SAT: 6809.5 ( it: 23 , weight check 0.15998 <= 0.16 )


 Registration::computeMultiresRegistration 
   - computing centroids 
   - computing initial transform
     -- using translation info
   - Get Gaussian Pyramid Limits ( min size: 16 max size: -1 ) 
   - initial transform:
Ti = [ ...
 1.0000000000000                0                0  0.7549524825104 
               0  1.0000000000000                0  1.3782336188040 
               0                0  1.0000000000000  2.7980857517232 
               0                0                0  1.0000000000000  ]

   - initial iscale:  Ii =1

Resolution: 3  S( 32 32 32 )  T( 32 32 32 )
 Iteration(f): 1
     -- intensity log diff: abs(-0.95429) 
     -- diff. to prev. transform: 0.493125
 Iteration(f): 2
     -- intensity log diff: abs(-0.0364415) 
     -- diff. to prev. transform: 0.384735
 Iteration(f): 3
     -- intensity log diff: abs(-0.00827196) 
     -- diff. to prev. transform: 0.135826
 Iteration(f): 4
     -- intensity log diff: abs(-0.00612299) 
     -- diff. to prev. transform: 0.176862
 Iteration(f): 5
     -- intensity log diff: abs(-0.00475979) 
     -- diff. to prev. transform: 0.175329 max it: 5 reached!

Resolution: 2  S( 64 64 64 )  T( 64 64 64 )
 Iteration(f): 1
     -- intensity log diff: abs(-0.00466659) 
     -- diff. to prev. transform: 0.234584
 Iteration(f): 2
     -- intensity log diff: abs(0.00115124) 
     -- diff. to prev. transform: 0.0328487
 Iteration(f): 3
     -- intensity log diff: abs(0.000109859)  <= 0.001  :-)
     -- diff. to prev. transform: 0.00391814  <= 0.01   :-)

Resolution: 1  S( 128 128 128 )  T( 128 128 128 )
 Iteration(f): 1
     -- intensity log diff: abs(-0.0651463) 
     -- diff. to prev. transform: 0.864178
 Iteration(f): 2
     -- intensity log diff: abs(-0.00422779) 
     -- diff. to prev. transform: 0.10776
 Iteration(f): 3
     -- intensity log diff: abs(-4.10415e-06)  <= 0.001  :-)
     -- diff. to prev. transform: 0.0040272  <= 0.01   :-)

Resolution: 0  S( 256 256 256 )  T( 256 256 256 )
 Iteration(f): 1
     -- intensity log diff: abs(0.00141693) 
     -- diff. to prev. transform: 0.423663
 Iteration(f): 2
     -- intensity log diff: abs(4.03255e-05)  <= 0.001  :-)
     -- diff. to prev. transform: 0.0421915
 Iteration(f): 3
     -- intensity log diff: abs(1.19626e-05)  <= 0.001  :-)
     -- diff. to prev. transform: 0.00370012  <= 0.01   :-)

   - final transform: 
Tf = [ ...
 0.9999991587311 -0.0012789570577 -0.0002163467389  1.1786573942830 
 0.0012790108202  0.9999991511777  0.0002485463705 -0.0797213166937 
 0.0002160286751 -0.0002488228712  0.9999999457094  1.1676807672993 
               0                0                0  1.0000000000000  ]

   - final iscale:  If = 2.94822

Final Transform:
Adjusting final transform due to initial resampling (voxel or size changes) ...
M = [ ...
-0.9999991587311  0.0002163467389 -0.0012789570577 160.1232668229064 
-0.0012790108202 -0.0002485463705  0.9999991511777 -95.6901942330638 
-0.0002160286751 -0.9999999457094 -0.0002488228712 160.2227542353485 
               0                0                0  1.0000000000000  ]

 Determinant : -1

Intenstiy Scale Factor: 2.94822

writing output transformation to /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/surface_recon_wf/fsnative2t1w_xfm/T1_robustreg.lta ...
converting VOX to RAS and saving RAS2RAS...
Adjusting Intensity of MOV by 2.94822


Registration took 0 minutes and 58 seconds.

 Thank you for using RobustRegister! 
 If you find it useful and use it for a publication, please cite: 

 Highly Accurate Inverse Consistent Registration: A Robust Approach
 M. Reuter, H.D. Rosas, B. Fischl.  NeuroImage 53(4):1181-1196, 2010.
 http://dx.doi.org/10.1016/j.neuroimage.2010.07.020
 http://reuter.mit.edu/papers/reuter-robreg10.pdf



Terminal - standard error
~~~~~~~~~~~~~~~~~~~~~~~~~


 makeIsotropic WARNING: not different enough, won't reslice!


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

