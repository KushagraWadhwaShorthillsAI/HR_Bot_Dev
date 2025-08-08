#!/usr/bin/env python3
"""
Unified Resume Retailor Tester

Usage:
    python unified_resume_retailor.py <mode>

Arguments:
    <mode> : 'jd' for retailor with job description, 'nojd' for retailor without job description

Example:
    python unified_resume_retailor.py jd
    python unified_resume_retailor.py nojd
"""
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load .env file from current directory
load_dotenv()

# Import retailor classes from existing scripts
from execute_stream_custom_files.retailor_resume_jd import ResumeRetailorWithJD
from execute_stream_custom_files.retailor_resume_nojd import ResumeRetailorNoJD
from docx_utils import DocxUtils

# Hardcoded file path
RESUME_JSON_PATH = ""


def generate_docx_file(retailored_resume, mode, original_filename):
    """
    Generate a DOCX file from the retailored resume data
    """
    try:
        # Create a timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Extract base filename without extension
        base_filename = os.path.splitext(os.path.basename(original_filename))[0]
        
        # Create output filename
        output_filename = f"{base_filename}_retailored_{mode}_{timestamp}.docx"
        
        # Generate DOCX using DocxUtils
        docx_stream = DocxUtils.generate_docx(retailored_resume)
        
        # Save the DOCX file
        with open(output_filename, 'wb') as f:
            f.write(docx_stream.read())
        
        print(f"\n✅ DOCX file generated successfully: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"\n❌ Error generating DOCX file: {str(e)}")
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python unified_resume_retailor.py <mode>")
        print("mode: 'jd' for retailor with job description, 'nojd' for retailor without job description")
        print("\nExamples:")
        print("  python unified_resume_retailor.py jd")
        print("  python unified_resume_retailor.py nojd")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if not os.path.isfile(RESUME_JSON_PATH):
        print(f"Error: File not found: {RESUME_JSON_PATH}")
        sys.exit(1)

    try:
        with open(RESUME_JSON_PATH, 'r') as f:
            resume_data = json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
        sys.exit(1)

    # Handle keywords for 'jd' mode
    if mode == 'jd':
        # Use hardcoded keywords for Software Engineer
        keywords = ["software development", "programming", "technology","python","java","javascript","react","node.js","aws","docker","kubernetes","sql","mongodb","postgresql","machine learning","ai","data science","api","rest","graphql","microservices","agile","scrum","git","devops","ci/cd","testing","frontend","backend","full stack","flask","django","azure","gcp"]
        
        # Add keywords to resume data
        resume_data['keywords'] = keywords
        
        print(f"\n🔑 Using Keywords: {', '.join(keywords)}")

    azure_config = {
        "api_key": "",
        "api_version": "2024-08-01-preview",
        "endpoint":"https://us-tax-law-rag-demo.openai.azure.com/",
        "deployment": "gpt-4o-mini"
    }

    retailored_resume = None

    if mode == 'jd':
        retailor = ResumeRetailorWithJD(azure_config)
        try:
            retailored_resume = retailor.retailor_resume_with_jd(resume_data)
            print("\n=== RETAILORED RESUME JSON OUTPUT ===")
            print(json.dumps(retailored_resume, indent=2))
        except Exception as e:
            print(json.dumps({"error": f"Failed to retailor resume with JD: {str(e)}"}))
            sys.exit(1)
    elif mode == 'nojd':
        retailor = ResumeRetailorNoJD(azure_config)
        try:
            retailored_resume = retailor.retailor_resume_no_jd(resume_data)
            print("\n=== RETAILORED RESUME JSON OUTPUT ===")
            print(json.dumps(retailored_resume, indent=2))
        except Exception as e:
            print(json.dumps({"error": f"Failed to retailor resume without JD: {str(e)}"}))
            sys.exit(1)
    else:
        print("Invalid mode. Use 'jd' or 'nojd'.")
        sys.exit(1)

    # Generate DOCX file if retailoring was successful
    if retailored_resume and not isinstance(retailored_resume, dict) or "error" not in retailored_resume:
        print("\n=== GENERATING DOCX FILE ===")
        docx_filename = generate_docx_file(retailored_resume, mode, RESUME_JSON_PATH)
        if docx_filename:
            print(f"📄 DOCX file saved as: {docx_filename}")
        else:
            print("❌ Failed to generate DOCX file")
    else:
        print("❌ Cannot generate DOCX file due to retailoring errors")

if __name__ == "__main__":
    main()
