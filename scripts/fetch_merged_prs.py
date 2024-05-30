import os
import subprocess
import re
from github import Github
from github.Repository import Repository

def get_pull_title(pull_id: int, repo: Repository) -> str:
    pr = repo.get_pull(pull_id)
    return f"PR #{pr.number}: {pr.title} by {pr.user.login}"

def check_pr_titles(repo: Repository, src_branch: str, dest_branch: str, regex: str) -> list:
    gitlog = subprocess.check_output(
        [
            "git",
            "log",
            f"origin/{dest_branch}..origin/{src_branch}",
            "--merges",
            "--pretty=format:%s",
        ]
    ).decode()

    title_pattern = re.compile(regex)
    merge_pattern = re.compile(r"^Merge pull request #(\d+) from .*\$")

    merged_prs = []

    for line in gitlog.split("\n"):
        merge_match = re.search(merge_pattern, line)
        if merge_match:
            pr_id = int(merge_match.group(1))
            title = get_pull_title(pr_id, repo)
            merged_prs.append(title)

    return merged_prs

def main():
    github_personal_access_token = os.getenv("GITHUB_TOKEN")
    if not github_personal_access_token:
        raise ValueError("GitHub token not found")

    github_object = Github(github_personal_access_token)
    repo = github_object.get_repo("nikhilkamuni/Teams_notification")
    merged_prs = check_pr_titles(repo, "nightly_success", "main", ".*")

    if merged_prs:
        print("\n".join(merged_prs))
    else:
        print("No merged PRs found.")

if __name__ == "__main__":
    main()
