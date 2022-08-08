from typing import List

from create_derivatives import CreateBIDSDerivatives
from create_subjects import CreateBIDSSubjects


def test_create_bids_projects_1():
    """
    Nothing strange, subjects, sessisons, plans.
    :return:
    """
    path_mock_data = r"C:\Temp\Test\\"
    list_subjects = [7, 8, 9]
    list_subject_sessions = [4, 6, 5]
    list_subject_modalities = ["T1w", "T2w"]

    # Create the subjects
    for index, subject in enumerate(list_subjects):
        bids_subject = CreateBIDSSubjects(
            process_id=index,
            index_subject=subject,
            path_to_mock_data=path_mock_data,
            list_sessions=list_subject_sessions,
            list_anatomy_modalities=list_subject_modalities,
        )
        bids_subject.run()

    list_derivatives_subjects = [7, 8]
    list_derivatives_subject_sessions = [5]
    list_derivatives_subject_modalities = ["T2w"]
    list_derivatives_subject_labels = ["lesion-manual-rater1", "lesion-manual-rater2"]

    # Create the derivatives
    for index, subject in enumerate(list_derivatives_subjects):
        bids_derivative = CreateBIDSDerivatives(
            process_id=index,
            index_subject=subject,
            path_to_mock_data=path_mock_data,
            list_sessions=list_derivatives_subject_sessions,
            list_anatomy_modalities=list_derivatives_subject_modalities,
            list_labels=list_derivatives_subject_labels,
        )
        bids_derivative.run()
