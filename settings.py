"""
Settings file for git-to-s3
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# The temporary directory the git repository will be cloned to locally
TEMP_DIRECTORY = os.path.join(BASE_DIR, 'git_to_s3_temp')

GIT_URL = 'your_git_repository_url.git'

AWS_STORAGE_BUCKET_NAME = 'your_aws_bucket_name'
