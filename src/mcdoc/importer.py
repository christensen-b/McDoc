"""
Document importer for McDoc
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from .document import Document


class DocumentImporter:
    """Import user-created documents into McDoc system"""
    
    def __init__(self):
        """Initialize document importer"""
        pass
    
    def import_from_json(self, filepath: str) -> Document:
        """
        Import document from JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Document instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract required fields
        title = data.get('title', 'Untitled')
        template_name = data.get('template', 'basic')
        content = data.get('content', {})
        metadata = data.get('metadata', {})
        
        return Document(title, content, template_name, metadata)
    
    def import_from_markdown(self, filepath: str, template_name: str = 'basic',
                           metadata: Optional[Dict[str, Any]] = None) -> Document:
        """
        Import document from Markdown file
        
        Args:
            filepath: Path to Markdown file
            template_name: Template to use for the document
            metadata: Optional metadata
            
        Returns:
            Document instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Extract title from first heading or filename
        title = Path(filepath).stem
        lines = md_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Parse frontmatter if exists
        content_metadata = metadata or {}
        content_body = md_content
        
        if md_content.startswith('---'):
            parts = md_content.split('---', 2)
            if len(parts) >= 3:
                import yaml
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    if isinstance(frontmatter, dict):
                        content_metadata.update(frontmatter)
                    content_body = parts[2].strip()
                except:
                    pass
        
        content = {
            'body': content_body,
            'source_file': filepath
        }
        
        return Document(title, content, template_name, content_metadata)
    
    def import_from_text(self, filepath: str, title: Optional[str] = None,
                        template_name: str = 'basic',
                        metadata: Optional[Dict[str, Any]] = None) -> Document:
        """
        Import document from plain text file
        
        Args:
            filepath: Path to text file
            title: Document title (uses filename if not provided)
            template_name: Template to use
            metadata: Optional metadata
            
        Returns:
            Document instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        doc_title = title or Path(filepath).stem
        content = {
            'body': text_content,
            'source_file': filepath
        }
        
        return Document(doc_title, content, template_name, metadata or {})
    
    def import_document(self, filepath: str, template_name: Optional[str] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> Document:
        """
        Import document auto-detecting format
        
        Args:
            filepath: Path to document file
            template_name: Template to use (auto-detect if not provided)
            metadata: Optional metadata
            
        Returns:
            Document instance
        """
        ext = Path(filepath).suffix.lower()
        
        if ext == '.json':
            return self.import_from_json(filepath)
        elif ext in ['.md', '.markdown']:
            return self.import_from_markdown(filepath, template_name or 'basic', metadata)
        else:
            return self.import_from_text(filepath, template_name=template_name or 'basic',
                                        metadata=metadata)
