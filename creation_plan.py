import pytest
from typing import List

from create_derivatives import CreateBIDSDerivatives
from create_subjects import CreateBIDSSubjects


def test_create_bids_projects_1():
    """
    Nothing strange, subjects, sessions, plans.
    :return:
    """
    path_mock_data = r"C:\Temp\Test\\"
    list_subjects = [5]
    list_subject_sessions = [4, 6, 5]

    # This must be in the order of appending
    # MUST have bids_details keyword
    list_subject_specific_bids_dict = [
        {
            "acq": ["MTon", "MToff", "T1w"],  # Acquisition
            "MODALITY": ["MTS"],  # Modality
        },
        {
            "flip": [1, 2],  # Flip angle
            "mt": ["on", "off"],  # MT
            "MODALITY": ["MTS"],  # Modality
        },
        {
            "flip": [2],  # Flip angle
            "mt": ["off"],  # MT
            "MODALITY": ["MTS"],  # Modality
        }
    ]

    # Create the subjects
    for index, subject in enumerate(list_subjects):
        bids_subject = CreateBIDSSubjects(
            process_id=index,
            index_subject=subject,
            path_to_mock_data=path_mock_data,
            list_sessions=list_subject_sessions,
            list_bids_details=list_subject_specific_bids_dict,

        )
        bids_subject.run()

    list_derivatives_subjects = [9, 10]
    list_derivatives_subject_sessions = [5, 4]
    list_subject_specific_bids_dict = [
        {
            "flip": [1, 2],  # Flip angle
            "mt": ["on", "off"],  # MT
            "MODALITY": ["MTS"],  # Modality
        },
    ]
    list_derivatives_subject_labels = ["lesion-manual-rater1", "lesion-manual-rater2"]

    # Create the derivatives
    for index, subject in enumerate(list_derivatives_subjects):
        bids_derivative = CreateBIDSDerivatives(
            process_id=index,
            index_subject=subject,
            path_to_mock_data=path_mock_data,
            list_sessions=list_derivatives_subject_sessions,
            list_bids_details=list_subject_specific_bids_dict,
            list_labels=list_derivatives_subject_labels,
        )
        bids_derivative.run()
