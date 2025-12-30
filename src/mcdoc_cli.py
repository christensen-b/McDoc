#!/usr/bin/env python3
"""
McDoc CLI - Command Line Interface for Document Framework
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcdoc import (
    Template,
    TemplateRegistry,
    Document,
    DocumentProcessor,
    DocumentImporter
)


def main():
    parser = argparse.ArgumentParser(
        description='McDoc - Document Framework and Library System'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List templates command
    list_parser = subparsers.add_parser('list-templates', 
                                        help='List available templates')
    list_parser.add_argument('--templates-dir', default='templates',
                            help='Templates directory path')
    
    # Import command
    import_parser = subparsers.add_parser('import',
                                          help='Import a document')
    import_parser.add_argument('file', help='File to import')
    import_parser.add_argument('--template', help='Template to use')
    import_parser.add_argument('--output', help='Output file path')
    import_parser.add_argument('--templates-dir', default='templates',
                              help='Templates directory path')
    import_parser.add_argument('--library-dir', default='library',
                              help='Library directory path')
    import_parser.add_argument('--author', help='Document author')
    
    # Process command
    process_parser = subparsers.add_parser('process',
                                           help='Process a document with template')
    process_parser.add_argument('file', help='Document file to process')
    process_parser.add_argument('--templates-dir', default='templates',
                               help='Templates directory path')
    process_parser.add_argument('--library-dir', default='library',
                               help='Library directory path')
    process_parser.add_argument('--output', help='Output file path')
    
    # Create document command
    create_parser = subparsers.add_parser('create',
                                          help='Create a new document interactively')
    create_parser.add_argument('--template', required=True,
                              help='Template to use')
    create_parser.add_argument('--templates-dir', default='templates',
                              help='Templates directory path')
    create_parser.add_argument('--library-dir', default='library',
                              help='Library directory path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Handle commands
    if args.command == 'list-templates':
        return list_templates(args)
    elif args.command == 'import':
        return import_document(args)
    elif args.command == 'process':
        return process_document(args)
    elif args.command == 'create':
        return create_document(args)
    
    return 0


def list_templates(args):
    """List all available templates"""
    registry = TemplateRegistry(args.templates_dir)
    templates = registry.list_templates()
    
    if not templates:
        print(f"No templates found in {args.templates_dir}")
        return 1
    
    print("Available templates:")
    for name in templates:
        template = registry.get_template(name)
        description = template.metadata.get('description', 'No description')
        print(f"  - {name}: {description}")
        required = template.get_required_fields()
        if required:
            print(f"    Required fields: {', '.join(required)}")
    
    return 0


def import_document(args):
    """Import a document"""
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        return 1
    
    # Initialize components
    registry = TemplateRegistry(args.templates_dir)
    importer = DocumentImporter()
    processor = DocumentProcessor(registry)
    
    # Set up metadata
    metadata = {}
    if args.author:
        metadata['author'] = args.author
    
    # Import document
    print(f"Importing document from {args.file}...")
    doc = importer.import_document(args.file, args.template, metadata)
    
    # Add default author if not set
    if 'author' not in doc.content and 'author' not in doc.metadata:
        doc.metadata['author'] = 'Unknown'
    
    # Process document
    print(f"Processing with template: {doc.template_name}")
    try:
        formatted = processor.process(doc)
        
        # Save to library
        output_path = processor.save_to_library(doc, args.library_dir)
        print(f"Document saved to library: {output_path}")
        
        # Save to custom output if specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"Also saved to: {args.output}")
        
        return 0
    except Exception as e:
        print(f"Error processing document: {e}")
        return 1


def process_document(args):
    """Process an existing document"""
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        return 1
    
    # Initialize components
    registry = TemplateRegistry(args.templates_dir)
    processor = DocumentProcessor(registry)
    
    # Load document
    print(f"Loading document from {args.file}...")
    try:
        doc = Document.load_from_file(args.file)
    except Exception as e:
        print(f"Error loading document: {e}")
        return 1
    
    # Process document
    print(f"Processing with template: {doc.template_name}")
    try:
        formatted = processor.process(doc)
        
        # Save to library
        output_path = processor.save_to_library(doc, args.library_dir)
        print(f"Document saved to library: {output_path}")
        
        # Save to custom output if specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"Also saved to: {args.output}")
        
        return 0
    except Exception as e:
        print(f"Error processing document: {e}")
        return 1


def create_document(args):
    """Create a document interactively"""
    # Initialize components
    registry = TemplateRegistry(args.templates_dir)
    processor = DocumentProcessor(registry)
    
    # Get template
    template = registry.get_template(args.template)
    if not template:
        print(f"Error: Template '{args.template}' not found")
        print("Use 'list-templates' to see available templates")
        return 1
    
    print(f"Creating document with template: {args.template}")
    print(f"Description: {template.metadata.get('description', 'N/A')}")
    print()
    
    # Get required fields
    required_fields = template.get_required_fields()
    content = {}
    
    print("Please provide the following information:")
    title = input("Title: ").strip()
    
    for field in required_fields:
        if field == 'title':
            content['title'] = title
            continue
        
        value = input(f"{field}: ").strip()
        content[field] = value
    
    # Create document
    metadata = {}
    doc = Document(title, content, args.template, metadata)
    
    # Process and save
    try:
        formatted = processor.process(doc)
        output_path = processor.save_to_library(doc, args.library_dir)
        print(f"\nDocument created and saved to library: {output_path}")
        return 0
    except Exception as e:
        print(f"\nError creating document: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
