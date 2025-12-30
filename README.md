# McDoc - Document Framework and Library System

A comprehensive document framework for importing user-created documents, formatting them with templates, and producing uniform documents for a centralized library.

## Overview

McDoc provides a complete solution for:
- **Importing** documents from various formats (JSON, Markdown, plain text)
- **Formatting** content using customizable templates
- **Processing** documents to ensure uniform styling
- **Managing** a centralized document library

## Quick Start

```bash
# List available templates
python src/mcdoc_cli.py list-templates

# Import and process a document
python src/mcdoc_cli.py import examples/example_basic.json

# Create a new document interactively
python src/mcdoc_cli.py create --template basic
```

## Features

- ✅ Flexible template system with placeholder-based formatting
- ✅ Support for multiple input formats (JSON, Markdown, text)
- ✅ Automated document processing and formatting
- ✅ Centralized library for uniform document storage
- ✅ CLI and Python API for easy integration
- ✅ Metadata tracking and document versioning

## Structure

```
McDoc/
├── src/mcdoc/          # Core framework
├── templates/          # Document templates
├── examples/           # Example documents
├── library/            # Processed document library
└── documents/          # User documents for import
```

## Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed usage instructions, API reference, and examples.

## Templates

Included templates:
- **basic** - Simple document with title, author, and body
- **technical_report** - Comprehensive technical report format
- **meeting_notes** - Meeting minutes and notes template

## Example Usage

### Import a document:
```bash
python src/mcdoc_cli.py import my_doc.md --template basic --author "John Doe"
```

### Create a document interactively:
```bash
python src/mcdoc_cli.py create --template technical_report
```

### Use the Python API:
```python
from mcdoc import TemplateRegistry, DocumentProcessor, DocumentImporter

registry = TemplateRegistry('templates')
importer = DocumentImporter()
processor = DocumentProcessor(registry)

doc = importer.import_from_json('my_document.json')
formatted = processor.process(doc)
processor.save_to_library(doc, 'library')
```

## Requirements

- Python 3.7+
- Optional: PyYAML (for Markdown frontmatter support)

## License

Open source document framework.
