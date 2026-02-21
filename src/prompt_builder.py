"""
Prompt builder for generating structured prompts for the LLM.
"""
from typing import List, Dict
from parsers.base import FileAnalysis


class PromptBuilder:
    """Builds structured prompts for documentation updates."""
    
    def __init__(self, preserve_tone: bool = True, preserve_style: bool = True):
        self.preserve_tone = preserve_tone
        self.preserve_style = preserve_style
    
    def build_update_prompt(
        self,
        current_readme: str,
        file_changes: List[Dict[str, str]],
        parsed_files: List[FileAnalysis],
        current_time: str = ""
    ) -> str:
        """
        Build a prompt for updating documentation.
        
        Args:
            current_readme: Current README content
            file_changes: List of dicts with 'filepath' and 'diff' keys
            parsed_files: List of FileAnalysis objects
            
        Returns:
            Structured prompt string
        """
        prompt_parts = [
            self._get_system_instructions(),
            f"Current Time: {current_time}",
            self._get_current_readme_section(current_readme),
            self._get_code_changes_section(file_changes),
            self._get_parsed_structure_section(parsed_files),
            self._get_changelog_instructions(current_time),
            self._get_constraints_section(),
            self._get_output_instructions()
        ]
        
        return "\n\n".join(prompt_parts)
    
    def _get_system_instructions(self) -> str:
        """Get system-level instructions."""
        return """# Task: Update Technical Documentation

You are a technical documentation expert. Your task is to update the README.md file to accurately reflect recent code changes. Your goal is to provide clear, descriptive, and helpful documentation, not just a list of code changes."""
    
    def _get_current_readme_section(self, readme: str) -> str:
        """Format the current README section."""
        return f"""## Current README Content

```markdown
{readme}
```"""
    
    def _get_code_changes_section(self, file_changes: List[Dict[str, str]]) -> str:
        """Format the code changes section."""
        changes_text = "## Recent Code Changes\n\n"
        
        for change in file_changes:
            filepath = change['filepath']
            diff = change['diff']
            changes_text += f"### File: `{filepath}`\n\n```diff\n{diff}\n```\n\n"
        
        return changes_text
    
    def _get_parsed_structure_section(self, parsed_files: List[FileAnalysis]) -> str:
        """Format the parsed code structure section."""
        structure_text = "## Extracted Code Structure\n\n"
        structure_text += "The following information was extracted using AST parsing to ensure accuracy:\n\n"
        
        for analysis in parsed_files:
            structure_text += f"### File: `{analysis.filepath}` ({analysis.language})\n\n"
            
            # Add module docstring if present
            if analysis.module_docstring:
                structure_text += f"**Module Description:** {analysis.module_docstring}\n\n"
            
            # Add functions
            if analysis.functions:
                structure_text += "**Functions:**\n"
                for func in analysis.functions:
                    async_prefix = "async " if func.is_async else ""
                    params = ", ".join(func.parameters)
                    return_type = f" -> {func.return_type}" if func.return_type else ""
                    
                    structure_text += f"- `{async_prefix}{func.name}({params}){return_type}`"
                    
                    if func.docstring:
                        structure_text += f"\n  - Full Docstring:\n{func.docstring}"
                    
                    structure_text += "\n"
                structure_text += "\n"
            
            # Add classes
            if analysis.classes:
                structure_text += "**Classes:**\n"
                for cls in analysis.classes:
                    bases = f"({', '.join(cls.base_classes)})" if cls.base_classes else ""
                    structure_text += f"- `{cls.name}{bases}`"
                    
                    if cls.docstring:
                        structure_text += f"\n  - Full Docstring:\n{cls.docstring}"
                    
                    if cls.methods:
                        structure_text += "\n  - Methods: "
                        structure_text += ", ".join([f"`{m.name}`" for m in cls.methods])
                    
                    structure_text += "\n"
                structure_text += "\n"
        
        return structure_text
    
    def _get_changelog_instructions(self, current_time: str) -> str:
        """Get instructions for the changelog section."""
        return f"""## Changelog Instructions - CRITICAL: Preserve All History
        
**MANDATORY RULES FOR CHANGELOG:**
1.  **NEVER DELETE OR MODIFY existing changelog entries** - All previous entries must remain exactly as they are
2.  **Check for an existing 'Changelog', 'Recent Updates', 'History', or 'Version History' section**
3.  If a changelog section exists:
    - **Keep ALL previous entries completely intact** - do not edit, modify, or remove any existing entries
    - **Add a NEW entry at the TOP** of the changelog section with timestamp: **{current_time}**
    - List ONLY the new changes under this new timestamp entry
    - Maintain the same format and style as existing entries
4.  If no changelog section exists, create a new "## 📝 Changelog" section at the end of the README
5.  **Preserve all timestamps and dates** from previous entries - they are historical records
6.  Also ensure there is a descriptive 'Project Overview' or 'Description' section at the beginning. If not, create one based on the code analysis.

**REMEMBER**: The changelog is a historical record - never remove or alter past entries!
"""
    
    def _get_constraints_section(self) -> str:
        """Get constraints for the update."""
        constraints = ["## Constraints"]
        
        if self.preserve_tone:
            constraints.append("- **Preserve the original tone and voice** of the documentation")
        
        if self.preserve_style:
            constraints.append("- **Maintain the existing structure and style** (headings, formatting, etc.)")
        
        constraints.extend([
            "- **CRITICAL: Preserve ALL existing README content** - Never delete or remove any existing sections, paragraphs, or content",
            "- **Only ADD or UPDATE content** - Never remove historical information, changelog entries, or previous documentation",
            "- **Update technical details comprehensively**, providing clear descriptions of purpose and usage",
            "- **Include parameter descriptions, return values, and examples** where available",
            "- **Add new sections** if necessary to fully document new features",
            "- **Do not remove sections** unless the functionality has been completely removed (and even then, mark as deprecated rather than removing)",
            "- **Be descriptive and detailed** - generate high-quality, comprehensive documentation",
            "- **Highlight breaking changes** if function signatures or behavior have changed significantly",
            "- **Maintain chronological order** in changelog sections - newest entries at top, oldest at bottom",
            "- **Preserve all formatting, emojis, and styling** from the original README"
        ])
        
        return "\n".join(constraints)
    
    def _get_output_instructions(self) -> str:
        """Get output format instructions."""
        return """## Output Instructions

Provide the updated README.md content in full. Use the following format:

```markdown
[Your updated README content here]
```

If no changes are needed, respond with: "NO_CHANGES_NEEDED"
"""
