# src/analyzer.py

import os
from typing import List, Dict
from src.parser import ParserFactory

# Data structure to hold extracted comments
class Comment:
    def __init__(self, file: str, line_number: int, text: str, context: List[str]):
        self.file = file
        self.line_number = line_number
        self.text = text
        self.context = context

    def to_dict(self) -> Dict:
        return {
            "file": self.file,
            "line_number": self.line_number,
            "text": self.text,
            "context": self.context
        }

class Analyzer:
    def __init__(self, project_path: str, tags: List[str]):
        self.project_path = project_path
        self.tags = tags
        self.comments: List[Comment] = []

    def analyze(self):
        for root, _, files in os.walk(self.project_path):
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                try:
                    parser = ParserFactory.get_parser(ext)
                except ValueError:
                    continue  # Skip files without a suitable parser
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                comments = parser.parse(content)
                self._extract_comments(file_path, comments)

    def _extract_comments(self, file_path: str, comments: List[str]):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for comment in comments:
            if any(tag in comment for tag in self.tags):
                # Find the line number of the comment
                for i, line in enumerate(lines):
                    if comment in line:
                        context = self._get_context(lines, i)
                        self.comments.append(Comment(
                            file=file_path,
                            line_number=i + 1,
                            text=comment,
                            context=context
                        ))
                        break

    def _get_context(self, lines: List[str], index: int, context_range: int = 2) -> List[str]:
        start = max(index - context_range, 0)
        end = min(index + context_range + 1, len(lines))
        return [line.strip() for line in lines[start:end]]

    def get_comments(self) -> List[Dict]:
        return [comment.to_dict() for comment in self.comments]