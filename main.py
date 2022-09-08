from github import Github
import os

from github.GithubException import UnknownObjectException

access_token = os.getenv('DEPENDABOT_DISCOVERY_TOKEN')

# using an access token
g = Github(access_token)
# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

print(g.get_user().name)

repoName = "danielt998/HanziToAnki"
repo = g.get_repo(repoName)
main_branch = repo.master_branch

try:
    workflows_dir = repo.get_contents(".github/workflows")
except UnknownObjectException:
    print(f".github workflows not found, nothing to do for repository {repoName}")
    exit()

try:
    dependabot_file = repo.get_contents(".github/dependabot.yml")
except UnknownObjectException:
    pass

if dependabot_file is not None:
    actions_ecosystem_phrase = "package-ecosystem: \"github-actions\"".encode()
    has_actions_updates = True if actions_ecosystem_phrase in dependabot_file.decoded_content else False


breakpoint()

# pr = repo.create_pull(title="Use 'requests' instead of 'httplib'", body='body', head="develop", base=main_branch)