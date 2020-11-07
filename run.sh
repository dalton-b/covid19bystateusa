#!/bin/bash
echo "Starting run.sh..."
echo "Creating virtual environment..."
python3 -m venv ./env
echo "Activating environment..."
source ./env/bin/activate
echo "Installing packages..."
pip3 install -e .
echo "Running the project..."
covid_update
echo "Setting GitHub username..."
git config user.name "dalton-b"
echo "Staging changes..."
git add .
echo "Committing changes..."
git commit -m "test_01"
echo "Setting origin..."
git remote set-url origin git@github.com:dalton-b/covid19bystateusa.git
echo "Pushing changes..."
GIT_SSH_COMMAND='ssh -i' '$1 git push
echo "Done!"
