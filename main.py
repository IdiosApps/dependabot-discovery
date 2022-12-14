from github import Github
import os

from github.GithubException import UnknownObjectException

access_token = os.getenv('DEPENDABOT_DISCOVERY_TOKEN')

# using an access token
g = Github(access_token)
# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

print(g.get_user().name)

repoName = "awslabs/smithy"
repo = g.get_repo(repoName)
main_branch_name = repo.default_branch
original_main_branch = repo.get_branch(main_branch_name)
dependabot_branch = "dependabot_github_actions"

try:
    workflows_dir = repo.get_contents(".github/workflows")
except UnknownObjectException:
    print(f".github workflows not found, nothing to do for repository {repoName}")
    exit()

try:
    dependabot_file = repo.get_contents(".github/dependabot.yml")
except UnknownObjectException:
    dependabot_file = None
    pass

has_actions_updates = False
if dependabot_file is not None:
    actions_ecosystem_phrase = "package-ecosystem: \"github-actions\"".encode()
    has_actions_updates = actions_ecosystem_phrase in dependabot_file.decoded_content

if has_actions_updates:
    print(f"Repository already has dependabot updates for GitHub Actions")
    exit()

print(f"Creating remote branch {dependabot_branch}")
is_fork = False
try:
    repo.create_git_ref(ref='refs/heads/' + dependabot_branch, sha=original_main_branch.commit.sha)
except UnknownObjectException:
    print("Unable to create branch. Creating fork")
    is_fork = True
    repo = repo.create_fork()
    repo.create_git_ref(ref='refs/heads/' + dependabot_branch, sha=original_main_branch.commit.sha)

message = "Add dependabot updates for dependencies in GitHub Actions workflows"
dependabot_header = """version: 2
updates:"""
dependabot_body = """
  - package-ecosystem: "github-actions"
    directory: \"/\"
    schedule:
      interval: \"weekly\""""

if dependabot_file is None:
    repo.create_file(".github/dependabot.yml", message, dependabot_header + dependabot_body, dependabot_branch)
else:
    new_body = dependabot_file.decoded_content + dependabot_body.encode()
    repo.update_file(".github/dependabot.yml", message, new_body, dependabot_file.sha, dependabot_branch)

pr_title = "Add Dependabot for GitHub Action ecosystem"
pr_body = f"""
This PR adds dependabot updates for dependencies in GitHub Action workflows.

> Actions are often updated with bug fixes and new features to make automated processes more reliable, faster, and safer. When you enable Dependabot version updates for GitHub Actions, Dependabot will help ensure that references to actions in a repository's workflow.yml file are kept up to date.
>
> https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot

Here should go an example line of code which is outdated in this repo: ...

This branch+commit+pr was generated by {g.get_user().login}, by using [IdiosApp's Dependendabot discovery tool](https://github.com/IdiosApps/dependabot-discovery)
"""

if is_fork:
    original_repo = g.get_repo(repoName)
    # https://github.com/PyGithub/PyGithub/issues/792#issuecomment-451731362
    pr = original_repo.create_pull(pr_title,
                                   pr_body,
                                   main_branch_name,
                                   '{}:{}'.format(g.get_user().login, dependabot_branch),
                                   True)
else:
    pr = repo.create_pull(pr_title,
                          pr_body,
                          main_branch_name,
                          dependabot_branch)
