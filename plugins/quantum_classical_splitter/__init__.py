from flask import Flask

from qhana_plugin_runner.api.util import SecurityBlueprint
from qhana_plugin_runner.util.plugins import plugin_identifier, QHAnaPluginBase

_plugin_name = "quantum-classical-splitter"
__version__ = "v0.1.0"
_identifier = plugin_identifier(_plugin_name, __version__)

QUANTUM_CLASSICAL_SPLITTER_BP = SecurityBlueprint(
    _identifier,
    __name__,
    description="A quantum-classical splitter that can identify steps in a BPMN which shall be run on a specific quantum computer.",
    template_folder="quantum_classical_splitter_templates"
)


class QuantumClassicalSplitterBp(QHAnaPluginBase):

    name = _plugin_name
    version = __version__

    def __init__(self, app):
        super().__init__(app)

    def get_api_blueprint(self):
        return QUANTUM_CLASSICAL_SPLITTER_BP

    def get_requirements(self) -> str:
        return ""


try:
    # It is important to import the routes **after** COSTUME_LOADER_BLP and CostumeLoader are defined, because they are
    # accessed as soon as the routes are imported.
    from . import routes
except ImportError:
    # When running `poetry run flask install`, importing the routes will fail, because the dependencies are not
    # installed yet.
    pass
