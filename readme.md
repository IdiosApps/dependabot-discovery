# Dependabot Discovery

Dependabot Discovery is a tool that automates adding GitHub Action dependabot capabilities to specified repositories.

I did this [manually](https://github.com/hyperion-project/hyperion.ng/pull/1486) a few times, and I still see repositories that could benefit from this - especially when there is a lot of toil associated with checking many repositories.

This project will let users quickly and easily add these capabilities to as many repositories as needed. It should work both for github.com, and for enterprise projects. 

# Why keep these things up to date?

GitHub themselves said it best:

> Actions are often updated with bug fixes and new features to make automated processes more reliable, faster, and safer. When you enable Dependabot version updates for GitHub Actions, Dependabot will help ensure that references to actions in a repository's workflow.yml file are kept up to date.
> 
> https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot

# Usage

1. Clone this repository `COMMAND`
2. Create a GitHub Personal Access Token (PAT) with repo permissions - LINK
3. For now, edit main.py
   - Goals section specifies how interaction will be improved

# Goals

- [ ] Raise PR to specified repository which adds GitHub Action Dependabot capabilities 
  - [x] For a repo which the user has write permissions
  - [ ] Optionally: Create a fork so that PRs can be raised in repos which the user doesn't have write access
- [ ] Refactor code to have concepts of `Smells`, `Evidence`, and `Solutions`
  - The specified repo will be checked for some `Smells`
    - For example, a GitHub Action workflow uses a very old dependency
  - The raised PR will state `Evidence` of the smell
    - For example, "File F at line L has V1, which has newer verison V3" 
    - This should make PRs more convincing
  - The `Solution` is the internal code facilitating the fix
    - For example, appending the github-actions ecosystem to an existing dependabot.yml file 
- [ ] To keep github-action smells up-to-date, this repo can have an Action itself with common smells. Dependabot can keep it updated so the latest versions are known.
- [ ] Use the same model to facilitate safer `gradlew` upgrades - [dependabot does not yet do gradlew updates](https://github.com/IdiosApps/dependabot-gradlewrapper-test), and Gradle offers an Action to verify gradlew upgrades.
- [ ] Let user choose options to save resources (only discover & fix suspected smells)
- [ ] Let the user process multiple files
- [ ] Add option to check through all repos in an org (good for cron)