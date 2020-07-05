from dataclasses import asdict
from typing import List

from toolbox.deps.clients import MavenClient


class DepsManager:

    def __init__(self):
        self.scrapper = MavenClient

    def search(self, query: str) -> List[dict]:
        search_page = self.scrapper.search(query)
        results: List[dict] = []
        for res in search_page.results:
            details = self.scrapper.get_artifact_details(res.group_id, res.artifact_id)
            res_obj = asdict(res)
            res_obj["version"] = details.latest_version
            results.append(res_obj)
        return results
