Node: single_subject_01_wf (anat_preproc_wf (brain_extraction_wf (norm (fixes)
==============================================================================


 Hierarchy : fmriprep_wf.single_subject_01_wf.anat_preproc_wf.brain_extraction_wf.norm
 Exec ID : norm


Original Inputs
---------------


* args : <undefined>
* collapse_output_transforms : True
* convergence_threshold : [1e-08, 1e-08, 1e-09]
* convergence_window_size : [10, 10, 15]
* dimension : 3
* environ : {'NSLOTS': '8'}
* fixed_image : ['/home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_tmpl/tpl-OASIS30ANTs_res-01_T1w_maths.nii.gz']
* fixed_image_mask : <undefined>
* fixed_image_masks : ['/home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz']
* float : True
* initial_moving_transform : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/init_aff/initialization.mat']
* initial_moving_transform_com : <undefined>
* initialize_transforms_per_stage : False
* interpolation : LanczosWindowedSinc
* interpolation_parameters : <undefined>
* invert_initial_moving_transform : <undefined>
* metric : ['MI', 'MI', ['CC', 'CC']]
* metric_item_trait : <undefined>
* metric_stage_trait : <undefined>
* metric_weight : [1.0, 1.0, [0.5, 0.5]]
* metric_weight_item_trait : 1.0
* metric_weight_stage_trait : <undefined>
* moving_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_target/sub-01_T1w_ras_valid_maths_corrected_maths.nii.gz']
* moving_image_mask : <undefined>
* moving_image_masks : <undefined>
* num_threads : 8
* number_of_iterations : [[100, 100, 50, 10], [100, 100, 50, 10], [5, 0]]
* output_inverse_warped_image : <undefined>
* output_transform_prefix : anat_to_template
* output_warped_image : True
* radius_bins_item_trait : 5
* radius_bins_stage_trait : <undefined>
* radius_or_number_of_bins : [32, 32, [4, 4]]
* restore_state : <undefined>
* restrict_deformation : <undefined>
* sampling_percentage : [0.25, 0.25, [1.0, 1.0]]
* sampling_percentage_item_trait : <undefined>
* sampling_percentage_stage_trait : <undefined>
* sampling_strategy : ['Regular', 'Regular', ['None', 'None']]
* sampling_strategy_item_trait : <undefined>
* sampling_strategy_stage_trait : <undefined>
* save_state : <undefined>
* shrink_factors : [[8, 4, 2, 1], [8, 4, 2, 1], [2, 1]]
* sigma_units : ['vox', 'vox', 'vox']
* smoothing_sigmas : [[4.0, 2.0, 1.0, 0.0], [4.0, 2.0, 1.0, 0.0], [1.0, 0.0]]
* transform_parameters : [(0.1,), (0.1,), (0.1, 3.0, 0.0)]
* transforms : ['Rigid', 'Affine', 'SyN']
* use_estimate_learning_rate_once : <undefined>
* use_histogram_matching : True
* verbose : True
* winsorize_lower_quantile : 0.025
* winsorize_upper_quantile : 0.975
* write_composite_transform : False


Execution Inputs
----------------


* args : <undefined>
* collapse_output_transforms : True
* convergence_threshold : [1e-08, 1e-08, 1e-09]
* convergence_window_size : [10, 10, 15]
* dimension : 3
* environ : {'NSLOTS': '8'}
* fixed_image : ['/home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_tmpl/tpl-OASIS30ANTs_res-01_T1w_maths.nii.gz']
* fixed_image_mask : <undefined>
* fixed_image_masks : ['/home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz']
* float : True
* initial_moving_transform : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/init_aff/initialization.mat']
* initial_moving_transform_com : <undefined>
* initialize_transforms_per_stage : False
* interpolation : LanczosWindowedSinc
* interpolation_parameters : <undefined>
* invert_initial_moving_transform : <undefined>
* metric : ['MI', 'MI', ['CC', 'CC']]
* metric_item_trait : <undefined>
* metric_stage_trait : <undefined>
* metric_weight : [1.0, 1.0, [0.5, 0.5]]
* metric_weight_item_trait : 1.0
* metric_weight_stage_trait : <undefined>
* moving_image : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_target/sub-01_T1w_ras_valid_maths_corrected_maths.nii.gz']
* moving_image_mask : <undefined>
* moving_image_masks : <undefined>
* num_threads : 8
* number_of_iterations : [[100, 100, 50, 10], [100, 100, 50, 10], [5, 0]]
* output_inverse_warped_image : <undefined>
* output_transform_prefix : anat_to_template
* output_warped_image : True
* radius_bins_item_trait : 5
* radius_bins_stage_trait : <undefined>
* radius_or_number_of_bins : [32, 32, [4, 4]]
* restore_state : <undefined>
* restrict_deformation : <undefined>
* sampling_percentage : [0.25, 0.25, [1.0, 1.0]]
* sampling_percentage_item_trait : <undefined>
* sampling_percentage_stage_trait : <undefined>
* sampling_strategy : ['Regular', 'Regular', ['None', 'None']]
* sampling_strategy_item_trait : <undefined>
* sampling_strategy_stage_trait : <undefined>
* save_state : <undefined>
* shrink_factors : [[8, 4, 2, 1], [8, 4, 2, 1], [2, 1]]
* sigma_units : ['vox', 'vox', 'vox']
* smoothing_sigmas : [[4.0, 2.0, 1.0, 0.0], [4.0, 2.0, 1.0, 0.0], [1.0, 0.0]]
* transform_parameters : [(0.1,), (0.1,), (0.1, 3.0, 0.0)]
* transforms : ['Rigid', 'Affine', 'SyN']
* use_estimate_learning_rate_once : <undefined>
* use_histogram_matching : True
* verbose : True
* winsorize_lower_quantile : 0.025
* winsorize_upper_quantile : 0.975
* write_composite_transform : False


Execution Outputs
-----------------


* composite_transform : <undefined>
* elapsed_time : <undefined>
* forward_invert_flags : <undefined>
* forward_transforms : <undefined>
* inverse_composite_transform : <undefined>
* inverse_warped_image : <undefined>
* metric_value : <undefined>
* reverse_forward_invert_flags : <undefined>
* reverse_forward_transforms : <undefined>
* reverse_invert_flags : [True, False]
* reverse_transforms : ['/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template0GenericAffine.mat', '/out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm/anat_to_template1InverseWarp.nii.gz']
* save_state : <undefined>
* warped_image : <undefined>


Runtime info
------------


* cmdline : antsRegistration --collapse-output-transforms 1 --dimensionality 3 --float 1 --initial-moving-transform [ /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/init_aff/initialization.mat, 0 ] --initialize-transforms-per-stage 0 --interpolation LanczosWindowedSinc --output [ anat_to_template, anat_to_template_Warped.nii.gz ] --transform Rigid[ 0.1 ] --metric MI[ /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz, /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz, 1, 32, Regular, 0.25 ] --convergence [ 100x100x50x10, 1e-08, 10 ] --smoothing-sigmas 4.0x2.0x1.0x0.0vox --shrink-factors 8x4x2x1 --use-histogram-matching 1 --masks [ /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz, NULL ] --transform Affine[ 0.1 ] --metric MI[ /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz, /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz, 1, 32, Regular, 0.25 ] --convergence [ 100x100x50x10, 1e-08, 10 ] --smoothing-sigmas 4.0x2.0x1.0x0.0vox --shrink-factors 8x4x2x1 --use-histogram-matching 1 --masks [ /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz, NULL ] --transform SyN[ 0.1, 3.0, 0.0 ] --metric CC[ /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz, /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz, 0.5, 4, None, 1 ] --metric CC[ /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_tmpl/tpl-OASIS30ANTs_res-01_T1w_maths.nii.gz, /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_target/sub-01_T1w_ras_valid_maths_corrected_maths.nii.gz, 0.5, 4, None, 1 ] --convergence [ 5x0, 1e-09, 15 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-histogram-matching 1 --masks [ /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz, NULL ] -v --winsorize-image-intensities [ 0.025, 0.975 ]  --write-composite-transform 0
* duration : 397.864026
* hostname : 87a7076871ed
* prev_wd : /tmp
* working_dir : /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/norm


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 All_Command_lines_OK
Using single precision for computations.
=============================================================================
The composite transform comprises the following transforms (in order): 
  1. /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/init_aff/initialization.mat (type = AffineTransform)
=============================================================================
  Reading mask(s).
    Registration stage 0
      Fixed mask = /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz
      No moving mask
    Registration stage 1
      Fixed mask = /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz
      No moving mask
    Registration stage 2
      Fixed mask = /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_desc-BrainCerebellumExtraction_mask.nii.gz
      No moving mask
  number of levels = 4
  number of levels = 4
  number of levels = 2
  fixed image: /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz
  moving image: /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz
  fixed image: /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz
  moving image: /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz
  fixed image: /home/fmriprep/.cache/templateflow/tpl-OASIS30ANTs/tpl-OASIS30ANTs_res-01_T1w.nii.gz
  moving image: /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/inu_n4/mapflow/_inu_n40/sub-01_T1w_ras_valid_maths_corrected.nii.gz
  fixed image: /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_tmpl/tpl-OASIS30ANTs_res-01_T1w_maths.nii.gz
  moving image: /out/work/fmriprep_wf/single_subject_01_wf/anat_preproc_wf/brain_extraction_wf/lap_target/sub-01_T1w_ras_valid_maths_corrected_maths.nii.gz
Dimension = 3
Number of stages = 3
Use Histogram Matching true
Winsorize image intensities true
Lower quantile = 0.025
Upper quantile = 0.975
Stage 1 State
   Image metric = Mattes
     Fixed image = Image (0x3f64b40)
  RTTI typeinfo:   itk::Image<float, 3u>
  Reference Count: 2
  Modified Time: 2149
  Debug: Off
  Object Name: 
  Observers: 
    none
  Source: (none)
  Source output name: (none)
  Release Data: Off
  Data Released: False
  Global Release Data: Off
  PipelineMTime: 0
  UpdateMTime: 1934
  RealTimeStamp: 0 seconds 
  LargestPossibleRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  BufferedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  RequestedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  Spacing: [1, 1, 1]
  Origin: [215, 293, -255]
  Direction: 
-1 0 0
0 -1 0
0 0 1

  IndexToPointMatrix: 
-1 0 0
0 -1 0
0 0 1

  PointToIndexMatrix: 
-1 0 0
0 -1 0
0 0 1

  Inverse Direction: 
-1 0 0
0 -1 0
0 0 1

  PixelContainer: 
    ImportImageContainer (0x3f64dd0)
      RTTI typeinfo:   itk::ImportImageContainer<unsigned long, float>
      Reference Count: 1
      Modified Time: 1931
      Debug: Off
      Object Name: 
      Observers: 
        none
      Pointer: 0x7ffff566f010
      Container manages memory: true
      Size: 16091136
      Capacity: 16091136

     Moving image = Image (0x3006e60)
  RTTI typeinfo:   itk::Image<float, 3u>
  Reference Count: 2
  Modified Time: 2150
  Debug: Off
  Object Name: 
  Observers: 
    none
  Source: (none)
  Source output name: (none)
  Release Data: Off
  Data Released: False
  Global Release Data: Off
  PipelineMTime: 0
  UpdateMTime: 2147
  RealTimeStamp: 0 seconds 
  LargestPossibleRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  BufferedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  RequestedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  Spacing: [1, 1, 1]
  Origin: [60.8313, 128.946, -127.5]
  Direction: 
-1 0 0
0 -1 0
0 0 1

  IndexToPointMatrix: 
-1 0 0
0 -1 0
0 0 1

  PointToIndexMatrix: 
-1 0 0
0 -1 0
0 0 1

  Inverse Direction: 
-1 0 0
0 -1 0
0 0 1

  PixelContainer: 
    ImportImageContainer (0x4ec2680)
      RTTI typeinfo:   itk::ImportImageContainer<unsigned long, float>
      Reference Count: 1
      Modified Time: 2144
      Debug: Off
      Object Name: 
      Observers: 
        none
      Pointer: 0x4ec3490
      Container manages memory: true
      Size: 262144
      Capacity: 262144

     Weighting = 1
     Sampling strategy = regular
     Number of bins = 32
     Radius = 4
     Sampling percentage  = 0.25
   Transform = Rigid
     Gradient step = 0.1
     Update field sigma (voxel space) = 0
     Total field sigma (voxel space) = 0
     Update field time sigma = 0
     Total field time sigma  = 0
     Number of time indices = 0
     Number of time point samples = 0
Stage 2 State
   Image metric = Mattes
     Fixed image = Image (0x4fc34a0)
  RTTI typeinfo:   itk::Image<float, 3u>
  Reference Count: 2
  Modified Time: 2577
  Debug: Off
  Object Name: 
  Observers: 
    none
  Source: (none)
  Source output name: (none)
  Release Data: Off
  Data Released: False
  Global Release Data: Off
  PipelineMTime: 0
  UpdateMTime: 2362
  RealTimeStamp: 0 seconds 
  LargestPossibleRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  BufferedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  RequestedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  Spacing: [1, 1, 1]
  Origin: [215, 293, -255]
  Direction: 
-1 0 0
0 -1 0
0 0 1

  IndexToPointMatrix: 
-1 0 0
0 -1 0
0 0 1

  PointToIndexMatrix: 
-1 0 0
0 -1 0
0 0 1

  Inverse Direction: 
-1 0 0
0 -1 0
0 0 1

  PixelContainer: 
    ImportImageContainer (0x2ffd0e0)
      RTTI typeinfo:   itk::ImportImageContainer<unsigned long, float>
      Reference Count: 1
      Modified Time: 2359
      Debug: Off
      Object Name: 
      Observers: 
        none
      Pointer: 0x7ffff190c010
      Container manages memory: true
      Size: 16091136
      Capacity: 16091136

     Moving image = Image (0x4fc7880)
  RTTI typeinfo:   itk::Image<float, 3u>
  Reference Count: 2
  Modified Time: 2578
  Debug: Off
  Object Name: 
  Observers: 
    none
  Source: (none)
  Source output name: (none)
  Release Data: Off
  Data Released: False
  Global Release Data: Off
  PipelineMTime: 0
  UpdateMTime: 2575
  RealTimeStamp: 0 seconds 
  LargestPossibleRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  BufferedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  RequestedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  Spacing: [1, 1, 1]
  Origin: [60.8313, 128.946, -127.5]
  Direction: 
-1 0 0
0 -1 0
0 0 1

  IndexToPointMatrix: 
-1 0 0
0 -1 0
0 0 1

  PointToIndexMatrix: 
-1 0 0
0 -1 0
0 0 1

  Inverse Direction: 
-1 0 0
0 -1 0
0 0 1

  PixelContainer: 
    ImportImageContainer (0x4ec19a0)
      RTTI typeinfo:   itk::ImportImageContainer<unsigned long, float>
      Reference Count: 1
      Modified Time: 2572
      Debug: Off
      Object Name: 
      Observers: 
        none
      Pointer: 0x4fc8d10
      Container manages memory: true
      Size: 262144
      Capacity: 262144

     Weighting = 1
     Sampling strategy = regular
     Number of bins = 32
     Radius = 4
     Sampling percentage  = 0.25
   Transform = Affine
     Gradient step = 0.1
     Update field sigma (voxel space) = 0
     Total field sigma (voxel space) = 0
     Update field time sigma = 0
     Total field time sigma  = 0
     Number of time indices = 0
     Number of time point samples = 0
Stage 3 State
   Image metric = CC
     Fixed image = Image (0x50c8d20)
  RTTI typeinfo:   itk::Image<float, 3u>
  Reference Count: 2
  Modified Time: 3005
  Debug: Off
  Object Name: 
  Observers: 
    none
  Source: (none)
  Source output name: (none)
  Release Data: Off
  Data Released: False
  Global Release Data: Off
  PipelineMTime: 0
  UpdateMTime: 2790
  RealTimeStamp: 0 seconds 
  LargestPossibleRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  BufferedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  RequestedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [216, 291, 256]
  Spacing: [1, 1, 1]
  Origin: [215, 293, -255]
  Direction: 
-1 0 0
0 -1 0
0 0 1

  IndexToPointMatrix: 
-1 0 0
0 -1 0
0 0 1

  PointToIndexMatrix: 
-1 0 0
0 -1 0
0 0 1

  Inverse Direction: 
-1 0 0
0 -1 0
0 0 1

  PixelContainer: 
    ImportImageContainer (0x3007e70)
      RTTI typeinfo:   itk::ImportImageContainer<unsigned long, float>
      Reference Count: 1
      Modified Time: 2787
      Debug: Off
      Object Name: 
      Observers: 
        none
      Pointer: 0x7fffedba9010
      Container manages memory: true
      Size: 16091136
      Capacity: 16091136

     Moving image = Image (0x50cd0c0)
  RTTI typeinfo:   itk::Image<float, 3u>
  Reference Count: 2
  Modified Time: 3006
  Debug: Off
  Object Name: 
  Observers: 
    none
  Source: (none)
  Source output name: (none)
  Release Data: Off
  Data Released: False
  Global Release Data: Off
  PipelineMTime: 0
  UpdateMTime: 3003
  RealTimeStamp: 0 seconds 
  LargestPossibleRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  BufferedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  RequestedRegion: 
    Dimension: 3
    Index: [0, 0, 0]
    Size: [64, 64, 64]
  Spacing: [1, 1, 1]
  Origin: [60.8313, 128.946, -127.5]
  Direction: 
-1 0 0
0 -1 0
0 0 1

  IndexToPointMatrix: 
-1 0 0
0 -1 0
0 0 1

  PointToIndexMatrix: 
-1 0 0
0 -1 0
0 0 1

  Inverse Direction: 
-1 0 0
0 -1 0
0 0 1

  PixelContainer: 
    ImportImageContainer (0x4fc6890)
      RTTI typeinfo:   itk::ImportImageContainer<unsigned long, float>
      Reference Count: 1
      Modified Time: 3000
      Debug: Off
      Object Name: 
      Observers: 
        none
      Pointer: 0x50ce550
      Container manages memory: true
      Size: 262144
      Capacity: 262144

     Weighting = 0.5
     Sampling strategy = none
     Number of bins = 32
     Radius = 4
     Sampling percentage  = 1
   Transform = SyN
     Gradient step = 0.1
     Update field sigma (voxel space) = 3
     Total field sigma (voxel space) = 0
     Update field time sigma = 0
     Total field time sigma  = 0
     Number of time indices = 0
     Number of time point samples = 0
Registration using 3 total stages.

Stage 0
  iterations = 100x100x50x10
  convergence threshold = 1e-08
  convergence window size = 10
  number of levels = 4
  using the Mattes MI metric (number of bins = 32, weight = 1)
  preprocessing:  winsorizing the image intensities
  preprocessing:  histogram matching the images
  Shrink factors (level 1 out of 4): [8, 8, 8]
  Shrink factors (level 2 out of 4): [4, 4, 4]
  Shrink factors (level 3 out of 4): [2, 2, 2]
  Shrink factors (level 4 out of 4): [1, 1, 1]
  smoothing sigmas per level: [4, 2, 1, 0]
  regular sampling (percentage = 0.25)

*** Running Euler3DTransform registration ***

DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -6.493126153946e-01, inf, 4.5569e-01, 4.5559e-01, 
 2DIAGNOSTIC,     2, -6.555143594742e-01, inf, 4.5786e-01, 2.1679e-03, 
 2DIAGNOSTIC,     3, -6.586304306984e-01, inf, 4.6111e-01, 3.2520e-03, 
 2DIAGNOSTIC,     4, -6.838776469231e-01, inf, 4.6376e-01, 2.6510e-03, 
 2DIAGNOSTIC,     5, -6.843810677528e-01, inf, 4.6616e-01, 2.3942e-03, 
 2DIAGNOSTIC,     6, -6.901707649231e-01, inf, 4.6820e-01, 2.0459e-03, 
 2DIAGNOSTIC,     7, -7.563319206238e-01, inf, 4.7040e-01, 2.1999e-03, 
 2DIAGNOSTIC,     8, -7.730598449707e-01, inf, 4.7244e-01, 2.0351e-03, 
 2DIAGNOSTIC,     9, -7.753449678421e-01, inf, 4.7494e-01, 2.5079e-03, 
 2DIAGNOSTIC,    10, -7.789995074272e-01, 1.398233044893e-02, 4.8574e-01, 1.0800e-02, 
 2DIAGNOSTIC,    11, -7.787488102913e-01, 1.243709027767e-02, 4.8871e-01, 2.9678e-03, 
 2DIAGNOSTIC,    12, -8.254536986351e-01, 1.170612871647e-02, 4.9153e-01, 2.8160e-03, 
 2DIAGNOSTIC,    13, -6.681131124496e-01, 5.477008875459e-03, 4.9474e-01, 3.2148e-03, 
 2DIAGNOSTIC,    14, -6.557687520981e-01, 1.136609644163e-04, 5.0543e-01, 1.0683e-02, 
DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -1.978043615818e-01, inf, 8.9314e-01, 3.8772e-01, 
 2DIAGNOSTIC,     2, -2.038785815239e-01, inf, 9.0284e-01, 9.7020e-03, 
 2DIAGNOSTIC,     3, -2.082372456789e-01, inf, 9.1508e-01, 1.2235e-02, 
 2DIAGNOSTIC,     4, -2.098534107208e-01, inf, 9.2975e-01, 1.4672e-02, 
 2DIAGNOSTIC,     5, -2.092169821262e-01, inf, 9.3944e-01, 9.6889e-03, 
 2DIAGNOSTIC,     6, -2.092839926481e-01, inf, 9.4843e-01, 8.9910e-03, 
 2DIAGNOSTIC,     7, -2.093574851751e-01, inf, 9.5867e-01, 1.0239e-02, 
 2DIAGNOSTIC,     8, -2.094518393278e-01, inf, 9.6901e-01, 1.0344e-02, 
 2DIAGNOSTIC,     9, -2.096032351255e-01, inf, 9.7869e-01, 9.6750e-03, 
 2DIAGNOSTIC,    10, -2.098295986652e-01, 2.420092932880e-03, 9.8824e-01, 9.5479e-03, 
 2DIAGNOSTIC,    11, -2.109578400850e-01, 1.048594247550e-03, 9.9945e-01, 1.1209e-02, 
 2DIAGNOSTIC,    12, -2.114620655775e-01, 5.468052113429e-04, 1.0104e+00, 1.0948e-02, 
 2DIAGNOSTIC,    13, -2.302468717098e-01, 2.478283829987e-03, 1.0213e+00, 1.0861e-02, 
 2DIAGNOSTIC,    14, -2.592063844204e-01, 6.708825007081e-03, 1.0315e+00, 1.0294e-02, 
 2DIAGNOSTIC,    15, -4.158731400967e-01, 2.219148539007e-02, 1.0459e+00, 1.4327e-02, 
 2DIAGNOSTIC,    16, -4.519674777985e-01, 3.444769605994e-02, 1.0726e+00, 2.6698e-02, 
 2DIAGNOSTIC,    17, -4.515510499477e-01, 4.118014499545e-02, 1.0902e+00, 1.7586e-02, 
 2DIAGNOSTIC,    18, -4.563592970371e-01, 4.339300468564e-02, 1.1035e+00, 1.3347e-02, 
 2DIAGNOSTIC,    19, -4.640538394451e-01, 4.167402163148e-02, 1.1246e+00, 2.1077e-02, 
 2DIAGNOSTIC,    20, -4.671892821789e-01, 3.650068119168e-02, 1.1519e+00, 2.7307e-02, 
 2DIAGNOSTIC,    21, -4.661404192448e-01, 2.880102023482e-02, 1.1630e+00, 1.1124e-02, 
 2DIAGNOSTIC,    22, -4.651426076889e-01, 1.965084299445e-02, 1.1729e+00, 9.8999e-03, 
 2DIAGNOSTIC,    23, -4.646096825600e-01, 1.070170570165e-02, 1.1903e+00, 1.7342e-02, 
 2DIAGNOSTIC,    24, -4.618665277958e-01, 2.698570722714e-03, 1.2029e+00, 1.2645e-02, 
 2DIAGNOSTIC,    25, -4.622705578804e-01, 9.039916913025e-04, 1.2162e+00, 1.3273e-02, 
 2DIAGNOSTIC,    26, -4.596944153309e-01, 3.505711501930e-04, 1.2269e+00, 1.0754e-02, 
DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -2.246792763472e-01, inf, 2.0018e+00, 7.7484e-01, 
 2DIAGNOSTIC,     2, -2.265677750111e-01, inf, 2.0860e+00, 8.4223e-02, 
 2DIAGNOSTIC,     3, -2.299164384604e-01, inf, 2.2284e+00, 1.4240e-01, 
 2DIAGNOSTIC,     4, -2.308408319950e-01, inf, 2.3865e+00, 1.5807e-01, 
 2DIAGNOSTIC,     5, -2.312635928392e-01, inf, 2.4756e+00, 8.9105e-02, 
 2DIAGNOSTIC,     6, -2.312611639500e-01, inf, 2.5785e+00, 1.0295e-01, 
 2DIAGNOSTIC,     7, -2.341087907553e-01, inf, 2.6423e+00, 6.3783e-02, 
 2DIAGNOSTIC,     8, -2.398036420345e-01, inf, 2.7076e+00, 6.5256e-02, 
 2DIAGNOSTIC,     9, -2.440513074398e-01, inf, 2.7822e+00, 7.4664e-02, 
 2DIAGNOSTIC,    10, -2.478411644697e-01, 5.699011031538e-03, 2.8880e+00, 1.0581e-01, 
 2DIAGNOSTIC,    11, -2.512746155262e-01, 5.935627501458e-03, 2.9542e+00, 6.6177e-02, 
 2DIAGNOSTIC,    12, -2.516517937183e-01, 5.814067088068e-03, 3.0254e+00, 7.1177e-02, 
 2DIAGNOSTIC,    13, -2.550647556782e-01, 5.799821577966e-03, 3.1367e+00, 1.1136e-01, 
 2DIAGNOSTIC,    14, -2.604094147682e-01, 5.776579026133e-03, 3.2699e+00, 1.3312e-01, 
 2DIAGNOSTIC,    15, -2.681150138378e-01, 5.852766800672e-03, 3.3889e+00, 1.1902e-01, 
 2DIAGNOSTIC,    16, -2.730991840363e-01, 5.733166821301e-03, 3.5432e+00, 1.5429e-01, 
 2DIAGNOSTIC,    17, -2.751065790653e-01, 5.430300254375e-03, 3.7808e+00, 2.3763e-01, 
 2DIAGNOSTIC,    18, -2.758890390396e-01, 5.081369541585e-03, 3.9309e+00, 1.5015e-01, 
 2DIAGNOSTIC,    19, -2.781376838684e-01, 4.687073174864e-03, 4.0884e+00, 1.5749e-01, 
 2DIAGNOSTIC,    20, -2.784049510956e-01, 4.120802972466e-03, 4.2975e+00, 2.0905e-01, 
 2DIAGNOSTIC,    21, -2.783043980598e-01, 3.413331229240e-03, 4.4642e+00, 1.6675e-01, 
 2DIAGNOSTIC,    22, -2.784256637096e-01, 2.489075297490e-03, 4.6303e+00, 1.6605e-01, 
 2DIAGNOSTIC,    23, -2.786628901958e-01, 1.598265487701e-03, 4.7543e+00, 1.2403e-01, 
 2DIAGNOSTIC,    24, -2.786287069321e-01, 8.778233896010e-04, 4.8705e+00, 1.1613e-01, 
 2DIAGNOSTIC,    25, -2.792650163174e-01, 5.034991772845e-04, 4.9802e+00, 1.0974e-01, 
 2DIAGNOSTIC,    26, -2.794051170349e-01, 3.303182893433e-04, 5.1232e+00, 1.4296e-01, 
 2DIAGNOSTIC,    27, -2.800528109074e-01, 2.489477046765e-04, 5.2657e+00, 1.4256e-01, 
 2DIAGNOSTIC,    28, -2.812207043171e-01, 2.242111222586e-04, 5.4034e+00, 1.3765e-01, 
 2DIAGNOSTIC,    29, -2.883085608482e-01, 5.313102738000e-04, 5.5466e+00, 1.4324e-01, 
 2DIAGNOSTIC,    30, -3.263931274414e-01, 2.142946235836e-03, 5.6964e+00, 1.4982e-01, 
 2DIAGNOSTIC,    31, -3.588635325432e-01, 4.496813286096e-03, 5.8470e+00, 1.5059e-01, 
 2DIAGNOSTIC,    32, -3.609545826912e-01, 6.291938479990e-03, 5.9916e+00, 1.4460e-01, 
 2DIAGNOSTIC,    33, -3.624725043774e-01, 7.435208186507e-03, 6.1483e+00, 1.5673e-01, 
 2DIAGNOSTIC,    34, -3.632150590420e-01, 7.818832993507e-03, 6.3314e+00, 1.8303e-01, 
 2DIAGNOSTIC,    35, -3.628732860088e-01, 7.424924522638e-03, 6.5264e+00, 1.9497e-01, 
 2DIAGNOSTIC,    36, -3.630237281322e-01, 6.352366879582e-03, 6.6255e+00, 9.9155e-02, 
 2DIAGNOSTIC,    37, -3.626292943954e-01, 4.776376299560e-03, 6.7859e+00, 1.6039e-01, 
 2DIAGNOSTIC,    38, -3.626817762852e-01, 2.907587680966e-03, 6.9272e+00, 1.4130e-01, 
 2DIAGNOSTIC,    39, -3.628051280975e-01, 1.052518957295e-03, 7.0706e+00, 1.4336e-01, 
 2DIAGNOSTIC,    40, -3.628135621548e-01, 1.363196206512e-04, 7.2346e+00, 1.6400e-01, 
 2DIAGNOSTIC,    41, -3.631153106689e-01, 4.936433469993e-05, 7.3547e+00, 1.2013e-01, 
 2DIAGNOSTIC,    42, -3.632476031780e-01, 1.381567381031e-05, 7.5110e+00, 1.5635e-01, 
 2DIAGNOSTIC,    43, -3.634126484394e-01, 1.664054798312e-05, 7.6457e+00, 1.3465e-01, 
 2DIAGNOSTIC,    44, -3.635294437408e-01, 3.680085137603e-05, 7.7730e+00, 1.2735e-01, 
 2DIAGNOSTIC,    45, -3.649683594704e-01, 7.569058652734e-05, 7.9067e+00, 1.3365e-01, 
 2DIAGNOSTIC,    46, -3.685500323772e-01, 1.823718484957e-04, 8.0647e+00, 1.5797e-01, 
 2DIAGNOSTIC,    47, -3.666216433048e-01, 2.173879765905e-04, 8.3169e+00, 2.5227e-01, 
 2DIAGNOSTIC,    48, -3.665351569653e-01, 2.316666650586e-04, 8.4480e+00, 1.3105e-01, 
 2DIAGNOSTIC,    49, -3.668815493584e-01, 2.329289709451e-04, 8.6143e+00, 1.6628e-01, 
 2DIAGNOSTIC,    50, -3.668392896652e-01, 2.097437536577e-04, 8.7832e+00, 1.6888e-01, 
DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -2.300854623318e-01, inf, 1.3186e+01, 4.4026e+00, 
 2DIAGNOSTIC,     2, -2.309809774160e-01, inf, 1.3929e+01, 7.4313e-01, 
 2DIAGNOSTIC,     3, -2.310343682766e-01, inf, 1.5035e+01, 1.1063e+00, 
 2DIAGNOSTIC,     4, -2.310280203819e-01, inf, 1.5875e+01, 8.3986e-01, 
 2DIAGNOSTIC,     5, -2.310078442097e-01, inf, 1.6594e+01, 7.1930e-01, 
 2DIAGNOSTIC,     6, -2.311059236526e-01, inf, 1.7435e+01, 8.4024e-01, 
 2DIAGNOSTIC,     7, -2.313560843468e-01, inf, 1.9000e+01, 1.5652e+00, 
 2DIAGNOSTIC,     8, -2.313769906759e-01, inf, 1.9936e+01, 9.3588e-01, 
 2DIAGNOSTIC,     9, -2.313937097788e-01, inf, 2.1049e+01, 1.1131e+00, 
 2DIAGNOSTIC,    10, -2.313913702965e-01, 2.585652691778e-04, 2.2041e+01, 9.9268e-01, 
  Elapsed time (stage 0): 2.2613e+01


Stage 1
  iterations = 100x100x50x10
  convergence threshold = 1.0000e-08
  convergence window size = 10
  number of levels = 4
  using the Mattes MI metric (number of bins = 32, weight = 1.0000e+00)
  preprocessing:  winsorizing the image intensities
  preprocessing:  histogram matching the images
  Shrink factors (level 1 out of 4): [8, 8, 8]
  Shrink factors (level 2 out of 4): [4, 4, 4]
  Shrink factors (level 3 out of 4): [2, 2, 2]
  Shrink factors (level 4 out of 4): [1, 1, 1]
  smoothing sigmas per level: [4, 2, 1, 0]
  regular sampling (percentage = 2.5000e-01)

*** Running AffineTransform registration ***

DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -8.516496419907e-01, inf, 4.6757e-01, 4.6757e-01, 
 2DIAGNOSTIC,     2, -8.619522452354e-01, inf, 4.7086e-01, 3.2902e-03, 
 2DIAGNOSTIC,     3, -8.714879155159e-01, inf, 4.7336e-01, 2.4981e-03, 
 2DIAGNOSTIC,     4, -8.673114776611e-01, inf, 4.7638e-01, 3.0220e-03, 
 2DIAGNOSTIC,     5, -8.766898512840e-01, inf, 4.7896e-01, 2.5802e-03, 
 2DIAGNOSTIC,     6, -8.666661977768e-01, inf, 4.8220e-01, 3.2430e-03, 
 2DIAGNOSTIC,     7, -8.670663237572e-01, inf, 4.8492e-01, 2.7170e-03, 
 2DIAGNOSTIC,     8, -8.665117621422e-01, inf, 4.8733e-01, 2.4052e-03, 
 2DIAGNOSTIC,     9, -8.817371129990e-01, inf, 4.9004e-01, 2.7151e-03, 
 2DIAGNOSTIC,    10, -8.880684375763e-01, 1.585583668202e-03, 4.9367e-01, 3.6340e-03, 
 2DIAGNOSTIC,    11, -8.929659724236e-01, 1.512357033789e-03, 4.9694e-01, 3.2611e-03, 
 2DIAGNOSTIC,    12, -8.811549544334e-01, 1.278360374272e-03, 4.9995e-01, 3.0160e-03, 
 2DIAGNOSTIC,    13, -9.082580208778e-01, 1.891150604934e-03, 5.0303e-01, 3.0739e-03, 
 2DIAGNOSTIC,    14, -9.976354241371e-01, 4.147691652179e-03, 5.0790e-01, 4.8759e-03, 
 2DIAGNOSTIC,    15, -9.977395534515e-01, 5.844525061548e-03, 5.1160e-01, 3.7010e-03, 
 2DIAGNOSTIC,    16, -1.001670479774e+00, 6.685001309961e-03, 5.1512e-01, 3.5200e-03, 
 2DIAGNOSTIC,    17, -9.995734095573e-01, 6.806376855820e-03, 5.1839e-01, 3.2721e-03, 
 2DIAGNOSTIC,    18, -1.007728695869e+00, 6.400717422366e-03, 5.2159e-01, 3.1960e-03, 
 2DIAGNOSTIC,    19, -1.004605293274e+00, 5.616558250040e-03, 5.2644e-01, 4.8480e-03, 
 2DIAGNOSTIC,    20, -1.015973210335e+00, 4.668783862144e-03, 5.2981e-01, 3.3751e-03, 
 2DIAGNOSTIC,    21, -1.023845911026e+00, 3.599789692089e-03, 5.3463e-01, 4.8170e-03, 
 2DIAGNOSTIC,    22, -1.026815414429e+00, 2.182431751862e-03, 5.3852e-01, 3.8941e-03, 
 2DIAGNOSTIC,    23, -1.019067049026e+00, 9.217898477800e-04, 5.4235e-01, 3.8300e-03, 
 2DIAGNOSTIC,    24, -1.019464135170e+00, 8.283834322356e-04, 5.4569e-01, 3.3319e-03, 
 2DIAGNOSTIC,    25, -1.020286798477e+00, 6.735986680724e-04, 5.4910e-01, 3.4170e-03, 
 2DIAGNOSTIC,    26, -1.029448628426e+00, 6.174931186251e-04, 5.5311e-01, 4.0061e-03, 
 2DIAGNOSTIC,    27, -1.021082878113e+00, 3.876706177834e-04, 5.5649e-01, 3.3789e-03, 
 2DIAGNOSTIC,    28, -1.022149801254e+00, 2.466650330462e-04, 5.6049e-01, 4.0050e-03, 
 2DIAGNOSTIC,    29, -1.036401629448e+00, 2.059226098936e-04, 5.6478e-01, 4.2839e-03, 
 2DIAGNOSTIC,    30, -1.036670684814e+00, 2.553177764639e-04, 5.6818e-01, 3.4051e-03, 
 2DIAGNOSTIC,    31, -1.036940574646e+00, 3.540726611391e-04, 5.7208e-01, 3.8941e-03, 
 2DIAGNOSTIC,    32, -1.020771384239e+00, 2.961874124594e-04, 5.7579e-01, 3.7119e-03, 
 2DIAGNOSTIC,    33, -1.019435286522e+00, 1.379211462336e-04, 5.8182e-01, 6.0341e-03, 
DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -4.645992815495e-01, inf, 1.0401e+00, 4.5827e-01, 
 2DIAGNOSTIC,     2, -4.689598679543e-01, inf, 1.0517e+00, 1.1652e-02, 
 2DIAGNOSTIC,     3, -4.761729538441e-01, inf, 1.0638e+00, 1.2050e-02, 
 2DIAGNOSTIC,     4, -5.119118690491e-01, inf, 1.0764e+00, 1.2562e-02, 
 2DIAGNOSTIC,     5, -5.669302344322e-01, inf, 1.0888e+00, 1.2420e-02, 
 2DIAGNOSTIC,     6, -5.987234711647e-01, inf, 1.1055e+00, 1.6690e-02, 
 2DIAGNOSTIC,     7, -6.168583631516e-01, inf, 1.1245e+00, 1.9064e-02, 
 2DIAGNOSTIC,     8, -6.184177398682e-01, inf, 1.1418e+00, 1.7306e-02, 
 2DIAGNOSTIC,     9, -6.190854310989e-01, inf, 1.1568e+00, 1.5017e-02, 
 2DIAGNOSTIC,    10, -6.173093914986e-01, 2.239562198520e-02, 1.1795e+00, 2.2685e-02, 
 2DIAGNOSTIC,    11, -6.168905496597e-01, 1.719184964895e-02, 1.1987e+00, 1.9193e-02, 
 2DIAGNOSTIC,    12, -6.181570291519e-01, 1.166682690382e-02, 1.2177e+00, 1.9018e-02, 
 2DIAGNOSTIC,    13, -6.180609464645e-01, 6.290171295404e-03, 1.2371e+00, 1.9388e-02, 
 2DIAGNOSTIC,    14, -6.208385229111e-01, 2.504052594304e-03, 1.2567e+00, 1.9590e-02, 
 2DIAGNOSTIC,    15, -6.219291687012e-01, 8.537448593415e-04, 1.2732e+00, 1.6457e-02, 
 2DIAGNOSTIC,    16, -6.222257614136e-01, 3.154027799610e-04, 1.2956e+00, 2.2417e-02, 
 2DIAGNOSTIC,    17, -6.240010857582e-01, 3.865649923682e-04, 1.3147e+00, 1.9116e-02, 
 2DIAGNOSTIC,    18, -6.233869791031e-01, 4.370127862785e-04, 1.3342e+00, 1.9523e-02, 
 2DIAGNOSTIC,    19, -6.217851042747e-01, 4.194045031909e-04, 1.3540e+00, 1.9792e-02, 
 2DIAGNOSTIC,    20, -6.216439008713e-01, 3.201896615792e-04, 1.3737e+00, 1.9624e-02, 
 2DIAGNOSTIC,    21, -6.211703419685e-01, 1.801129983505e-04, 1.3940e+00, 2.0299e-02, 
 2DIAGNOSTIC,    22, -6.209641695023e-01, 6.018896237947e-05, 1.4143e+00, 2.0383e-02, 
DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -3.732984662056e-01, inf, 2.3442e+00, 9.2990e-01, 
 2DIAGNOSTIC,     2, -3.747747242451e-01, inf, 2.5283e+00, 1.8407e-01, 
 2DIAGNOSTIC,     3, -3.753629028797e-01, inf, 2.6476e+00, 1.1934e-01, 
 2DIAGNOSTIC,     4, -3.764544725418e-01, inf, 2.7751e+00, 1.2749e-01, 
 2DIAGNOSTIC,     5, -3.781240284443e-01, inf, 2.9040e+00, 1.2888e-01, 
 2DIAGNOSTIC,     6, -3.780674040318e-01, inf, 3.0520e+00, 1.4802e-01, 
 2DIAGNOSTIC,     7, -3.774773478508e-01, inf, 3.2024e+00, 1.5033e-01, 
 2DIAGNOSTIC,     8, -3.780653774738e-01, inf, 3.3370e+00, 1.3466e-01, 
 2DIAGNOSTIC,     9, -3.776527941227e-01, inf, 3.4921e+00, 1.5503e-01, 
 2DIAGNOSTIC,    10, -3.779987394810e-01, 7.259395206347e-04, 3.6591e+00, 1.6707e-01, 
 2DIAGNOSTIC,    11, -3.780974149704e-01, 4.376969009172e-04, 3.8223e+00, 1.6318e-01, 
 2DIAGNOSTIC,    12, -3.779618144035e-01, 2.445462159812e-04, 3.9447e+00, 1.2242e-01, 
 2DIAGNOSTIC,    13, -3.780260682106e-01, 9.674327884568e-05, 4.0900e+00, 1.4531e-01, 
 2DIAGNOSTIC,    14, -3.783870041370e-01, 3.668760473374e-05, 4.2755e+00, 1.8550e-01, 
 2DIAGNOSTIC,    15, -3.782667815685e-01, 5.873046029592e-05, 4.4310e+00, 1.5552e-01, 
 2DIAGNOSTIC,    16, -3.783953487873e-01, 7.732041558484e-05, 4.5726e+00, 1.4152e-01, 
 2DIAGNOSTIC,    17, -3.782450854778e-01, 5.337522088666e-05, 4.7026e+00, 1.3007e-01, 
 2DIAGNOSTIC,    18, -3.782639801502e-01, 5.355153552955e-05, 4.8109e+00, 1.0827e-01, 
 2DIAGNOSTIC,    19, -3.783040046692e-01, 3.346923767822e-05, 4.9682e+00, 1.5730e-01, 
 2DIAGNOSTIC,    20, -3.785694837570e-01, 3.521345206536e-05, 5.0746e+00, 1.0642e-01, 
 2DIAGNOSTIC,    21, -3.784730136395e-01, 3.383246439626e-05, 5.1811e+00, 1.0645e-01, 
 2DIAGNOSTIC,    22, -3.786329030991e-01, 3.070331149502e-05, 5.3166e+00, 1.3550e-01, 
 2DIAGNOSTIC,    23, -3.787611722946e-01, 3.104894130956e-05, 5.4734e+00, 1.5681e-01, 
 2DIAGNOSTIC,    24, -3.787444829941e-01, 3.930047023459e-05, 5.5807e+00, 1.0732e-01, 
 2DIAGNOSTIC,    25, -3.788053691387e-01, 4.139339944231e-05, 5.7483e+00, 1.6758e-01, 
 2DIAGNOSTIC,    26, -3.790629506111e-01, 5.087933095638e-05, 5.9096e+00, 1.6131e-01, 
 2DIAGNOSTIC,    27, -3.787120282650e-01, 4.087089837412e-05, 6.0430e+00, 1.3339e-01, 
 2DIAGNOSTIC,    28, -3.785792291164e-01, 2.509616933821e-05, 6.1771e+00, 1.3413e-01, 
 2DIAGNOSTIC,    29, -3.784386515617e-01, 5.467837581818e-06, 6.2813e+00, 1.0422e-01, 
DIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 2DIAGNOSTIC,     1, -2.298690974712e-01, inf, 1.0504e+01, 4.2228e+00, 
 2DIAGNOSTIC,     2, -2.299639731646e-01, inf, 1.1379e+01, 8.7535e-01, 
 2DIAGNOSTIC,     3, -2.300358712673e-01, inf, 1.2687e+01, 1.3077e+00, 
 2DIAGNOSTIC,     4, -2.300046235323e-01, inf, 1.3789e+01, 1.1021e+00, 
 2DIAGNOSTIC,     5, -2.299838811159e-01, inf, 1.4640e+01, 8.5094e-01, 
 2DIAGNOSTIC,     6, -2.299745976925e-01, inf, 1.5381e+01, 7.4101e-01, 
 2DIAGNOSTIC,     7, -2.299658507109e-01, inf, 1.6263e+01, 8.8167e-01, 
 2DIAGNOSTIC,     8, -2.299657166004e-01, inf, 1.7161e+01, 8.9812e-01, 
 2DIAGNOSTIC,     9, -2.299694418907e-01, inf, 1.8112e+01, 9.5068e-01, 
 2DIAGNOSTIC,    10, -2.299374043941e-01, 3.698454747791e-06, 1.8869e+01, 7.5722e-01, 
  Elapsed time (stage 1): 1.9669e+01


Stage 2
  iterations = 5x0
  convergence threshold = 1.0000e-09
  convergence window size = 15
  number of levels = 2
  using the CC metric (radius = 4, weight = 5.0000e-01)
  preprocessing:  winsorizing the image intensities
  preprocessing:  histogram matching the images
  using the CC metric (radius = 4, weight = 5.0000e-01)
  preprocessing:  winsorizing the image intensities
  preprocessing:  histogram matching the images
  Shrink factors (level 1 out of 2): [2, 2, 2]
  Shrink factors (level 2 out of 2): [1, 1, 1]
  smoothing sigmas per level: [1, 0]
  Using default NONE metricSamplingStrategy 

*** Running SyN registration (varianceForUpdateField = 3.0000e+00, varianceForTotalField = 0.0000e+00) ***

XXDIAGNOSTIC,Iteration,metricValue,convergenceValue,ITERATION_TIME_INDEX,SINCE_LAST
 1DIAGNOSTIC,     1, -9.280031919479e-01, inf, 5.6777e+01, 5.6777e+01, 
 1DIAGNOSTIC,     2, -9.283123612404e-01, inf, 1.3066e+02, 7.3880e+01, 
 1DIAGNOSTIC,     3, -9.286091327667e-01, inf, 1.9817e+02, 6.7512e+01, 
 1DIAGNOSTIC,     4, -9.289255738258e-01, inf, 2.7328e+02, 7.5113e+01, 
 1DIAGNOSTIC,     5, -9.292569756508e-01, inf, 3.3366e+02, 6.0374e+01, 
  Elapsed time (stage 2): 341.5


Total elapsed time: 383.9


Terminal - standard error
~~~~~~~~~~~~~~~~~~~~~~~~~


  file NULL does not exist . 
 file NULL does not exist . 
 file NULL does not exist . 


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
* NSLOTS : 8
* OMP_NUM_THREADS : 1
* OS : Linux
* PATH : /usr/local/miniconda/bin:/opt/ICA-AROMA:/usr/lib/ants:/usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* PERL5LIB : /opt/freesurfer/mni/lib/perl5/5.8.5
* POSSUMDIR : /usr/share/fsl/5.0
* PYTHONNOUSERSITE : 1
* PYTHONWARNINGS : ignore
* SUBJECTS_DIR : /opt/freesurfer/subjects

