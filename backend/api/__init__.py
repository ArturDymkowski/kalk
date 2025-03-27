"""
Pakiet zawierający trasy API i integrację z zewnętrznymi usługami.
"""

from .routes import api_bp
from .openai_client import OpenAIClient

__all__ = ['api_bp', 'OpenAIClient']
