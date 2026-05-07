# Contributing to McDoc

Thank you for your interest in contributing to McDoc! This document provides guidelines for contributing to the enterprise IT documentation library.

## How to Contribute

### Types of Contributions

1. **New Templates** - Create templates for new document types
2. **Example Documents** - Add example documents demonstrating best practices
3. **Improvements** - Enhance existing templates and documentation
4. **Corrections** - Fix errors or unclear content
5. **Structure** - Suggest improvements to organization

### Contribution Process

1. **Identify Need**
   - Determine what needs to be added or improved
   - Check if similar content already exists
   - Ensure it aligns with enterprise IT needs

2. **Create Content**
   - Follow existing templates and style
   - Use clear, professional language
   - Include all required sections
   - Add examples where helpful

3. **Review**
   - Self-review for completeness and accuracy
   - Check formatting and links
   - Verify consistency with existing content

4. **Submit**
   - Create descriptive commit messages
   - Update relevant indexes
   - Document changes in revision history

## Documentation Standards

### Writing Style

- **Clear and Concise**: Use simple, direct language
- **Professional**: Maintain enterprise-appropriate tone
- **Consistent**: Follow existing patterns and terminology
- **Complete**: Include all necessary information
- **Accurate**: Verify technical accuracy

### Formatting

- **Markdown**: Use standard Markdown syntax
- **Headers**: Use hierarchical header structure (H1, H2, H3)
- **Lists**: Use bulleted or numbered lists appropriately
- **Tables**: Use tables for structured data
- **Code Blocks**: Use fenced code blocks with language specification
- **Links**: Use descriptive link text, verify links work

### Structure

- **Document Control**: Include metadata table
- **Table of Contents**: For longer documents
- **Sections**: Logical section organization
- **Cross-References**: Link to related documents
- **Revision History**: Track changes in revision table
- **Approval Section**: Include when appropriate

## Template Guidelines

### Creating Templates

Templates should include:
- Document control metadata section
- Clear purpose and scope
- Standard sections applicable to document type
- Example content showing how to use
- Placeholder text with instructions
- Revision history table
- Approval section where appropriate

### Template Sections

Required sections for all templates:
- Document Control (ID, version, owner, dates, status)
- Purpose
- Scope
- Main content sections
- Related Documentation
- Revision History

## File Organization

### Naming Conventions

- **Files**: Use lowercase with hyphens (e.g., `information-security-policy.md`)
- **Directories**: Use lowercase singular nouns (e.g., `policy`, `procedure`)
- **Templates**: Use UPPERCASE for templates (e.g., `POLICY_TEMPLATE.md`)

### Directory Structure

```
docs/
├── category/
│   ├── README.md          # Index and guidelines for category
│   ├── document-1.md      # Individual documents
│   └── document-2.md
└── templates/
    └── TEMPLATE_NAME.md   # Templates
```

### README Files

Each category should have a README.md containing:
- Category description
- Document index table
- Category guidelines
- How to use the category
- Related documentation links

## Quality Checklist

Before submitting, verify:

- [ ] Content is accurate and complete
- [ ] Follows existing template structure
- [ ] Uses consistent formatting
- [ ] All links work correctly
- [ ] Tables are properly formatted
- [ ] Code blocks have language specified
- [ ] Spelling and grammar are correct
- [ ] Document control section is complete
- [ ] Revision history is updated
- [ ] Related documentation is linked
- [ ] Index is updated (if applicable)

## Example Contributions

### Adding a New Policy

1. Copy `docs/templates/POLICY_TEMPLATE.md`
2. Save as `docs/policies/your-policy-name.md`
3. Fill in all sections
4. Update `docs/policies/README.md` index
5. Commit with message: "Add [Policy Name] policy"

### Adding a New Template

1. Create template in `docs/templates/`
2. Use UPPERCASE naming (e.g., `NEW_TEMPLATE.md`)
3. Include complete structure and examples
4. Document in `docs/README.md`
5. Commit with message: "Add template for [Document Type]"

### Improving Existing Content

1. Make targeted improvements
2. Update revision history
3. Verify no broken links or formatting
4. Commit with message: "Update [Document Name]: [brief description]"

## Commit Message Guidelines

Use clear, descriptive commit messages:

**Format**: `[Action] [Document/Area]: [Description]`

**Examples**:
- `Add password policy with MFA requirements`
- `Update POLICY_TEMPLATE: Add compliance section`
- `Fix broken links in security README`
- `Improve incident response procedure clarity`

**Actions**:
- `Add` - New content
- `Update` - Modify existing content
- `Fix` - Correct errors
- `Remove` - Delete obsolete content
- `Reorganize` - Restructure content

## Review Criteria

Contributions are evaluated on:

1. **Relevance**: Applicable to enterprise IT
2. **Quality**: Professional and accurate
3. **Completeness**: All necessary information included
4. **Consistency**: Matches existing style and structure
5. **Value**: Adds meaningful content or improvement

## Questions and Support

If you have questions:

1. Review existing documentation
2. Check similar examples
3. Review this contributing guide
4. Ask in your team channels

## Best Practices

### Do's
✅ Follow existing templates and patterns  
✅ Use professional, clear language  
✅ Include examples and explanations  
✅ Keep formatting consistent  
✅ Update indexes when adding content  
✅ Verify all links work  
✅ Test procedures before documenting  

### Don'ts
❌ Don't include sensitive or confidential information  
❌ Don't use unclear abbreviations without definitions  
❌ Don't break existing formatting or structure  
❌ Don't add content without proper review  
❌ Don't ignore template structure  
❌ Don't forget to update revision history  

## License and Usage

- Content should be appropriate for enterprise use
- Avoid including proprietary or confidential information
- Ensure compliance with your organization's policies
- Content should be generalizable for enterprise IT

## Versioning

- **Major Version** (X.0): Significant restructuring or additions
- **Minor Version** (1.X): New content or meaningful updates
- **Patch** (1.0.X): Corrections and minor improvements

Track version changes in document revision history.

## Thank You

Your contributions help build a comprehensive, high-quality documentation library for enterprise IT teams. Every improvement, no matter how small, adds value.

---

**Last Updated**: 2025-12-30  
**Version**: 1.0
