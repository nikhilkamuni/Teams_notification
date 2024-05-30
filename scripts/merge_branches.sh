#!/bin/bash
set -e

git config --global user.email "nikhilkamuni@gmail.com"
git config --global user.name "nikhilkamuni"
git checkout nightly_success
git fetch origin  # Ensure we have the latest changes from the remote
git merge origin/nightly -m "Automated merge from nightly to nightly_success"
git push https://$GITHUB_TOKEN@github.com/nikhilkamuni/Teams_notification.git nightly_success
