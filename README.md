# data_multisession_testing
Light-weighted data for our integrated multi-session testings

# Content
* sub-ms01: BIDS folder with multiple contrast (T1w/MPRAGE, T2w, FLAIR). Original image and derivatives (see below) are the first 3 subjects from post processed data from lesion challenge 2015. 
* `derivatives/labels/sub-ms01`: derivatives folder with the following labels:
  * `_seg-manual`: spinal cord segmentations for all contrasts,
  * `_lesion-manual`: dummy labels which are supposed to represent lesion segmentation. WARNING: these are *not* actual lesion segmentations, but are only here for the purpose of testing the workflow of `ivadomed` codebase.
  * `_labels-disc-manual`: dummy label (single voxel), which is supposed to represent disc label. WARNING: this is *not* an actual label that represent the anatomy, but is only here for the purpose of testing the workflow of `ivadomed` codebase.
* bounding\_box.json: dictionary to test a specific function from `ivadomed/scripts/bounding_box.py`.
* dataset\_description.json: this file is needed to described the dataset.
* participants.csv: table with subject name and potential metadata.
* temporary\_results.csv: Used to test `ivadomed/scripts/compare_models.py`.

* sub-unf02/sub-unf03: copies of sub-unf01
