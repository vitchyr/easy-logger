import __main__ as main
from collections import namedtuple
from typing import List

GitInfo = namedtuple(
    'GitInfo',
    [
        ('directory', str),
        ('code_diff', str),
        ('code_diff_staged', str),
        ('commit_hash', str),
        ('branch_name', str),
    ],
)


def generate_git_infos(directories: List[str]) -> List[GitInfo]:
    try:
        import git

        git_infos = []
        for directory in directories:
            # Idk how to query these things, so I'm just doing try-catch
            try:
                repo = git.Repo(directory)
                try:
                    branch_name = repo.active_branch.name
                except TypeError:
                    branch_name = '[DETACHED]'
                git_infos.append(GitInfo(
                    directory=directory,
                    code_diff=repo.git.diff(None),
                    code_diff_staged=repo.git.diff('--staged'),
                    commit_hash=repo.head.commit.hexsha,
                    branch_name=branch_name,
                ))
            except git.exc.InvalidGitRepositoryError:
                pass
    except (ImportError, UnboundLocalError, NameError):
        git_infos = None
    return git_infos


def save_git_infos(git_infos: List[GitInfo], log_dir: str):
    for (
            directory, code_diff, code_diff_staged, commit_hash, branch_name
    ) in git_infos:
        if directory[-1] == '/':
            diff_file_name = directory[1:-1].replace("/", "-") + ".patch"
            diff_staged_file_name = (
                    directory[1:-1].replace("/", "-") + "_staged.patch"
            )
        else:
            diff_file_name = directory[1:].replace("/", "-") + ".patch"
            diff_staged_file_name = (
                    directory[1:].replace("/", "-") + "_staged.patch"
            )
        if code_diff is not None and len(code_diff) > 0:
            with open(osp.join(log_dir, diff_file_name), "w") as f:
                f.write(code_diff + '\n')
        if code_diff_staged is not None and len(code_diff_staged) > 0:
            with open(osp.join(log_dir, diff_staged_file_name), "w") as f:
                f.write(code_diff_staged + '\n')
        with open(osp.join(log_dir, "git_infos.txt"), "a") as f:
            f.write("directory: {}".format(directory))
            f.write('\n')
            f.write("git hash: {}".format(commit_hash))
            f.write('\n')
            f.write("git branch name: {}".format(branch_name))
            f.write('\n\n')
