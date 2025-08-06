#!/usr/bin/env python3
"""
Unified Resume Retailor Tester

Usage:
    python unified_resume_retailor.py <resume_json_path> <mode>

Arguments:
    <resume_json_path> : Path to the input resume JSON file
    <mode>             : 'jd' for retailor with job description, 'nojd' for retailor without job description

Example:
    python unified_resume_retailor.py ./sample_resume.json jd
    python unified_resume_retailor.py ./sample_resume.json nojd
"""
import sys
import os
import json
from dotenv import load_dotenv

# Load .env file from current directory
load_dotenv()

# Import retailor classes from existing scripts
from execute_stream_custom_files.retailor_resume_jd import ResumeRetailorWithJD
from execute_stream_custom_files.retailor_resume_nojd import ResumeRetailorNoJD


def main():
    if len(sys.argv) != 3:
        print("Usage: python unified_resume_retailor.py <resume_json_path> <mode>")
        print("mode: 'jd' for retailor with job description, 'nojd' for retailor without job description")
        sys.exit(1)

    resume_json_path = sys.argv[1]
    mode = sys.argv[2].lower()

    if not os.path.isfile(resume_json_path):
        print(f"Error: File not found: {resume_json_path}")
        sys.exit(1)

    try:
        with open(resume_json_path, 'r') as f:
            resume_data = json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
        sys.exit(1)


    azure_config = {
                "api_key": "",
                "api_version": "2024-08-01-preview",
                "endpoint":"https://us-tax-law-rag-demo.openai.azure.com/",
                "deployment": "gpt-4o-mini"
            }

    if mode == 'jd':
        retailor = ResumeRetailorWithJD(azure_config)
        try:
            retailored_resume = retailor.retailor_resume_with_jd(resume_data)
            print(json.dumps(retailored_resume, indent=2))
        except Exception as e:
            print(json.dumps({"error": f"Failed to retailor resume with JD: {str(e)}"}))
    elif mode == 'nojd':
        retailor = ResumeRetailorNoJD(azure_config)
        try:
            retailored_resume = retailor.retailor_resume_no_jd(resume_data)
            print(json.dumps(retailored_resume, indent=2))
        except Exception as e:
            print(json.dumps({"error": f"Failed to retailor resume without JD: {str(e)}"}))
    else:
        print("Invalid mode. Use 'jd' or 'nojd'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
