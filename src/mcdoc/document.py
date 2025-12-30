"""
Document management for McDoc
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class Document:
    """Represents a document in the McDoc system"""
    
    def __init__(self, title: str, content: Dict[str, Any], template_name: str, 
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a document
        
        Args:
            title: Document title
            content: Document content as key-value pairs
            template_name: Name of template to use
            metadata: Additional metadata
        """
        self.title = title
        self.content = content
        self.template_name = template_name
        self.metadata = metadata or {}
        self.metadata['created_at'] = self.metadata.get('created_at', 
                                                         datetime.now().isoformat())
        self.formatted_content: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary"""
        return {
            'title': self.title,
            'content': self.content,
            'template_name': self.template_name,
            'metadata': self.metadata,
            'formatted_content': self.formatted_content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """Create document from dictionary"""
        doc = cls(
            title=data['title'],
            content=data['content'],
            template_name=data['template_name'],
            metadata=data.get('metadata', {})
        )
        doc.formatted_content = data.get('formatted_content')
        return doc
    
    def save_to_file(self, filepath: str):
        """Save document to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Document':
        """Load document from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


class DocumentProcessor:
    """Process documents using templates"""
    
    def __init__(self, template_registry):
        """
        Initialize document processor
        
        Args:
            template_registry: TemplateRegistry instance
        """
        self.template_registry = template_registry
    
    def process(self, document: Document) -> str:
        """
        Process document with its template
        
        Args:
            document: Document to process
            
        Returns:
            Formatted document content
            
        Raises:
            ValueError: If template not found
        """
        template = self.template_registry.get_template(document.template_name)
        if not template:
            raise ValueError(f"Template '{document.template_name}' not found")
        
        # Merge document content with metadata for template population
        template_data = {**document.content}
        template_data['title'] = document.title
        template_data.update(document.metadata)
        
        # Format the template
        formatted = template.format(template_data)
        document.formatted_content = formatted
        return formatted
    
    def save_to_library(self, document: Document, library_dir: str) -> str:
        """
        Save processed document to library
        
        Args:
            document: Document to save
            library_dir: Library directory path
            
        Returns:
            Path to saved document
        """
        library_path = Path(library_dir)
        library_path.mkdir(parents=True, exist_ok=True)
        
        # Create safe filename from title
        safe_title = "".join(c for c in document.title if c.isalnum() or c in (' ', '-', '_'))
        safe_title = safe_title.replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save formatted content
        output_filename = f"{safe_title}_{timestamp}.md"
        output_path = library_path / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(document.formatted_content or "")
        
        # Save document metadata
        meta_filename = f"{safe_title}_{timestamp}.json"
        meta_path = library_path / meta_filename
        document.save_to_file(str(meta_path))
        
        return str(output_path)
