import pytest
import os
import json
from src.analyzer import Analyzer

@pytest.fixture
def setup_sample_project(tmpdir):
    """
    Sets up a sample project directory with files containing various tags.
    """
    project_dir = tmpdir.mkdir("sample_project")
    
    # Sample Python file
    sample_py = project_dir.join("sample.py")
    sample_py.write("""\
# sample.py

def add(a, b):
    # @TODO: Handle negative numbers
    return a + b

def subtract(a, b):
    \"\"\"
    @FIXME: Subtraction logic might be incorrect
    \"\"\"
    return a - b

def multiply(a, b):
    # Regular comment
    return a * b
""")
    
    # Sample JavaScript file
    sample_js = project_dir.join("sample.js")
    sample_js.write("""\
// sample.js

function multiply(a, b) {
    // @REFACTOR: Improve performance
    return a * b;
}

/*
@IMPROVE: Add error handling
*/
function divide(a, b) {
    return a / b;
}

function modulus(a, b) {
    return a % b;
}
""")
    
    # Sample Java file
    sample_java = project_dir.join("sample.java")
    sample_java.write("""\
// sample.java

public class Sample {
    // @BUG: NullPointerException might occur
    public int add(int a, int b) {
        return a + b;
    }

    /*
    @HACK: Temporary fix for performance issue
    */
    public void process() {
        // processing logic
    }

    public void noTagMethod() {
        // This method has no tags
    }
}
""")
    
    return project_dir.strpath

def test_tag_detection_basic(setup_sample_project, tmpdir):
    """
    Test that the Analyzer correctly detects and categorizes basic tags.
    """
    project_path = setup_sample_project
    output_path = os.path.join(tmpdir, "report.json")
    
    analyzer = Analyzer(project_path=project_path, tags=["@TODO", "@FIXME", "@REFACTOR", "@IMPROVE", "@BUG", "@HACK"])
    analyzer.analyze()
    comments = analyzer.get_comments()
    
    # Write report to a temporary file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4)
    
    # Load the report for assertions
    with open(output_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Expected tags and their counts
    expected_tags = {
        "@TODO": 1,
        "@FIXME": 1,
        "@REFACTOR": 1,
        "@IMPROVE": 1,
        "@BUG": 1,
        "@HACK": 1
    }
    
    # Initialize tag counts
    tag_counts = {tag: 0 for tag in expected_tags}
    
    for comment in report:
        for tag in comment['tags']:
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1  # Unexpected tags

    print(tag_counts)
    
    # Assert that each expected tag is detected exactly once
    for tag, count in expected_tags.items():
        assert tag_counts.get(tag, 0) == count, f"Expected {count} occurrences of {tag}, found {tag_counts.get(tag, 0)}"

def test_tag_detection_multiple_tags(setup_sample_project, tmpdir):
    """
    Test that the Analyzer correctly detects multiple tags within a single comment.
    """
    project_path = setup_sample_project
    output_path = os.path.join(tmpdir, "report.json")
    
    # Modify a file to include multiple tags in a single comment
    sample_py_path = os.path.join(project_path, "sample.py")
    with open(sample_py_path, 'a', encoding='utf-8') as f:
        f.write("\n    # @TODO: Implement feature X @FIXME: Bug in feature Y")
    
    analyzer = Analyzer(project_path=project_path, tags=["@TODO", "@FIXME", "@REFACTOR", "@IMPROVE", "@BUG", "@HACK"])
    analyzer.analyze()
    comments = analyzer.get_comments()
    
    # Write report to a temporary file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4)
    
    # Load the report for assertions
    with open(output_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Initialize tag counts
    tag_counts = {
        "@TODO": 0,      # Existing from Phase 1
        "@FIXME": 0,     # One from Phase 1 and one added now
        "@REFACTOR": 0,
        "@IMPROVE": 0,
        "@BUG": 0,
        "@HACK": 0
    }
    
    for comment in report:
        for tag in comment['tags']:
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1  # Unexpected tags

    print(tag_counts)
    
    # Adjust counts considering the new comment with two tags
    assert tag_counts["@TODO"] == 2, f"Expected 2 occurrences of @TODO, found {tag_counts['@TODO']}"
    assert tag_counts["@FIXME"] == 2, f"Expected 2 occurrences of @FIXME, found {tag_counts['@FIXME']}"

def test_tag_detection_unrecognized_tags(setup_sample_project, tmpdir):
    """
    Test that the Analyzer ignores unrecognized tags.
    """
    project_path = setup_sample_project
    output_path = os.path.join(tmpdir, "report.json")
    
    # Modify a file to include an unrecognized tag
    sample_js_path = os.path.join(project_path, "sample.js")
    with open(sample_js_path, 'a', encoding='utf-8') as f:
        f.write("\n    // @UNKNOWN: This is an unrecognized tag")
    
    analyzer = Analyzer(project_path=project_path, tags=["@TODO", "@FIXME", "@REFACTOR", "@IMPROVE", "@BUG", "@HACK"])
    analyzer.analyze()
    comments = analyzer.get_comments()
    
    # Write report to a temporary file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4)
    
    # Load the report for assertions
    with open(output_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Ensure that comments with unrecognized tags are not included
    for comment in report:
        for tag in comment['tags']:
            assert tag in ["@TODO", "@FIXME", "@REFACTOR", "@IMPROVE", "@BUG", "@HACK"], f"Unrecognized tag found: {tag}"

def test_tag_detection_case_sensitivity(setup_sample_project, tmpdir):
    """
    Test that the Analyzer correctly handles case sensitivity in tags.
    """
    project_path = setup_sample_project
    output_path = os.path.join(tmpdir, "report.json")
    
    # Modify a file to include tags with different cases
    sample_java_path = os.path.join(project_path, "sample.java")
    with open(sample_java_path, 'a', encoding='utf-8') as f:
        f.write("\n    // @todo: Lowercase tag\n    // @FixMe: Mixed case tag\n")
    
    analyzer = Analyzer(project_path=project_path, tags=["@TODO", "@FIXME", "@REFACTOR", "@IMPROVE", "@BUG", "@HACK"])
    analyzer.analyze()
    comments = analyzer.get_comments()
    
    # Write report to a temporary file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4)
    
    # Load the report for assertions
    with open(output_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Initialize tag counts
    tag_counts = {
        "@TODO": 1,      # Existing from Phase 1
        "@FIXME": 1,     # Existing from Phase 1
        "@REFACTOR": 1,
        "@IMPROVE": 1,
        "@BUG": 1,
        "@HACK": 1
    }
    
    # Since the new tags are in different cases, they should not be counted
    # Unless you decide to make tag detection case-insensitive
    for comment in report:
        for tag in comment['tags']:
            assert tag.isupper(), f"Tag with incorrect case detected: {tag}"
