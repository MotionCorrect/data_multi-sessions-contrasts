# data_multisession_testing
Light-weight real data for our integrated multi-session testings

# Data Source
* Derived partially from publicly available at https://smart-stats-tools.org/lesion-challenge-2015, 
* Nii file source here: https://smart-stats-tools.org/sites/default/files/lesion_challenge/training_final_v4.zip
* Description and acquisition protocol here: https://smart-stats-tools.org/sites/default/files/lesion_challenge/Training_data_description.pdf

# Content
* `sub-ms01`: BIDS folder with multiple contrast (T1w/MPRAGE, T2w, FLAIR). Original image and derivatives (see below) are the first subject from post processed data from MS lesion challenge 2015.
   * 4 Sessions 
* `sub-ms02`: BIDS folder with multiple contrast (T1w/MPRAGE, T2w, FLAIR). Original image and derivatives (see below) are the second subject from post processed data from MS lesion challenge 2015.
   * 4 Sessions
* `sub-ms03`: BIDS folder with multiple contrast (T1w/MPRAGE, T2w, FLAIR). Original image and derivatives (see below) are the third subject from post processed data from MS lesion challenge 2015.
   * 5 Sessions
* `derivatives/labels/sub-ms01/ses-01`: derivatives folder with the following labels (using sub-ms01/ses-01 as example): 
  * `_lesion-manual-rater1.nii`: dummy labels which are supposed to represent lesion segmentation. WARNING: these are *not* actual lesion segmentations, but are only here for the purpose of testing the workflow of `ivadomed` codebase.
  * `_lesion-manual-rater2.nii`: dummy labels which are supposed to represent lesion segmentation. WARNING: these are *not* actual lesion segmentations, but are only here for the purpose of testing the workflow of `ivadomed` codebase.
