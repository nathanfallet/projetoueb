# Get started with Git

## First time

First, clone the repository to work with it:

```bash
git clone https://github.com/NathanFallet/ProjetOueb.git
cd ProjetOueb
```

## Create a new feature

First, be sure to be on the last version of the main branch:

```bash
git pull
```

And then, create a branch (and switch to it) for the feature:

```bash
git branch feature/name-of-the-feature
git checkout feature/name-of-the-feature
```

Write some code, and commit (using VSCode, or from command line):

```bash
git add .
git commit -m "Added an awesome feature"
```

When the feature is ready, push the branch to the remote repository:

```
bash git push
```

Or if you push the branch for the first time:

```bash
git push --set-upstream origin feature/name-of-the-feature
```

Then, go to the repository on the web, and you will show a warning saying that your branch has some commits, with a button to create a pull request. Click on that button to create one.

If your feature/fix is related to an issues, write `Fixes #<number>` to link the pull request to that issue.

Finally, go back to the main branch to start again:

```bash
git checkout main
git pull
```
