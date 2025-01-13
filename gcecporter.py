import random
import time
import re
import gitlab
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import random
from prometheus_client import start_http_server, Gauge

# Configuration
group_name = 'impressico2'
gitlab_server = 'https://gitlab.com/'
auth_token = 'glpat-XXXXXXXXXXXXyvEA'

# Initialize GitLab client
gl = gitlab.Gitlab(url=gitlab_server, private_token=auth_token)

# Try to retrieve the group
try:
    group = gl.groups.get(group_name)
    print(f"Successfully retrieved group: {group.name}")
except gitlab.exceptions.GitlabGetError as e:
    print(f"Error retrieving group: {e}")
    exit(1)

# Retrieve project
project_id = 66085228  # Replace with your project ID
try:
    project = gl.projects.get(project_id)
    print(f"Successfully retrieved project: {project.name}")
except gitlab.exceptions.GitlabGetError as e:
    print(f"Error retrieving project: {e}")
    exit(1)

# Define Prometheus metric
gitlab_branch_count = Gauge('gitlab_branch_count', "Number of Branch Count")

# Function to get metrics
def get_metrics():
    gitlab_branch_count.set(len(project.branches.list()))
    branch_count = len(project.branches.list())
    print(f"Branch count: {branch_count}")  
    gitlab_branch_count.set(branch_count)

# Main loop
if __name__ == '__main__':
    start_http_server(8500)
    while True:
        get_metrics()
        time.sleep(3600)  # Run every 1 hr

