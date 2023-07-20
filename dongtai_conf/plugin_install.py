import zipfile
import requests
from io import BytesIO
import fire
import os
from shutil import copytree
from typing import Optional


def _get_plugin(repo: str, extra: dict):
    url_schema = "https://github.com/{repo}/{resofurl}"
    default_url = "https://github.com/HXSecurityBusiness/DongTai-webapi/archive/refs/heads/main.zip"
    default_url = (
        "https://github.com/Bidaya0/DongTai-openapi/archive/refs/tags/v1.0.3.zip"
    )
    if "branch" in extra.keys():
        resofurl = f'archive/refs/heads/{extra["branch"]}.zip'
    elif "tag" in extra.keys():
        resofurl = f'archive/refs/tags/{extra["tag"]}.zip'
    elif "commit" in extra.keys():
        resofurl = f'zip/{extra["commit"]}'
    else:
        resofurl = "archive/refs/heads/main.zip"
    final_url = f"https://github.com/{repo}/{resofurl}"
    if "uri" in extra.keys():
        final_url = extra["uri"]
    r = requests.get(final_url, stream=True)
    z = zipfile.ZipFile(BytesIO(r.content))
    owner, repo_name = repo.split("/")
    z.extractall(f"/tmp/plugin/{repo_name}")


def _install_plugin(repo: str):
    owner, repo_name = repo.split("/")
    base_path = f"/tmp/plugin/{repo_name}/{os.listdir(f'/tmp/plugin/{repo_name}')[0]}"
    copyapp_path = f"{base_path}/logs"
    copytree(copyapp_path, f"./{repo_name}")
    copyapp_path = f"{base_path}/logs"
    copytree(copyapp_path, f"./plugin/{repo_name}/")


def get_plugin(
    repo: str,
    branch: Optional[str] = None,
    tag: Optional[str] = None,
    commit: Optional[str] = None,
    uri: Optional[str] = None,
):
    extra = {
        key: value
        for key, value in filter(
            lambda x: x[1],
            zip(["branch", "tag", "commit", "uri"], [branch, tag, commit, uri]),
        )
    }
    _get_plugin(repo, extra)
    _install_plugin(repo)


if __name__ == "__main__":
    fire.Fire(get_plugin)
