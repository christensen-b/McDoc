"""
McDoc - Document Framework and Library System
"""

__version__ = "0.1.0"

from .template import Template, TemplateRegistry
from .document import Document, DocumentProcessor
from .importer import DocumentImporter

__all__ = [
    "Template",
    "TemplateRegistry",
    "Document",
    "DocumentProcessor",
    "DocumentImporter",
]
