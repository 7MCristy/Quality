import os
 import requests
 from datetime import datetime, timedelta
 import calendar
 import yaml
 from datetime import datetime, timedelta
 import json
 import sys
 
 # Configuration from environment variables
 GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
 GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")  # This env var is set by GitHub Actions
 
 def get_devops_phases():
     """Obtener las fases predeterminadas de DevOps"""
     # Usar un conjunto predeterminado de fases DevOps
     devops_phases = [
         "Plan", "Code", "Build", "Test",
         "Release", "Deploy", "Operate", "Monitor"
     ]
 # If not running in Actions, allow fallback for local development
 if not GITHUB_REPOSITORY:
     GITHUB_REPOSITORY = "usuario/repositorio"  # Only used if not running in GitHub Actions
     print("Warning: GITHUB_REPOSITORY not found. Using default value for local development.")
 
     return devops_phases
 GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"
 
 # Headers for GitHub API
 headers = {}
 if GITHUB_TOKEN:
     headers["Authorization"] = f"token {GITHUB_TOKEN}"
     headers["Accept"] = "application/vnd.github.v4+json"
 else:
     # We can still make some unauthenticated requests, with lower rate limits
     headers["Accept"] = "application/vnd.github.v4+json"
     print("Warning: No GITHUB_TOKEN provided. Using unauthenticated requests (limited rate).")
 
 
 def get_devops_phases():
     """Get DevOps phases from GitHub labels"""
     try:
         response = requests.get(f"{GITHUB_API_URL}/labels", headers=headers)
         response.raise_for_status()
 
         # Filter only DevOps-related labels
         all_labels = response.json()
         devops_labels = [label["name"] for label in all_labels if "devops" in label["name"].lower()]
 
         # If no specific DevOps labels, use default set
         if not devops_labels:
             devops_labels = [
                 "Plan", "Code", "Build", "Test",
                 "Release", "Deploy", "Operate", "Monitor"
             ]
 
         return devops_labels
     except Exception as e:
         print(f"Error fetching GitHub labels: {e}")
         # Return default phases in case of error
         return [
             "Plan", "Code", "Build", "Test",
             "Release", "Deploy", "Operate", "Monitor"
         ]
 
 
 def get_completed_issues_by_week(phase, start_date, end_date):
     """Get completed issues for a phase in date range"""
     try:
         # Format dates for GitHub API
         start_date_str = start_date.strftime('%Y-%m-%d')
         end_date_str = end_date.strftime('%Y-%m-%d')
 
         # Query closed issues with specific label in date range
         query = f"repo:{GITHUB_REPOSITORY} label:\"{phase}\" closed:{start_date_str}..{end_date_str}"
         response = requests.get(
             "https://api.github.com/search/issues",
             headers=headers,
             params={"q": query}
         )
         response.raise_for_status()
 
         return response.json()["total_count"]
     except Exception as e:
         print(f"Error fetching issues for {phase}: {e}")
         return 0
