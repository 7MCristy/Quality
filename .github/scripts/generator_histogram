import os
import requests
import matplotlib.pyplot as plt
import datetime

# Configuration from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")  # This env var is set by GitHub Actions

# If not running in Actions, allow fallback for local development
if not GITHUB_REPOSITORY:
    GITHUB_REPOSITORY = "ainhprzz/BetterHealthProject"  # Default value for local development
    print(f"Warning: GITHUB_REPOSITORY not found. Using default value: {GITHUB_REPOSITORY}")

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"

# Headers for GitHub API
headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"
    headers["Accept"] = "application/vnd.github.v3+json"
else:
    # We can still make some unauthenticated requests, with lower rate limits
    headers["Accept"] = "application/vnd.github.v3+json"
    print("Warning: No GITHUB_TOKEN provided. Using unauthenticated requests (limited rate).")

# Labels to track
devops_labels = [
    {"name": "Plan", "color": "0052cc", "description": "Planning phase tasks"},
    {"name": "Code", "color": "006b75", "description": "Coding phase tasks"},
    {"name": "Build", "color": "ff9f1c", "description": "Build phase tasks"},
    {"name": "Test", "color": "e99695", "description": "Testing phase tasks"},
    {"name": "Release", "color": "bfd4f2", "description": "Release phase tasks"},
    {"name": "Deploy", "color": "7057ff", "description": "Deployment phase tasks"},
    {"name": "Operate", "color": "008672", "description": "Operation phase tasks"},
    {"name": "Monitor", "color": "d73a4a", "description": "Monitoring phase tasks"},
]

# Additional labels to track
additional_labels = ["back-end", "bug", "database", "documentation", "front-end", "tests", "wontfix"]

def get_date() -> str:
    """Get current month formatted as 'MX' where X is the month number"""
    now = datetime.datetime.now()
    month = now.strftime("%m")
    return f"M{month}"

def create_devops_labels():
    """Create default DevOps labels if they don't exist"""
    for label in devops_labels:
        try:
            # Check if label exists
            response = requests.get(
                f"{GITHUB_API_URL}/labels/{label['name']}",
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"Label '{label['name']}' already exists.")
            elif response.status_code == 404:
                # Create the label
                response = requests.post(
                    f"{GITHUB_API_URL}/labels",
                    headers=headers,
                    json=label
                )
                
                if response.status_code == 201:
                    print(f"Label '{label['name']}' created successfully.")
                else:
                    print(f"Failed to create label '{label['name']}'. Status code: {response.status_code}")
                    print(f"Response: {response.text}")
            else:
                print(f"Error checking label '{label['name']}'. Status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error processing label '{label['name']}': {e}")

def count_labels(state="all"):
    """Count the number of issues with each label"""
    # Initialize counts dictionary with all labels set to 0
    labels_count = {}
    for label in devops_labels:
        labels_count[label["name"]] = 0
    
    for label in additional_labels:
        labels_count[label] = 0
    
    # Get all issues with the specified state
    try:
        page = 1
        per_page = 100
        more_issues = True
        
        while more_issues:
            response = requests.get(
                f"{GITHUB_API_URL}/issues",
                headers=headers,
                params={"state": state, "page": page, "per_page": per_page}
            )
            response.raise_for_status()
            
            issues = response.json()
            if not issues:
                more_issues = False
                break
                
            for issue in issues:
                # Skip pull requests (GitHub API returns PRs as issues)
                if "pull_request" in issue:
                    continue
                    
                for label in issue.get("labels", []):
                    label_name = label.get("name")
                    if label_name in labels_count:
                        labels_count[label_name] += 1
            
            page += 1
            
        return labels_count
        
    except Exception as e:
        print(f"Error fetching or processing issues: {e}")
        return labels_count

def generate_plot(labels_count):
    """Generate a histogram of the number of issues with each label"""
    plt.figure(figsize=(12, 8))
    
    # Get all labels with counts greater than 0
    active_labels = {k: v for k, v in labels_count.items() if v > 0}
    
    # If no active labels, use all labels
    if not active_labels:
        active_labels = labels_count
    
    # Sort by count for better visualization
    sorted_labels = dict(sorted(active_labels.items(), key=lambda item: item[1], reverse=True))
    
    # Create bar plot
    bars = plt.bar(sorted_labels.keys(), sorted_labels.values())
    
    # Add count labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.0f}', ha='center', va='bottom')
    
    plt.ylabel('Number of Issues')
    
    # Add date to title
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    plt.title(f'Ishikawa Histogram of Issues by Label - {current_date}')
    
    plt.xticks(rotation=45, ha='right')
    
    # Set y-axis to include all values plus some padding
    max_value = max(active_labels.values()) if active_labels else 0
    plt.yticks(range(0, max_value + 2 if max_value > 0 else 1))
    
    # Adjust layout
    plt.tight_layout()
    
    # Save with date in filename
    filename = f"generator_histogram_{get_date()}.png"
    plt.savefig(filename)
    print(f"Histogram saved as {filename}")
    return filename

def main():
    # First create the DevOps labels if they don't exist
    create_devops_labels()
    
    # Then count the issues with each label
    labels_count = count_labels()
    
    # Finally generate the plot
    generate_plot(labels_count)

if __name__ == '__main__':
    main()
