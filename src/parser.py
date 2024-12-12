import re
from abc import ABC, abstractmethod
from typing import List

# Abstract Base Class for Parsers
class Parser(ABC):
    """
    Abstract base class for parsers. Implements the Template Method pattern.
    """

    def parse(self, file_content: str) -> List[str]:
        """
        Template method for parsing file content. Extracts single-line and multi-line comments.
        """
        comments = []
        # Extract single-line comments
        single_comments = self.extract_single_line_comments(file_content)
        comments.extend(single_comments)

        # Extract multi-line comments
        multi_comments = self.extract_multi_line_comments(file_content)
        for comment in multi_comments:
            # Split multi-line comments into individual lines
            for line in comment.strip().split('\n'):
                comments.append(line.strip())

        return comments

    @abstractmethod
    def extract_single_line_comments(self, file_content: str) -> List[str]:
        """
        Extract single-line comments based on the language-specific pattern.
        """
        pass

    @abstractmethod
    def extract_multi_line_comments(self, file_content: str) -> List[str]:
        """
        Extract multi-line comments based on the language-specific pattern.
        """
        pass


# Concrete Parser for Python
class PythonParser(Parser):
    SINGLE_LINE_COMMENT_PATTERN = re.compile(r'#\s*(.*)')
    MULTI_LINE_COMMENT_PATTERN = re.compile(r'"""([\s\S]*?)"""', re.MULTILINE)

    def extract_single_line_comments(self, file_content: str) -> List[str]:
        return self.SINGLE_LINE_COMMENT_PATTERN.findall(file_content)

    def extract_multi_line_comments(self, file_content: str) -> List[str]:
        return self.MULTI_LINE_COMMENT_PATTERN.findall(file_content)


# Concrete Parser for JavaScript
class JSParser(Parser):
    SINGLE_LINE_COMMENT_PATTERN = re.compile(r'//\s*(.*)')
    MULTI_LINE_COMMENT_PATTERN = re.compile(r'/\*([\s\S]*?)\*/', re.MULTILINE)

    def extract_single_line_comments(self, file_content: str) -> List[str]:
        return self.SINGLE_LINE_COMMENT_PATTERN.findall(file_content)

    def extract_multi_line_comments(self, file_content: str) -> List[str]:
        return self.MULTI_LINE_COMMENT_PATTERN.findall(file_content)


# Concrete Parser for Java
class JavaParser(Parser):
    SINGLE_LINE_COMMENT_PATTERN = re.compile(r'//\s*(.*)')
    MULTI_LINE_COMMENT_PATTERN = re.compile(r'/\*([\s\S]*?)\*/', re.MULTILINE)

    def extract_single_line_comments(self, file_content: str) -> List[str]:
        return self.SINGLE_LINE_COMMENT_PATTERN.findall(file_content)

    def extract_multi_line_comments(self, file_content: str) -> List[str]:
        return self.MULTI_LINE_COMMENT_PATTERN.findall(file_content)


# Factory to get the appropriate parser based on file extension
class ParserFactory:
    @staticmethod
    def get_parser(file_extension: str) -> Parser:
        if file_extension == '.py':
            return PythonParser()
        elif file_extension in ['.js', '.jsx', '.ts', '.tsx']:
            return JSParser()
        elif file_extension in ['.java']:
            return JavaParser()
        else:
            raise ValueError(f"No parser available for the extension: {file_extension}")
