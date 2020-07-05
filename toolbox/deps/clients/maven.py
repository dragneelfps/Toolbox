from typing import Optional

import requests
from bs4 import BeautifulSoup

from toolbox.deps.models.ArtifactDetailPage import ArtifactDetailPage
from toolbox.deps.models.SearchResultPage import SearchResultPage


def search(query: str, page: int = 1) -> SearchResultPage:
    assert len(query) > 0, "'query' term should be non-empty"
    params = {
        "q": query,
        "p": page
    }
    res = requests.get("https://mvnrepository.com/search", params=params)
    soup = BeautifulSoup(res.text, "html.parser")

    return SearchResultPage(soup, page)


def get_artifact_details(group_id: str, artifact_id: str, repo: Optional[str] = None) -> ArtifactDetailPage:
    params = {
        "repo": repo
    }
    res = requests.get("https://mvnrepository.com/artifact/{}/{}".format(group_id, artifact_id), params=params)
    soup = BeautifulSoup(res.text, "html.parser")

    return ArtifactDetailPage(soup, group_id=group_id, artifact_id=artifact_id, repo=repo)
