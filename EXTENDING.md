# Extending McDoc

This guide explains how to extend the McDoc framework with custom templates, importers, and processors.

## Creating Custom Templates

### Template Structure

Templates are Markdown files with placeholders in the format `{{field_name}}`.

**Example Template** (`templates/my_template.md`):

```markdown
# {{title}}

**Category:** {{category}}
**Priority:** {{priority}}

## Description

{{description}}

## Details

{{details}}
```

### Template Metadata

Create a corresponding JSON file with template metadata:

**Example Metadata** (`templates/my_template.json`):

```json
{
  "name": "my_template",
  "description": "Custom template for specific use case",
  "version": "1.0",
  "author": "Your Name",
  "required_fields": [
    "title",
    "category",
    "priority",
    "description",
    "details"
  ],
  "optional_fields": [
    "tags",
    "related_documents"
  ]
}
```

### Advanced Template Features

#### Conditional Sections

While the basic template system uses simple replacement, you can create templates with optional sections by using empty strings for missing fields:

```markdown
# {{title}}

{{optional_section}}

Main content: {{body}}
```

If `optional_section` is empty, it won't appear in the output.

#### Nested Content

For complex nested content, use the content dictionary structure:

```python
content = {
    'title': 'My Document',
    'section1_title': 'Introduction',
    'section1_body': 'Introduction text',
    'section2_title': 'Details',
    'section2_body': 'Details text'
}
```

Template:
```markdown
# {{title}}

## {{section1_title}}
{{section1_body}}

## {{section2_title}}
{{section2_body}}
```

## Custom Document Importers

### Extending the DocumentImporter Class

Create a custom importer by extending the base class:

```python
from mcdoc.importer import DocumentImporter
from mcdoc.document import Document
import xml.etree.ElementTree as ET

class XMLImporter(DocumentImporter):
    """Custom importer for XML documents"""
    
    def import_from_xml(self, filepath, template_name='basic'):
        """Import document from XML file"""
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        title = root.find('title').text
        content = {}
        
        for elem in root:
            if elem.tag != 'title':
                content[elem.tag] = elem.text
        
        return Document(title, content, template_name)
```

### Using Custom Importers

```python
from custom_importers import XMLImporter

importer = XMLImporter()
doc = importer.import_from_xml('document.xml', 'basic')
```

## Custom Document Processors

### Creating a Specialized Processor

Extend the DocumentProcessor for custom processing logic:

```python
from mcdoc.document import DocumentProcessor
from datetime import datetime

class TimestampedProcessor(DocumentProcessor):
    """Processor that adds timestamps to all documents"""
    
    def process(self, document):
        # Add timestamp to metadata
        document.metadata['processed_at'] = datetime.now().isoformat()
        document.metadata['processor_version'] = '1.0'
        
        # Call parent process method
        return super().process(document)
```

### Adding Validation

```python
class ValidatingProcessor(DocumentProcessor):
    """Processor with field validation"""
    
    def process(self, document):
        template = self.template_registry.get_template(document.template_name)
        if not template:
            raise ValueError(f"Template not found: {document.template_name}")
        
        # Check required fields
        required = template.get_required_fields()
        missing = []
        
        for field in required:
            if field not in document.content and field not in document.metadata:
                if field != 'title':  # title is separate
                    missing.append(field)
        
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        
        return super().process(document)
```

## Plugin System

### Creating Plugins

Create a plugins directory and define plugin interfaces:

```python
# plugins/base_plugin.py
class McDocPlugin:
    """Base class for McDoc plugins"""
    
    def __init__(self, config=None):
        self.config = config or {}
    
    def pre_process(self, document):
        """Called before document processing"""
        return document
    
    def post_process(self, document, formatted_content):
        """Called after document processing"""
        return formatted_content
```

### Example Plugin

```python
# plugins/markdown_enhancer.py
from .base_plugin import McDocPlugin
import re

class MarkdownEnhancer(McDocPlugin):
    """Plugin to enhance markdown output"""
    
    def post_process(self, document, formatted_content):
        # Add table of contents
        toc = self._generate_toc(formatted_content)
        
        # Insert TOC after first heading
        lines = formatted_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# '):
                lines.insert(i + 1, '\n## Table of Contents\n' + toc)
                break
        
        return '\n'.join(lines)
    
    def _generate_toc(self, content):
        headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        toc = []
        for heading in headings:
            if heading != 'Table of Contents':
                anchor = heading.lower().replace(' ', '-')
                toc.append(f"- [{heading}](#{anchor})")
        return '\n'.join(toc)
```

### Using Plugins

```python
from mcdoc import DocumentProcessor, TemplateRegistry
from plugins.markdown_enhancer import MarkdownEnhancer

registry = TemplateRegistry('templates')
processor = DocumentProcessor(registry)

# Create and apply plugin
plugin = MarkdownEnhancer()
formatted = processor.process(document)
enhanced = plugin.post_process(document, formatted)
```

## Advanced Template Registry

### Custom Template Loading

```python
from mcdoc.template import TemplateRegistry, Template

class DatabaseTemplateRegistry(TemplateRegistry):
    """Load templates from a database"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.templates = {}
        self._load_from_database()
    
    def _load_from_database(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT name, content, metadata FROM templates")
        
        for row in cursor.fetchall():
            name, content, metadata_json = row
            metadata = json.loads(metadata_json)
            
            # Create template from database content
            template = Template(name, '', metadata)
            template.content = content
            self.templates[name] = template
```

## Custom CLI Commands

### Extending the CLI

Add new commands to the CLI:

```python
# src/mcdoc_cli_extended.py
from mcdoc_cli import main as base_main
import argparse

def extended_main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    # Add custom command
    validate_parser = subparsers.add_parser('validate',
                                           help='Validate a document')
    validate_parser.add_argument('file', help='Document to validate')
    validate_parser.add_argument('--template', help='Template to validate against')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        return validate_document(args)
    
    # Fall back to base CLI
    return base_main()

def validate_document(args):
    # Validation logic here
    pass
```

## Integration Examples

### Web API Integration

```python
from flask import Flask, request, jsonify
from mcdoc import TemplateRegistry, DocumentProcessor, Document

app = Flask(__name__)
registry = TemplateRegistry('templates')
processor = DocumentProcessor(registry)

@app.route('/api/process', methods=['POST'])
def process_document():
    data = request.json
    
    doc = Document(
        title=data['title'],
        content=data['content'],
        template_name=data['template']
    )
    
    formatted = processor.process(doc)
    output_path = processor.save_to_library(doc, 'library')
    
    return jsonify({
        'status': 'success',
        'formatted': formatted,
        'path': output_path
    })
```

### Batch Processing

```python
from pathlib import Path
from mcdoc import TemplateRegistry, DocumentProcessor, DocumentImporter

def batch_import(input_dir, template_name='basic'):
    """Import and process all documents in a directory"""
    
    registry = TemplateRegistry('templates')
    processor = DocumentProcessor(registry)
    importer = DocumentImporter()
    
    results = []
    
    for filepath in Path(input_dir).glob('*'):
        if filepath.is_file():
            try:
                doc = importer.import_document(str(filepath), template_name)
                processor.process(doc)
                output = processor.save_to_library(doc, 'library')
                results.append({'file': str(filepath), 'status': 'success', 'output': output})
            except Exception as e:
                results.append({'file': str(filepath), 'status': 'error', 'error': str(e)})
    
    return results
```

## Best Practices

1. **Template Versioning**: Include version numbers in template metadata
2. **Field Validation**: Validate required fields before processing
3. **Error Handling**: Provide clear error messages for missing fields
4. **Documentation**: Document custom templates and their requirements
5. **Testing**: Test templates with various content types
6. **Backward Compatibility**: Maintain compatibility when updating templates

## Troubleshooting Custom Extensions

### Template Not Loading

- Verify template file is in the templates directory
- Check that .md and .json files have matching names
- Validate JSON metadata syntax

### Missing Fields Error

- Review required_fields in template metadata
- Ensure content dictionary includes all required fields
- Check for typos in field names

### Import Failures

- Verify file format is supported
- Check file encoding (should be UTF-8)
- Validate JSON structure for JSON imports

## Contributing Extensions

To contribute custom templates or extensions:

1. Create templates in the `templates/` directory
2. Add examples to `examples/`
3. Update documentation
4. Test with various document types
5. Submit pull request with description

## Resources

- [Main Documentation](DOCUMENTATION.md)
- [README](README.md)
- [Template Examples](templates/)
- [Document Examples](examples/)
