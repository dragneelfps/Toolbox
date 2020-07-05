from dataclasses import dataclass
from typing import Optional, List

from bs4 import BeautifulSoup, Tag


@dataclass
class ArtifactVersion:
    group_id: str
    artifact_id: str
    version: str
    repo: str
    usages: int
    date: str

    def __repr__(self):
        return "{}:{}:{}".format(self.group_id, self.artifact_id, self.version)


@dataclass
class ArtifactDetailPage:
    group_id: str
    artifact_id: str
    repo: Optional[str]
    versions: List[ArtifactVersion]
    latest_version: ArtifactVersion

    def __init__(self, soup: BeautifulSoup, group_id: str, artifact_id: str, repo: Optional[str] = None):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.repo = repo

        version_results = soup.select("table.versions tr")[1:]
        self.versions = []
        for version_result in version_results:
            version = self.__map_version_result(version_result, self.group_id, self.artifact_id)
            self.versions.append(version)
        self.latest_version = self.versions[0]

    @staticmethod
    def __map_version_result(version_result: Tag, group_id: str, artifact_id: str) -> ArtifactVersion:
        return ArtifactVersion(group_id=group_id,
                               artifact_id=artifact_id,
                               version=version_result.select_one("a.vbtn").text,
                               repo=version_result.select_one("td:nth-last-child(3) a").text,
                               usages=int(
                                   version_result.select_one("td:nth-last-child(2)").text.replace(",", "")),
                               date=version_result.select_one("td:nth-last-child(1)").text)
