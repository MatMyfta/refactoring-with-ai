# src/parser.py

import re
from abc import ABC, abstractmethod
from typing import List

# Abstract Base Class for Parsers
class Parser(ABC):
    @abstractmethod
    def parse(self, file_content: str) -> List[str]:
        """Parse the file content and return a list of comments."""
        pass

# Concrete Parser for Python
class PythonParser(Parser):
    SINGLE_LINE_COMMENT_PATTERN = re.compile(r'#\s*(.*)')
    MULTI_LINE_COMMENT_PATTERN = re.compile(r'"""([\s\S]*?)"""', re.MULTILINE)

    def parse(self, file_content: str) -> List[str]:
        comments = []
        # Extract single-line comments
        single_comments = self.SINGLE_LINE_COMMENT_PATTERN.findall(file_content)
        comments.extend(single_comments)

        # Extract multi-line comments
        multi_comments = self.MULTI_LINE_COMMENT_PATTERN.findall(file_content)
        for comment in multi_comments:
            # Split multi-line comments into individual lines
            for line in comment.strip().split('\n'):
                comments.append(line.strip())
        
        return comments

# Concrete Parser for JavaScript
class JSParser(Parser):
    SINGLE_LINE_COMMENT_PATTERN = re.compile(r'//\s*(.*)')
    MULTI_LINE_COMMENT_PATTERN = re.compile(r'/\*([\s\S]*?)\*/', re.MULTILINE)

    def parse(self, file_content: str) -> List[str]:
        comments = []
        # Extract single-line comments
        single_comments = self.SINGLE_LINE_COMMENT_PATTERN.findall(file_content)
        comments.extend(single_comments)

        # Extract multi-line comments
        multi_comments = self.MULTI_LINE_COMMENT_PATTERN.findall(file_content)
        for comment in multi_comments:
            # Split multi-line comments into individual lines
            for line in comment.strip().split('\n'):
                comments.append(line.strip())
        
        return comments
    
# Concrete Parser for Java
class JavaParser(Parser):
    SINGLE_LINE_COMMENT_PATTERN = re.compile(r'//\s*(.*)')
    MULTI_LINE_COMMENT_PATTERN = re.compile(r'/\*([\s\S]*?)\*/', re.MULTILINE)

    def parse(self, file_content: str) -> List[str]:
        comments = []
        # Extract single-line comments
        single_comments = self.SINGLE_LINE_COMMENT_PATTERN.findall(file_content)
        comments.extend(single_comments)

        # Extract multi-line comments
        multi_comments = self.MULTI_LINE_COMMENT_PATTERN.findall(file_content)
        for comment in multi_comments:
            # Split multi-line comments into individual lines
            for line in comment.strip().split('\n'):
                comments.append(line.strip())
        
        return comments

# Factory to get the appropriate parser based on file extension
class ParserFactory:
    @staticmethod
    def get_parser(file_extension: str) -> Parser:
        if file_extension == '.py':
            return PythonParser()
        elif file_extension in ['.js', '.jsx', '.ts', '.tsx']:
            return JSParser()
        else:
            raise ValueError(f"No parser available for the extension: {file_extension}")
