#!/bin/sh

coverage run -m pytest tests/test_assessment.py
coverage report -m