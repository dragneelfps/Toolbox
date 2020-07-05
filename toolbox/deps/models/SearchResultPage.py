from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup, Tag


@dataclass
class SearchResultItem:
    title: str
    group_id: str
    artifact_id: str
    description: str

    def tabulate_data(self) -> List[str]:
        return [self.title, self.group_id, self.artifact_id, self.description]

    def pretty_print(self):
        print("Title: ", self.title)
        print("Group Id: ", self.group_id)
        print("Artifact Id: ", self.artifact_id)
        print("Description: ", self.description)

    @staticmethod
    def tabulate_header() -> List[str]:
        return ["Title", "Group Id", "Artifact Id", "Description"]


@dataclass
class SearchResultPage:
    total_results: int
    current_page: int
    results: List[SearchResultItem]

    def __init__(self, soup: BeautifulSoup, current_page: int):
        self.current_page = current_page
        self.total_results = int(soup.select_one("#maincontent h2 b").text)

        search_results = soup.select("#maincontent div.im")
        self.results = list(map(self.__map_search_result, search_results))

    @staticmethod
    def __map_search_result(search_result: Tag) -> SearchResultItem:
        return SearchResultItem(title=search_result.select_one("h2.im-title > a").text,
                                group_id=search_result.select_one("p.im-subtitle > a:nth-child(1)").text,
                                artifact_id=search_result.select_one("p.im-subtitle > a:nth-child(2)").text,
                                description=search_result.select_one("div.im-description").contents[0].strip())
