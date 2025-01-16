import git
import os
import shutil


def clone_github_repo(repo_url, clone_dir):
    """
    Clones a GitHub repository to a specified directory.

    Parameters:
    - repo_url (str): The URL of the GitHub repository.
    - clone_dir (str): The directory where the repository will be cloned.

    Returns:
    - str: The path to the cloned directory.
    """
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)

    git.Repo.clone_from(repo_url, clone_dir)
    return clone_dir


def clean_up_clone(clone_dir):
    """
    Removes the cloned repository directory.

    Parameters:
    - clone_dir (str): The path to the cloned directory.
    """
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
