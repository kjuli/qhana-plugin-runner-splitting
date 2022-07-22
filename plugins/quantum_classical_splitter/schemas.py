import marshmallow as ma
from qhana_plugin_runner.api.util import (
    FrontendFormBaseSchema,
    MaBaseSchema,
    FileUrl
)

class QuantumClassicalSplitterParameterSchema(FrontendFormBaseSchema):
    pass

class TaskResponseSchema(MaBaseSchema):  # TODO: move to plugin runner?
    name = ma.fields.String(required=True, allow_none=False, dump_only=True)
    task_id = ma.fields.String(required=True, allow_none=False, dump_only=True)
    task_result_url = ma.fields.Url(required=True, allow_none=False, dump_only=True)

class QuantumClassicalSplitterRequestSchema(FrontendFormBaseSchema):
    input_data = FileUrl(
        required=True,
        allow_none=False,
        load_only=True,
        metadata={
            "label": "Input Data"
        }
    )
