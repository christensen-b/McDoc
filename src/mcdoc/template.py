"""
Template system for McDoc
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class Template:
    """Base template class for document formatting"""
    
    def __init__(self, name: str, template_path: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a template
        
        Args:
            name: Template name
            template_path: Path to template file
            metadata: Template metadata (author, version, description, etc.)
        """
        self.name = name
        self.template_path = template_path
        self.metadata = metadata or {}
        self.content = self._load_template()
    
    def _load_template(self) -> str:
        """Load template content from file"""
        if os.path.exists(self.template_path):
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def format(self, content: Dict[str, Any]) -> str:
        """
        Format template with provided content
        
        Args:
            content: Dictionary containing content to populate template
            
        Returns:
            Formatted document string
        """
        formatted = self.content
        for key, value in content.items():
            placeholder = f"{{{{{key}}}}}"
            formatted = formatted.replace(placeholder, str(value))
        return formatted
    
    def get_required_fields(self) -> List[str]:
        """
        Extract required fields from template
        
        Returns:
            List of required field names
        """
        pattern = r'\{\{([^}]+)\}\}'
        matches = re.findall(pattern, self.content)
        return list(set(matches))


class TemplateRegistry:
    """Registry for managing available templates"""
    
    def __init__(self, templates_dir: str):
        """
        Initialize template registry
        
        Args:
            templates_dir: Directory containing templates
        """
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, Template] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all templates from templates directory"""
        if not self.templates_dir.exists():
            return
        
        for template_file in self.templates_dir.glob("*.md"):
            # Check for metadata file
            metadata_file = template_file.with_suffix('.json')
            metadata = {}
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            
            template_name = template_file.stem
            template = Template(template_name, str(template_file), metadata)
            self.templates[template_name] = template
    
    def get_template(self, name: str) -> Optional[Template]:
        """
        Get template by name
        
        Args:
            name: Template name
            
        Returns:
            Template instance or None if not found
        """
        return self.templates.get(name)
    
    def list_templates(self) -> List[str]:
        """
        List all available templates
        
        Returns:
            List of template names
        """
        return list(self.templates.keys())
    
    def register_template(self, template: Template):
        """
        Register a new template
        
        Args:
            template: Template instance to register
        """
        self.templates[template.name] = template
