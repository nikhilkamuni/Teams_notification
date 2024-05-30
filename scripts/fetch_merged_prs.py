import os
import subprocess
import re
from github import Github
from github.Repository import Repository

def get_pull_details(pull_id: int, repo: Repository) -> (str, str):
    pr = repo.get_pull(pull_id)
    return pr.title, pr.user.login

def check_pr_titles(repo: Repository, src_branch: str, dest_branch: str, regex: str) -> list:
    gitlog = subprocess.check_output(
        [
            "git",
            "log",
            "origin/" + dest_branch + "..origin/" + src_branch,
            "--merges",
            "--pretty=format:%s",
        ]
    ).decode()

    title_pattern = re.compile(regex)
    merge_pattern = re.compile("^Merge pull request #([0-9]+) from .*\$")

    merged_prs = []

    for line in gitlog.split("\n"):
        merge_match = re.search(merge_pattern, line)
        if merge_match:
            pr_id = int(merge_match.group(1))
            title, user = get_pull_details(pr_id, repo)
            merged_prs.append(f"PR #{pr_id} by {user}: {title}")

    return merged_prs

if __name__ == "__main__":
    github_personal_access_token = os.getenv("GITHUB_TOKEN")
    assert github_personal_access_token

    github_object = Github(
        base_url="https://api.github.com",
        login_or_token=github_personal_access_token,
    )
    repo = github_object.get_repo("nikhilkamuni/Teams_notification")
    merged_prs = check_pr_titles(repo, "nightly_success", "main", ".*")
    for pr in merged_prs:
        print(pr)
