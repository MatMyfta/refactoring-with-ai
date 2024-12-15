import pytest
from src.parser import ParserFactory
from src.parser import PythonParser, JSParser, JavaParser

def test_parse_single_line_comments_python():
    parser = PythonParser()
    file_content = """\
def foo():
    # @TODO: fix this
    return 42
"""
    comments = parser.parse(file_content)
    assert len(comments) > 0, "Expected at least one comment"
    assert "@TODO" in comments[0], "Expected '@TODO' in the first comment"

def test_parse_single_line_comments_js():
    parser = JSParser()
    file_content = """\
 // @FIXME: check boundary conditions
function bar() { return 0; }
"""
    comments = parser.parse(file_content)
    assert len(comments) > 0, "Expected at least one comment"
    assert "@FIXME" in comments[0], "Expected '@FIXME' in the first comment"

def test_parse_multi_line_comments_python():
    parser = PythonParser()
    file_content = '''\
"""
@OPTIMIZE: This function is too slow
"""
def baz():
    return "ok"
'''
    comments = parser.parse(file_content)
    assert len(comments) == 1, "Expected exactly one multi-line comment block"
    assert "@OPTIMIZE" in comments[0], "Expected '@OPTIMIZE' in multi-line comment"

def test_parse_multi_line_comments_js():
    parser = JSParser()
    file_content = """\
/*
@IMPROVE: refactor this code
*/
function qux() { return 1; }
"""
    comments = parser.parse(file_content)
    assert len(comments) == 1, "Expected exactly one multi-line comment block"
    assert "@IMPROVE" in comments[0], "Expected '@IMPROVE' in multi-line comment"

def test_parse_single_line_comments_java():
    parser = JavaParser()
    file_content = """\
// @BUG: NullPointerException might occur
public int add(int a, int b) {
    return a + b;
}
"""
    comments = parser.parse(file_content)
    assert len(comments) > 0, "Expected at least one comment"
    assert "@BUG" in comments[0], "Expected '@BUG' in the first comment"

def test_parse_multi_line_comments_java():
    parser = JavaParser()
    file_content = """\
/*
@HACK: Temporary fix for performance issue
*/
public void process() {
}
"""
    comments = parser.parse(file_content)
    assert len(comments) == 1, "Expected exactly one multi-line comment block"
    assert "@HACK" in comments[0], "Expected '@HACK' in multi-line comment"

def test_no_comments_python():
    parser = PythonParser()
    file_content = """\
def noComment():
    return True
"""
    comments = parser.parse(file_content)
    assert len(comments) == 0, "Expected no comments for a comment-free file"

def test_no_comments_js():
    parser = JSParser()
    file_content = """\
function noComment() { return true; }
"""
    comments = parser.parse(file_content)
    assert len(comments) == 0, "Expected no comments for a comment-free file"

def test_no_comments_java():
    parser = JavaParser()
    file_content = """\
public class NoComment {
    public static void main(String[] args) {
        System.out.println("No comments here!");
    }
}
"""
    comments = parser.parse(file_content)
    assert len(comments) == 0, "Expected no comments for a comment-free file"

def test_mixed_comments():
    # Correcting the typo from @REFATOR to @REFACTOR
    parser_python = PythonParser()
    parser_js = JSParser()
    parser_java = JavaParser()

    python_content = """\
# @TODO: fix logic
"""
    js_content = """\
/*
@DEPRECATE: remove this feature next release
*/
"""
    java_content = """\
// @BUG: fix this bug
"""
    python_content_refactor = """\
# @REFACTOR: python style comment
"""

    comments = []
    comments.extend(parser_python.parse(python_content))
    comments.extend(parser_js.parse(js_content))
    comments.extend(parser_java.parse(java_content))
    comments.extend(parser_python.parse(python_content_refactor))

    # Filter comments containing tags
    tags = ['@TODO', '@FIXME', '@REFACTOR', '@OPTIMIZE', '@IMPROVE', '@DEPRECATE', '@REMOVE', '@BUG', '@HACK']
    tagged_comments = [comment for comment in comments if any(tag in comment for tag in tags)]

    assert len(tagged_comments) == 4, f"Expected 4 comments, got {len(tagged_comments)}"
    assert "@TODO" in tagged_comments[0], "Expected '@TODO' in the first comment"
    assert "@DEPRECATE" in tagged_comments[1], "Expected '@DEPRECATE' in the second comment"
    assert "@BUG" in tagged_comments[2], "Expected '@BUG' in the third comment"
    assert "@REFACTOR" in tagged_comments[3], "Expected '@REFACTOR' in the fourth comment"
