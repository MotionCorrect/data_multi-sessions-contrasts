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

list_bids_keywords = ["acq", "desc", "run"]


class CreateBIDSSubjects(CreateSubject):
    def __init__(
        self,
        process_id,
        index_subject,
        path_to_mock_data,
        list_sessions,
        list_anatomy_modalities,
    ):
        """
        Constructor that focus on create all sessions/modalities for a given subject.
        :param process_id:
        :param index_subject:
        :param path_to_mock_data:
        :param list_sessions:
        :param list_anatomy_modalities:
        """
        super(CreateSubject, self).__init__()
        self.id = process_id
        self.index_subject = index_subject
        self.path_to_mock_data = Path(path_to_mock_data)
        self.list_sessions = list_sessions
        self.list_modalities = list_anatomy_modalities

    @staticmethod
    def default_constructor(path_to_mock_data):
        """
        Default constructor.
        :return:
        """
        id = 1
        index_subject = [1, 2, 3, 4, 5]
        list_sessions = [1, 2, 3]
        list_modalities = ["T1w", "T2w", "FLAIR", "PD"]
        CreateBIDSSubjects(
            id, index_subject, path_to_mock_data, list_sessions, list_modalities
        )

    def run(self):
        """
        Main entry point of the multiprocess.
        :return:
        """
        self.create_sessions(self.list_sessions, self.list_modalities)

        # Save mock_json dictionary into a json file:
        mock_json: dict = self.generate_dataset_description_dict()

        path_json_file: Path = self.path_to_mock_data / "dataset_description.json"
        with open(str(path_json_file), "w") as f:
            json.dump(mock_json, f, indent=4, sort_keys=True)

    def create_sessions(self, sessions: List[str], anatomy_modalities: List[str]):
        for session in sessions:
            self.create_session_specific_contrasts(session, anatomy_modalities)

    def create_session_specific_contrasts(
        self, session: str, list_contrasts: List[str]
    ):
        """
        Create the expected nifti files for a given session.
        :param session:
        :param list_contrasts:
        :return:
        """
        for contrast in list_contrasts:
            self.create_one_json_nii_pair(session, contrast)

    def create_one_json_nii_pair(self, session: str, contrast: str, kwargs=None):
        """
        Create a nifti/JSON image pairs with an explicitly set list of session and model
        :param session:
        :param contrast:
        :param kwargs:
        :return:
        """
        file_stem: str = self.create_file_stem(session, contrast, kwargs)

        self.generate_a_json_file(
            file_stem, session=session, contrast=contrast, modality_category="anat"
        )

        self.generate_a_nifti_file(
            file_stem, session=session, modality_category="anat"
        )

    def generate_a_nifti_file(
        self, file_stem: str, modality_category: str, session: str
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
        # create nii file
        path_nii_file: Path = Path(
            self.path_to_mock_data,
            f"sub-{self.index_subject:02d}",
            f"ses-{session:02d}",
            f"{modality_category}",
            file_name_nii,
        )
        mock_data: Nifti1Image = create_mock_nifti1_object()
        path_nii_file.parent.mkdir(parents=True, exist_ok=True)
        save_nifty_data(mock_data, path_nii_file)

    def create_file_stem(self, session: str, modality: str, *kwargs):
        """
        Create a file stem for a nifti/JSON image pairs.
        :param session:
        :param modality:
        :param kwargs:
        :return:
        """
        stem = f"sub-{self.index_subject:02d}_ses-{session:02d}_{modality}"
        for keyword in list_bids_keywords:
            if keyword in kwargs:
                stem += f"_{keyword}-{kwargs.get(keyword,'')}"
        return stem

    def generate_a_json_file(
        self,
        file_stem: str,
        session: str,
        contrast: str,
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

        # path to JSON file
        path_json_file: Path = Path(
            self.path_to_mock_data,
            f"sub-{self.index_subject:02d}",
            f"ses-{session:02d}",
            f"{modality_category}",
            file_name_json,
        )
        # ensure the parent folder exists
        path_json_file.parent.mkdir(parents=True, exist_ok=True)
        mock_json: object = self.generate_file_description_dict(contrast)

        # Save mock_json dictionary into a json file:
        with open(path_json_file, "w") as f:
            json.dump(mock_json, f, indent=4, sort_keys=True)

    def generate_file_description_dict(self, contrast: str) -> dict:
        """
        Fill a json dictionary with a description of the nifti image.
        :param contrast:
        :return:
        """
        mock_meta_data = {
            "Modality": "MR",
            "MagneticFieldStrength": 3,
            "Manufacturer": "MOCK",
            "InstitutionName": "MOCK Research Center",
            "MRAcquisitionType": "3D",
            "SeriesDescription": contrast,
            "ProtocolName": contrast,
            "EchoTime": 1,
            "RepetitionTime": 1,
            "InversionTime": 1,
            "FlipAngle": 1,
            "SliceThickness": 1,
            "ConversionSoftware": "MOCK",
        }
        return mock_meta_data

    def generate_dataset_description_dict(self) -> dict:
        """
        Fill a json dictionary with a description of the entire dataset of the collections of the nifti images.
        :return:
        """
        mock_meta_dataset = {
            "Name": "MOCK multi-contrast multi-session dataset",
            "BIDSVersion": "1.0.2",
            "Researcher": "MOCK_RESEARCHER",
            "Study": "MOCK_STUDY",
            "PipelineDescription": {
                "Name": "MOCK  ivadomed multi contrast multi session pipeline"
            },
        }
        return mock_meta_dataset
