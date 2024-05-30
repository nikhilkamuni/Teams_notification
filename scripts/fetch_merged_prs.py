import os
import subprocess
import re
from github import Github
from github.Repository import Repository

def get_pull_info(pull_id: int, repo: Repository) -> str:
    pr = repo.get_pull(pull_id)
    return f"PR #{pr.number}: {pr.title} by {pr.user.login}"

def check_pr_titles(repo: Repository, src_branch: str, dest_branch: str, regex: str) -> list:
    # Fetch the latest updates from the remote repository
    subprocess.check_output(["git", "fetch", "origin"])

    gitlog = subprocess.check_output(
        [
            "git",
            "log",
            "origin/" + dest_branch + "..origin/" + src_branch,
            "--merges",
            "--pretty=format:%s",
        ]
    ).decode()

    print(f"Git log output:\n{gitlog}")  # Debug: Print git log output

    title_pattern = re.compile(regex)
    merge_pattern = re.compile("^Merge pull request #([0-9]+) from .*$")

    merged_prs = []

    for line in gitlog.split("\n"):
        merge_match = re.search(merge_pattern, line)
        if merge_match:
            pr_id = int(merge_match.group(1))
            pr_info = get_pull_info(pr_id, repo)
            merged_prs.append(pr_info)

    return merged_prs

def main():
    github_personal_access_token = os.getenv("GITHUB_TOKEN")
    assert github_personal_access_token

    github_object = Github(
        base_url="https://api.github.com",
        login_or_token=github_personal_access_token,
    )
    repo = github_object.get_repo("nikhilkamuni/Teams_notification")
    merged_prs = check_pr_titles(repo, "nightly_success", "main", ".*")

    if not merged_prs:
        print("No merged PRs found.")
    else:
        for pr in merged_prs:
            print(pr)

if __name__ == "__main__":
    main()
