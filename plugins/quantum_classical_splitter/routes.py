from http import HTTPStatus
from json import dumps
from typing import Mapping, Optional

import requests
from celery.canvas import chain
from flask import Response, redirect
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from flask.views import MethodView
from marshmallow import EXCLUDE
from celery.utils.log import get_task_logger
from marshmallow.utils import INCLUDE

from .schemas import QuantumClassicalSplitterParameterSchema, QuantumClassicalSplitterRequestSchema, TaskResponseSchema

from qhana_plugin_runner.api.plugin_schemas import (
    PluginMetadata,
    PluginMetadataSchema,
    PluginType,
    EntryPoint,
    DataMetadata,
)

from . import QuantumClassicalSplitterBp, QUANTUM_CLASSICAL_SPLITTER_BP
from qhana_plugin_runner.db.models.tasks import ProcessingTask
from qhana_plugin_runner.tasks import (
    add_step,
    save_task_error,
    save_task_result,
)

from .task import processing_task



@QUANTUM_CLASSICAL_SPLITTER_BP.route("/")
class PluginsView(MethodView):

    @QUANTUM_CLASSICAL_SPLITTER_BP.response(HTTPStatus.OK, PluginMetadataSchema())
    @QUANTUM_CLASSICAL_SPLITTER_BP.require_jwt("jwt", optional=True)
    def get(self):
        return PluginMetadata(
            title="Quantum-Classical Splitter",
            description="Generator for identifying steps in BPMN to assign to a QC",
            name=QuantumClassicalSplitterBp.instance.name,
            version=QuantumClassicalSplitterBp.instance.version,
            type=PluginType.complex,
            entry_point=EntryPoint(
                href=url_for(f"{QUANTUM_CLASSICAL_SPLITTER_BP.name}.ProcessView"),
                ui_href=url_for(f"{QUANTUM_CLASSICAL_SPLITTER_BP.name}.MicroFrontend"),
                data_input=[],
                data_output=[]
            ),
            tags=["data-annotation"]
        )

@QUANTUM_CLASSICAL_SPLITTER_BP.route("/ui/")
class MicroFrontend(MethodView):

    @QUANTUM_CLASSICAL_SPLITTER_BP.response(HTTPStatus.OK)
    @QUANTUM_CLASSICAL_SPLITTER_BP.arguments(
        QuantumClassicalSplitterParameterSchema(partial=True, unknown=EXCLUDE),
        location="query",
        required=False
    )
    @QUANTUM_CLASSICAL_SPLITTER_BP.require_jwt("jwt", optional=True)
    def get(self, errors):
        return self.render(request.args, errors)

    @QUANTUM_CLASSICAL_SPLITTER_BP.html_response(HTTPStatus.OK)
    @QUANTUM_CLASSICAL_SPLITTER_BP.arguments(
        QuantumClassicalSplitterParameterSchema(partial=True, unknown=EXCLUDE),
        location="query",
        required=False
    )
    @QUANTUM_CLASSICAL_SPLITTER_BP.require_jwt("jwt", optional=True)
    def post(self, errors):
        return self.render(request.form, errors)

    def render(self, data: Mapping, errors: dict):
        schema = QuantumClassicalSplitterParameterSchema()
        return Response(
            render_template(
                "quantum_classical_splitter_questionnaire.html",
                name=QuantumClassicalSplitterBp.instance.name,
                version=QuantumClassicalSplitterBp.instance.version,
                schema=schema,
                values=data,
                errors=errors,
                process=url_for(f"{QUANTUM_CLASSICAL_SPLITTER_BP.name}.ProcessView"),
                help_text="Some **help_text**",
                examples_values={}
            )
        )


@QUANTUM_CLASSICAL_SPLITTER_BP.route("/process/")
class ProcessView(MethodView):

    @QUANTUM_CLASSICAL_SPLITTER_BP.response(HTTPStatus.OK, TaskResponseSchema())
    @QUANTUM_CLASSICAL_SPLITTER_BP.arguments(
        QuantumClassicalSplitterRequestSchema(unknown=EXCLUDE), location="form"
    )
    def post(self, req_dict):
        """Start the demo task."""
        db_task = ProcessingTask(
            task_name=processing_task.name,
            parameters=dumps(req_dict),
        )
        db_task.save(commit=True)

        try:
            if "file" not in request.files:
                raise ValueError()

            file = request.files["file"]

            # requests.post("localhost:8080", data=file) Look Into this

        except Exception as err:
            pass

        return redirect(url_for(f"{QUANTUM_CLASSICAL_SPLITTER_BP.name}.QuestionnaireView"), HTTPStatus.SEE_OTHER)

@QUANTUM_CLASSICAL_SPLITTER_BP.route("/questionnaire/")
class QuestionnaireView(MethodView):

    @QUANTUM_CLASSICAL_SPLITTER_BP.html_response(HTTPStatus.OK)
    @QUANTUM_CLASSICAL_SPLITTER_BP.arguments(
        QuantumClassicalSplitterParameterSchema(partial=True, unknown=EXCLUDE),
        location="query",
        required=False
    )
    @QUANTUM_CLASSICAL_SPLITTER_BP.require_jwt("jwt", optional=True)
    def get(self, errors):
        return self.render(errors)

    def render(self, errors):
        schema = QuantumClassicalSplitterParameterSchema()
        return Response(
            render_template(
                "quantum_classical_splitter_questionnaire.html",
                name=QuantumClassicalSplitterBp.instance.name,
                version=QuantumClassicalSplitterBp.instance.version,
                schema=schema,
                values={},
                errors=errors,
                process=url_for(f"{QUANTUM_CLASSICAL_SPLITTER_BP.name}.ProcessView"),
                help_text="Some **help_text**",
                examples_values={}
            )
        )
