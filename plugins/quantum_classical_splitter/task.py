from tempfile import SpooledTemporaryFile

from typing import Optional
from json import loads

from celery.utils.log import get_task_logger

from . import QuantumClassicalSplitterBp
from qhana_plugin_runner.celery import CELERY
from qhana_plugin_runner.db.models.tasks import ProcessingTask

import requests

from qhana_plugin_runner.storage import STORE

TASK_LOGGER = get_task_logger(__name__)


@CELERY.task(name=f"{QuantumClassicalSplitterBp.instance.identifier}.processing_task", bind=True)
def processing_task(self, db_id: int) -> str:
    TASK_LOGGER.info(f"Starting BPMN File Questionaire Generator")
    task_data: Optional[ProcessingTask] = ProcessingTask.get_by_id(id_=db_id)

    if task_data is None:
        msg = f"Could not load task data with id {db_id} to read parameters!"
        TASK_LOGGER.error(msg)
        raise KeyError(msg)

    # TODO: Perform Request to Server
    #requests.post("localhost:8080/data", data={'file': file_input})
    return "Correct"
