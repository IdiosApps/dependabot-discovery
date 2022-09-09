# Dependabot Discovery

Dependabot Discovery is a tool that automates adding GitHub Action dependabot capabilities to specified repositories.

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