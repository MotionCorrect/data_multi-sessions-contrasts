import json
from abc import abstractmethod
from pathlib import Path
import multiprocessing
from typing import List

from nibabel import Nifti1Image

from nifti_mocker import (
    create_mock_nifti1_object,
    create_mock_nifti2_object,
    check_nifty_data,
    save_nifty_data,
)


class CreateSubject(multiprocessing.Process):
    """
    This is s the abstract class that highlights the main way to interact with subject related creation process
    """

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
        self.path_to_mock_data = path_to_mock_data
        self.list_sessions = list_sessions
        self.list_modalities = list_anatomy_modalities

    @staticmethod
    @abstractmethod
    def default_constructor(path_to_mock_data: str):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        """
        Main entry point of the multiprocess.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def create_one_json_nii_pair(self, session: str, contrast: str, kwargs=None):
        raise NotImplementedError

    @abstractmethod
    def generate_a_json_file(
        self,
        file_stem: str,
        session: str,
        contrast: str,
        modality_category: str = "anat",
    ):
        raise NotImplementedError

    @abstractmethod
    def create_file_stem(self, session: str, modality: str, *kwargs):
        raise NotImplementedError

    @abstractmethod
    def generate_file_description_dict(self, contrast: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def generate_dataset_description_dict(self) -> dict:
        raise NotImplementedError
