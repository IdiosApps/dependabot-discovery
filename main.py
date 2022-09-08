from github import Github
import os

access_token = os.getenv('DEPENDABOT_DISCOVERY_TOKEN')

# using an access token
g = Github(access_token)
# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

print(g.get_user().name)