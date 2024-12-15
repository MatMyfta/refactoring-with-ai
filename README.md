# Project Comment Analyzer

## Overview

A Dockerized Python application to analyze code comments across multiple languages (Python, JavaScript, Java), detect specific tags, extract context, and generate comprehensive reports.

## Features

- **Multi-Language Support:** Python, JavaScript, Java
- **Tag Detection:** `@TODO`, `@FIXME`, `@REFACTOR`, `@IMPROVE`, `@OPTIMIZE`, `@DEPRECATE`, `@REMOVE`, `@BUG`, `@HACK`
- **Context Extraction:** Surrounding code context for each tagged comment
- **Reporting:** JSON reports with detailed information
- **Test-Driven Development (TDD):** Comprehensive test suite using pytest
- **Dockerized Environment:** Consistent setup across different environments

## Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine
- [Make](https://www.gnu.org/software/make/) installed (optional, for using the Makefile)
