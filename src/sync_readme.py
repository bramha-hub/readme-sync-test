"""
Main script for README synchronization.
"""
import os
import sys
import yaml
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from parsers import ParserFactory
from parsers.base import FileAnalysis
from prompt_builder import PromptBuilder
from llm_client import LLMClient


class ReadmeSync:
    """Main class for synchronizing README with code changes."""
    
    def __init__(self, config_path: str = "config.yml"):
        """Initialize the sync tool."""
        self.config = self._load_config(config_path)
        self.parser_factory = ParserFactory()
        self.prompt_builder = PromptBuilder(
            preserve_tone=self.config['update_rules']['preserve_tone'],
            preserve_style=self.config['update_rules']['preserve_style']
        )
        self.llm_client = LLMClient(
            model=self.config['llm']['model'],
            temperature=self.config['llm']['temperature'],
            max_tokens=self.config['llm']['max_tokens']
        )
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files from git."""
        try:
            # Get the diff between HEAD and previous commit
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            
            files = result.stdout.strip().split('\n')
            
            # Filter by monitored extensions
            monitored_extensions = tuple(self.config['monitored_extensions'])
            filtered_files = [
                f for f in files 
                if f.endswith(monitored_extensions) and self._should_include_file(f)
            ]
            
            return filtered_files
        
        except subprocess.CalledProcessError as e:
            print(f"Error getting changed files: {e}")
            return []
    
    def _should_include_file(self, filepath: str) -> bool:
        """Check if file should be included based on exclude patterns."""
        from fnmatch import fnmatch
        
        for pattern in self.config['exclude_patterns']:
            if fnmatch(filepath, pattern):
                return False
        return True
    
    def get_file_diff(self, filepath: str) -> str:
        """Get git diff for a specific file."""
        try:
            result = subprocess.run(
                ['git', 'diff', 'HEAD~1', 'HEAD', '--', filepath],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    def read_file(self, filepath: str) -> str:
        """Read file content."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""
    
    def parse_changed_files(self, filepaths: List[str]) -> List[FileAnalysis]:
        """Parse changed files to extract structure."""
        analyses = []
        
        for filepath in filepaths:
            content = self.read_file(filepath)
            if content:
                analysis = self.parser_factory.parse_file(filepath, content)
                if analysis:
                    analyses.append(analysis)
        
        return analyses
    
    def get_file_changes(self, filepaths: List[str]) -> List[Dict[str, str]]:
        """Get diffs for changed files."""
        changes = []
        
        for filepath in filepaths:
            diff = self.get_file_diff(filepath)
            if diff:
                changes.append({
                    'filepath': filepath,
                    'diff': diff
                })
        
        return changes
    
    def update_readme(self, new_content: str, readme_path: str = "README.md"):
        """Update README file with new content."""
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Updated {readme_path}")
        except Exception as e:
            print(f"Error updating {readme_path}: {e}")
    
    def run(self):
        """Main execution flow."""
        print("🔍 README-Sync: Analyzing code changes...")
        
        # Get changed files
        changed_files = self.get_changed_files()
        
        if not changed_files:
            print("ℹ️  No relevant code changes detected.")
            return
        
        print(f"📝 Found {len(changed_files)} changed file(s):")
        for f in changed_files:
            print(f"   - {f}")
        
        # Parse changed files
        print("\n🔬 Parsing code structure...")
        parsed_files = self.parse_changed_files(changed_files)
        
        # Get file diffs
        file_changes = self.get_file_changes(changed_files)
        
        # Process each documentation file
        for doc_file in self.config['documentation_files']:
            if not os.path.exists(doc_file):
                print(f"⚠️  Documentation file not found: {doc_file}")
                continue
            
            print(f"\n📖 Processing {doc_file}...")
            
            # Read current documentation
            current_content = self.read_file(doc_file)
            
            # Build prompt
            prompt = self.prompt_builder.build_update_prompt(
                current_readme=current_content,
                file_changes=file_changes,
                parsed_files=parsed_files
            )
            
            # Generate update
            print("🤖 Generating documentation update with AI...")
            try:
                response = self.llm_client.generate_documentation_update(prompt)
                new_content = self.llm_client.extract_markdown_content(response)
                
                if new_content is None:
                    print(f"✓ {doc_file} is already up-to-date")
                    continue
                
                # Update the file
                self.update_readme(new_content, doc_file)
                
            except Exception as e:
                print(f"❌ Error generating update: {e}")
                sys.exit(1)
        
        print("\n✅ README sync complete!")


def main():
    """Entry point."""
    try:
        sync = ReadmeSync()
        sync.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
