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
main_branch_name = repo.default_branch
main_branch = repo.get_branch(main_branch_name)
target_branch = "dependabot_github_actions"

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

# if has_actions_updates:
#     print(f"Repository already has dependabot updates for GitHub Actions")
#     exit()

message = "Add dependabot updates for dependencies in GitHub Actions workflows"
dependabot_header = """version: 2
updates:"""
dependabot_body = """
  - package-ecosystem: "github-actions"
    directory: \"/\"
    schedule:
      interval: \"weekly\""""

print(f"Creating remote branch {target_branch}")
repo.create_git_ref(ref='refs/heads/' + target_branch, sha=main_branch.commit.sha)
if dependabot_file is None:
    repo.create_file(".github/dependabot.yml", message, dependabot_header + "\n" + dependabot_body, target_branch)
else:
    new_body = dependabot_file.decoded_content + dependabot_body.encode()
    repo.update_file(".github/dependabot.yml", message, new_body, dependabot_file.sha, target_branch)

breakpoint()

# pr = repo.create_pull(title="Use 'requests' instead of 'httplib'", body='body', head="develop", base=main_branch)