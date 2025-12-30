# McDoc - Document Framework and Library System

McDoc is a comprehensive document framework that allows you to import user-created documents, format them using templates, and produce uniform documents for a centralized library.

## Features

- **Template System**: Create and manage document templates with consistent formatting
- **Document Import**: Import documents from JSON, Markdown, or plain text files
- **Automatic Formatting**: Apply templates to user content automatically
- **Document Library**: Organize processed documents in a centralized library
- **CLI Interface**: Easy-to-use command-line tools for all operations
- **Metadata Management**: Track document metadata including author, date, version, etc.

## Folder Structure

```
McDoc/
├── src/                    # Source code
│   └── mcdoc/             # Main package
│       ├── __init__.py    # Package initialization
│       ├── template.py    # Template system
│       ├── document.py    # Document management
│       └── importer.py    # Document import functionality
├── templates/             # Document templates
│   ├── basic.md          # Basic template
│   ├── technical_report.md # Technical report template
│   └── meeting_notes.md  # Meeting notes template
├── documents/            # User documents (to be imported)
├── library/             # Processed documents library
├── examples/            # Example documents
└── config.json         # Configuration file
```

## Installation

No installation required! McDoc is a standalone Python framework.

Requirements:
- Python 3.7 or higher

Optional dependencies for enhanced functionality:
```bash
pip install pyyaml  # For YAML frontmatter in Markdown files
```

## Quick Start

### 1. List Available Templates

```bash
python src/mcdoc_cli.py list-templates
```

### 2. Import a Document

Import a JSON document:
```bash
python src/mcdoc_cli.py import examples/example_basic.json
```

Import a Markdown file:
```bash
python src/mcdoc_cli.py import examples/example_markdown.md --template basic --author "Jane Doe"
```

### 3. Create a Document Interactively

```bash
python src/mcdoc_cli.py create --template basic
```

### 4. Process an Existing Document

```bash
python src/mcdoc_cli.py process documents/my_document.json
```

## Templates

### Available Templates

1. **basic** - Simple document template with title, author, and body
2. **technical_report** - Comprehensive technical report with sections
3. **meeting_notes** - Meeting notes and minutes template

### Template Format

Templates use a simple `{{placeholder}}` syntax. Example:

```markdown
# {{title}}

**Author:** {{author}}
**Date:** {{created_at}}

## Content

{{body}}
```

### Creating Custom Templates

1. Create a Markdown file in the `templates/` directory
2. Use `{{field_name}}` for placeholders
3. Optionally create a `.json` file with metadata:

```json
{
  "name": "my_template",
  "description": "My custom template",
  "version": "1.0",
  "required_fields": ["title", "body", "author"]
}
```

## Document Import Formats

### JSON Format

```json
{
  "title": "Document Title",
  "template": "basic",
  "content": {
    "body": "Document content here",
    "author": "Author Name"
  },
  "metadata": {
    "category": "example",
    "tags": ["demo"]
  }
}
```

### Markdown Format

Any `.md` file can be imported. The first `# Heading` becomes the title:

```markdown
# My Document Title

Document content goes here.
```

### Plain Text

Any text file can be imported with a specified template.

## CLI Commands

### list-templates

List all available templates.

```bash
python src/mcdoc_cli.py list-templates [--templates-dir DIR]
```

### import

Import and process a document.

```bash
python src/mcdoc_cli.py import FILE [OPTIONS]

Options:
  --template NAME       Template to use
  --author NAME        Document author
  --output PATH        Custom output file
  --templates-dir DIR  Templates directory (default: templates)
  --library-dir DIR    Library directory (default: library)
```

### process

Process an existing McDoc JSON document.

```bash
python src/mcdoc_cli.py process FILE [OPTIONS]

Options:
  --output PATH        Custom output file
  --templates-dir DIR  Templates directory
  --library-dir DIR    Library directory
```

### create

Create a new document interactively.

```bash
python src/mcdoc_cli.py create --template NAME [OPTIONS]

Options:
  --template NAME      Template to use (required)
  --templates-dir DIR  Templates directory
  --library-dir DIR    Library directory
```

## Python API

### Using McDoc in Code

```python
from mcdoc import (
    TemplateRegistry,
    DocumentProcessor,
    DocumentImporter,
    Document
)

# Initialize components
registry = TemplateRegistry('templates')
importer = DocumentImporter()
processor = DocumentProcessor(registry)

# Import a document
doc = importer.import_from_json('examples/example_basic.json')

# Process with template
formatted = processor.process(doc)

# Save to library
output_path = processor.save_to_library(doc, 'library')
print(f"Saved to: {output_path}")
```

### Creating Documents Programmatically

```python
from mcdoc import Document, DocumentProcessor, TemplateRegistry

# Create a document
content = {
    'body': 'This is my document content.',
    'author': 'John Doe'
}

doc = Document(
    title='My Document',
    content=content,
    template_name='basic'
)

# Process and save
registry = TemplateRegistry('templates')
processor = DocumentProcessor(registry)
formatted = processor.process(doc)
output_path = processor.save_to_library(doc, 'library')
```

## Use Cases

### 1. Standardizing Meeting Notes

Import informal meeting notes and convert them to a standard format:

```bash
python src/mcdoc_cli.py import notes.txt --template meeting_notes
```

### 2. Creating Technical Reports

Use the technical report template for consistent documentation:

```bash
python src/mcdoc_cli.py create --template technical_report
```

### 3. Building a Document Library

Process multiple documents to build a uniform library:

```bash
for file in documents/*.json; do
    python src/mcdoc_cli.py import "$file"
done
```

## Configuration

Edit `config.json` to customize default settings:

```json
{
  "mcdoc": {
    "templates_dir": "templates",
    "documents_dir": "documents",
    "library_dir": "library"
  },
  "defaults": {
    "template": "basic",
    "author": "Unknown"
  }
}
```

## Best Practices

1. **Use Templates Consistently**: Pick templates that match your document type
2. **Include Metadata**: Add relevant metadata for better organization
3. **Review Required Fields**: Check template requirements before creating documents
4. **Organize Library**: Use the library directory for processed, uniform documents
5. **Version Templates**: Update template version numbers when making changes

## Troubleshooting

### Template Not Found

Ensure the template exists in the templates directory:
```bash
python src/mcdoc_cli.py list-templates
```

### Missing Required Fields

Check template requirements:
```bash
python src/mcdoc_cli.py list-templates
```

### Import Errors

Verify the document format matches the expected structure (JSON, Markdown, or text).

## Contributing

To add new templates:
1. Create a `.md` template file in `templates/`
2. Add a corresponding `.json` metadata file
3. Test with example documents

## License

This project is part of the McDoc documentation library framework.

## Support

For issues and questions, please refer to the repository documentation or create an issue in the GitHub repository.
