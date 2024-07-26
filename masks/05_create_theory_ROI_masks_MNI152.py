#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combines several masks into theory specific ROIs.

@author: Yamil Vidal
Email: hvidaldossantos@gmail.com
Created on Fri Jul  8 17:19:11 2022
"""

import sys
import numpy as np

projectRoot = '/mnt/beegfs/XNAT/COGITATE/fMRI/phase_2/processed'

bids_dir = projectRoot + '/bids'  
code_dir = projectRoot + '/bids/code' 
data_dir = projectRoot + '/bids/derivatives/fslFeat'

f_name_pattern = '/ICBM2009c_asym_nlin_bh_%(roi)s_space-%(space)s.nii.gz'
mask_dir = bids_dir + '/derivatives/masks/ICBM2009c_asym_nlin'

subject_list_type = 'phase3_V1_subset'
group_mask = data_dir + '/group/ses-V1/' + subject_list_type + '/ses-V1_task-Dur_analysis-3rdGLM_space-MNI152NLin2009cAsym_desc-cope15.gfeat/cope1.feat/mask.nii.gz'
#group_mask = bids_dir + '/MNI152NLin2009cAsym_res-01_desc-brain_mask.nii.gz'

# load helper functions / code dir
sys.path.append(code_dir)
from helper_functions_MRI import load_mri, save_mri

space = 'MNI152NLin2009cAsym'

# %%

roi_list = ['G_and_S_cingul-Ant',
             'G_and_S_cingul-Mid-Ant',
             'G_and_S_cingul-Mid-Post',
             'G_and_S_occipital_inf',
             'G_cuneus',
             'G_front_inf-Opercular',
             'G_front_inf-Orbital',
             'G_front_inf-Triangul',
             'G_front_middle',
             'G_oc-temp_lat-fusifor',
             'G_oc-temp_med-Lingual',
             'G_oc-temp_med-Parahip',
             'G_occipital_middle',
             'G_occipital_sup',
             'G_orbital',
             'G_pariet_inf-Angular',
             'G_pariet_inf-Supramar',
             'G_precentral',
             'G_temp_sup-Lateral',
             'G_temp_sup-Plan_tempo',
             'G_temporal_inf',
             'G_temporal_middle',
             'Lat_Fis-ant-Horizont',
             'Lat_Fis-ant-Vertical',
             'Pole_occipital',
             'Pole_temporal',
             'S_calcarine',
             'S_front_inf',
             'S_front_middle',
             'S_front_sup',
             'S_interm_prim-Jensen',
             'S_intrapariet_and_P_trans',
             'S_oc-temp_lat',
             'S_oc_middle_and_Lunatus',
             'S_oc_sup_and_transversal',
             'S_occipital_ant',
             'S_precentral-inf-part',
             'S_temporal_inf',
             'S_temporal_sup',
             'G_and_S_frontomargin',
             'G_and_S_transv_frontopol',
             'G_front_sup',
             'G_rectus',
             'G_subcallosal',
             'S_orbital_lateral',
             'S_orbital_med-olfact',
             'S_orbital-H_Shaped',
             'S_suborbital']

# Theory's lists of ROIs
GNW_roi_list = ['G_and_S_cingul-Ant',
                'G_and_S_cingul-Mid-Ant',
                'G_and_S_cingul-Mid-Post',
                'G_front_inf-Opercular',
                'G_front_inf-Orbital',
                'G_front_inf-Triangul',
                'G_front_middle',
                'Lat_Fis-ant-Horizont',
                'Lat_Fis-ant-Vertical',
                'S_front_inf',
                'S_front_middle',
                'S_front_sup']

IIT_roi_list = ['G_and_S_occipital_inf',
                'G_cuneus',
                'G_occipital_middle',
                'G_occipital_sup',
                'G_oc-temp_lat-fusifor',
                'G_oc-temp_med-Lingual',
                'G_oc-temp_med-Parahip',
                'G_temporal_inf',
                'Pole_occipital',
                'Pole_temporal',
                'S_calcarine',
                'S_intrapariet_and_P_trans',
                'S_oc_middle_and_Lunatus',
                'S_oc_sup_and_transversal',
                'S_temporal_sup']

IIT_extended_roi_list = ['G_and_S_occipital_inf',
                        'G_cuneus',
                        'G_occipital_middle',
                        'G_occipital_sup',
                        'G_oc-temp_lat-fusifor',
                        'G_oc-temp_med-Lingual',
                        'G_oc-temp_med-Parahip',
                        'G_orbital',
                        'G_pariet_inf-Angular',
                        'G_pariet_inf-Supramar',
                        'G_precentral',
                        'G_temp_sup-Lateral',
                        'G_temp_sup-Plan_tempo',
                        'G_temporal_inf',
                        'G_temporal_middle',
                        'Pole_occipital',
                        'Pole_temporal',
                        'S_calcarine',
                        'S_front_inf',
                        'S_interm_prim-Jensen',
                        'S_intrapariet_and_P_trans',
                        'S_oc_middle_and_Lunatus',
                        'S_oc_sup_and_transversal',
                        'S_occipital_ant',
                        'S_oc-temp_lat',
                        'S_precentral-inf-part',
                        'S_temporal_inf',
                        'S_temporal_sup']

IIT_excluded_roi_list = ['G_and_S_frontomargin',
             'G_and_S_transv_frontopol',
             'G_front_sup',
             'G_rectus',
             'G_subcallosal',
             'S_orbital_lateral',
             'S_orbital_med-olfact',
             'S_orbital-H_Shaped',
             'S_suborbital']

# Seed generation ROI list
FFA_roi_list = ['G_and_S_occipital_inf',
                'G_oc-temp_lat-fusifor']

LOC_roi_list = ['G_occipital_middle',
                'S_oc_middle_and_Lunatus']

# Should only bilateral masks be processed? these are assumed to be label with 
# a 'bh' (both hemispheres) in the file name (as created by 01_create_ROI_masks.py)
process_only_bilateral_masks = True

# %%

# load all anatomical ROIs
def get_mask_list(sub_mask_dir):
    """
    Get list of paths to all masks for current subject. Prints how many masks
    are found or prints warning (not an error) if none have been found.
    sub_mask_dir: path to mask dir
    Returns: list of paths to all masks
    """
    from glob import glob
    if process_only_bilateral_masks:
        mask_list = glob(sub_mask_dir + '/*_bh_*' + space + '.nii.gz')
        n_masks = len(mask_list)
        print('. Getting list of bilateral masks only. Found ' + str(n_masks) + ' masks')
    else:
        mask_list = glob(sub_mask_dir + '/*.nii.gz')
        n_masks = len(mask_list)
        print('. Getting list of all masks. Found ' + str(n_masks) + ' masks')
    if not mask_list:
        print('! Warning no masks found for current subject !!!')
    return mask_list

def load_a_rois():
    """
    Load all anatomica ROIs of a subject into a dictionary
    
    sub_id: Subject ID
    Returns: Dictionary containing all the anatomical ROIs of the subject
    """

    mask_paths = get_mask_list(mask_dir)
    mask_paths.sort()
    
    sub_mask_list = [l[115:] for l in mask_paths]
    sub_mask_list = [l[:-33] for l in sub_mask_list]
    
    # empty dictionary that will contain all masks of a subject
    a_rois = {}
    
    for n in range(0,len(mask_paths)):
        mask = mask_paths[n]
        m = load_mri(mask, group_mask)
        a_rois[sub_mask_list[n]] = m
        
    return a_rois, sub_mask_list

def combine_rois(combine_roi_list,combine_roi_name):
    print(sub_id + ' ' + 'ROI: ' + combine_roi_name)
    combine_roi = np.array([a_rois[n] for n in combine_roi_list])
    combine_roi = np.sum(combine_roi,axis=0)
    
    f_name = f_name_pattern%{'roi':combine_roi_name,'space':space}
    full_f_name = mask_dir + f_name
    
    return combine_roi, full_f_name
    
# %%

sub_id = 'ICBM2009c_asym_nlin'

a_rois, sub_roi_list = load_a_rois()

# if 'GNW' in sub_roi_list: sub_roi_list.remove('GNW')
# if 'IIT' in sub_roi_list: sub_roi_list.remove('IIT')
# if 'IIT_extended' in sub_roi_list: sub_roi_list.remove('IIT_extended')

# assert sub_roi_list == roi_list, 'Subject''s ROI list doest not match the provided list'

# # GNW
GNW_roi, full_f_name = combine_rois(GNW_roi_list,'GNW')
save_mri(GNW_roi,group_mask,full_f_name)

# # IIT
IIT_roi, full_f_name = combine_rois(IIT_roi_list,'IIT')
save_mri(IIT_roi,group_mask,full_f_name)

# # IIT_extended
IIT_extended_roi, full_f_name = combine_rois(IIT_extended_roi_list,'IIT_extended')
save_mri(IIT_extended_roi,group_mask,full_f_name)

# # IIT_excluded
IIT_excluded_roi, full_f_name = combine_rois(IIT_excluded_roi_list,'IIT_excluded')
save_mri(IIT_excluded_roi,group_mask,full_f_name)

# FFA
FFA_roi, full_f_name = combine_rois(FFA_roi_list,'FFA')
save_mri(FFA_roi,group_mask,full_f_name)

# LOC
LOC_roi, full_f_name = combine_rois(LOC_roi_list,'LOC')
save_mri(LOC_roi,group_mask,full_f_name)
