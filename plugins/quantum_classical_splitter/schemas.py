import marshmallow as ma
from qhana_plugin_runner.api.util import (
    FrontendFormBaseSchema,
    MaBaseSchema,
    FileUrl
)

class QuantumClassicalSplitterParameterSchema(FrontendFormBaseSchema):
    pass


class QuantumClassicalSplitterRequestSchema(FrontendFormBaseSchema):
    input_data = FileUrl(
        required=True,
        allow_none=False,
        load_only=True,
        metadata={
            "label": "Input Data"
        }
    )
