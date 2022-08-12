import itertools
import json
from pathlib import Path
import multiprocessing
from typing import List

from nibabel import Nifti1Image

from create_common import CreateSubject
from nifti_mocker import (
    create_mock_nifti1_object,
    create_mock_nifti2_object,
    check_nifty_data,
    save_nifty_data,
)


class CreateBIDSDerivatives(CreateSubject):
    def __init__(
        self,
        process_id,
        index_subject,
        path_to_mock_data,
        list_sessions: list or None,
        list_bids_details,
        list_labels,
    ):
        """
        Constructor that focus on create all sessions/modalities for a given subject.
        :param process_id:
        :param index_subject:
        :param path_to_mock_data:
        :param list_sessions:
        :param list_bids_details:
        """
        super(CreateSubject, self).__init__()
        self.id = process_id
        self.index_subject = index_subject
        self.path_to_mock_data = Path(path_to_mock_data)
        self.list_sessions = list_sessions
        self.list_bids_details = list_bids_details
        self.list_labels = list_labels

    @staticmethod
    def default_constructor(path_to_mock_data):
        """
        Default constructor.
        :return:
        """
        id = 1
        index_subject = [1, 3, 4, 6]
        list_sessions = [2, 4, 6]
        list_modalities = ["T2w"]
        list_labels = ["lesion-manual-rater1", "lesion-manual-rater2"]
        CreateBIDSDerivatives(
            id,
            index_subject,
            path_to_mock_data,
            list_sessions,
            list_modalities,
            list_labels,
        )

    def run(self):
        """
        Main entry point of the multiprocess.
        :return:
        """

        # Create the sessions
        self.create_sessions(self.list_sessions, self.list_bids_details)

        # Save mock_json dictionary into a json file:
        mock_json: dict = self.generate_dataset_description_dict()

        path_json_file: Path = (
            self.path_to_mock_data / "derivatives" / "dataset_description.json"
        )
        with open(str(path_json_file), "w") as f:
            json.dump(mock_json, f, indent=4, sort_keys=True)

    def create_sessions(
        self, sessions: List[str] or None, list_bids_details: List[dict]
    ):
        """
        Within each session, create the expected nifti label files
        :param sessions:
        :param list_bids_details:
        :return:
        """
        if sessions:
            for session in sessions:
                self.create_session_specific_labels(session, list_bids_details)
        else:
            self.create_session_specific_labels(None, list_bids_details)

    def create_session_specific_labels(
        self, session: str or None, list_bids_details_in_lists: List[dict]
    ):
        """
        Create the expected nifti files for a given session.
        :param session:
        :param list_bids_details:
        :return:
        """
        # Take a single bids_deetail dict from the list.
        # This dictionary contain LISTS
        for a_bids_detail_dict in list_bids_details_in_lists:

            # Break down a single bids_detail_dictionary into concretized individual specific bids parameter pairs.
            # This is because bids_details could have list PER modalities.
            # e.g. acq = ["T1w", "T2w", "FLAIR", "PD"] needs to be broken down into FOR separate calls.
            # Source Inspiration: https://stackoverflow.com/a/61335465

            bids_standard_keys, bids_values = zip(*a_bids_detail_dict.items())

            list_permuted_dicts: List[dict] = [
                dict(zip(bids_standard_keys, a_set_of_permuted_values))
                for a_set_of_permuted_values in itertools.product(*bids_values)
            ]

            for a_permuted_bids_detail_dict in list_permuted_dicts:
                self.create_one_json_nii_pair(session, a_permuted_bids_detail_dict)

    def create_one_json_nii_pair(self, session: str or None, bids_detail: dict):
        """
        Create a nifti/JSON image pairs with an explicitly set list of session and model
        :param session:
        :param contrast:
        :param kwargs:
        :return:
        """
        file_stem: str = self.create_file_stem(session, bids_detail)

        self.generate_a_json_file(
            file_stem,
            session=session,
            bids_detail=bids_detail,
            modality_category="anat",
        )

        self.generate_a_nifti_label(
            file_stem, session=session, modality_category="anat"
        )

    def generate_a_json_file(
        self,
        file_stem: str,
        session: str or None,
        bids_detail: dict,
        modality_category: str = "anat",
    ):
        """
        Generate a json file for a given modality_category and session.
        :param file_stem:
        :param contrast:
        :param session:
        :return:
        """
        # Generate JSON file
        file_name_json: str = file_stem + ".json"

        if session:
            # path to JSON file
            path_json_file: Path = Path(
                self.path_to_mock_data,
                f"derivatives",
                f"labels",
                f"sub-{self.index_subject:02d}",
                f"ses-{session:02d}",
                f"{modality_category}",
                file_name_json,
            )
        else:
            # path to JSON file
            path_json_file: Path = Path(
                self.path_to_mock_data,
                f"derivatives",
                f"labels",
                f"sub-{self.index_subject:02d}",
                f"{modality_category}",
                file_name_json,
            )
        # ensure the parent folder exists
        path_json_file.parent.mkdir(parents=True, exist_ok=True)
        mock_json: object = self.generate_file_description_dict(bids_detail)

        # Save mock_json dictionary into a json file:
        with open(path_json_file, "w") as f:
            json.dump(mock_json, f, indent=4, sort_keys=True)

    def generate_a_nifti_label(
        self, file_stem: str, session: str or None, modality_category: str = "anat"
    ):
        """
        Produce the expected nifti files for a given modality_category and session.
        :param file_stem:
        :param modality_category:
        :param session:
        :return:
        """
        # Generate Nifti file
        file_name_nii: str = file_stem + ".nii"
        if session:
            # create nii file
            path_nii_file: Path = Path(
                self.path_to_mock_data,
                f"derivatives",
                f"labels",
                f"sub-{self.index_subject:02d}",
                f"ses-{session:02d}",
                f"{modality_category}",
                file_name_nii,
            )
        else:
            # create nii file
            path_nii_file: Path = Path(
                self.path_to_mock_data,
                f"derivatives",
                f"labels",
                f"sub-{self.index_subject:02d}",
                f"{modality_category}",
                file_name_nii,
            )
        # Ensure the parent folder exists
        path_nii_file.parent.mkdir(parents=True, exist_ok=True)
        mock_data: Nifti1Image = create_mock_nifti1_object()
        save_nifty_data(mock_data, path_nii_file)
