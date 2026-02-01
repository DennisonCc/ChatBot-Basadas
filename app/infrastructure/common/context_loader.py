import os
import re
from pathlib import Path

class MarkdownContextLoader:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.include_pattern = re.compile(r'\[include:\s*(.+?\.md)\s*\]')

    def load_context(self, filename: str = "main.md", visited=None) -> str:
        """
        Loads a markdown file and recursively resolves [include: file.md] directives.
        """
        if visited is None:
            visited = set()

        file_path = self.base_path / filename
        if not file_path.exists():
            return f"\n[Error: Archivo de contexto no encontrado: {filename}]\n"

        if file_path in visited:
            return f"\n[Error: Inclusión circular detectada en: {filename}]\n"

        visited.add(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        def replacer(match):
            include_file = match.group(1)
            return self.load_context(include_file, visited.copy())

        resolved_content = self.include_pattern.sub(replacer, content)
        return resolved_content

# Singleton instance
loader = MarkdownContextLoader(os.path.join(os.path.dirname(__file__), "../../../knowledge"))
