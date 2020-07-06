import concurrent.futures
import itertools
from typing import List, Optional

from tabulate import tabulate

from toolbox.deps.clients import maven
from toolbox.deps.db import RepoDb
from toolbox.deps.models.SearchResultPage import SearchResultItem
from toolbox.utils import wait_print_until_complete


def execute(query: Optional[str] = None, group_id: Optional[str] = None, artifact_id: Optional[str] = None):
    if query is not None:
        search_by_query(query)
    if group_id is not None and artifact_id is not None:
        search_artifact(group_id, artifact_id)


def search_artifact(group_id: str, artifact_id: str):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        arti_details_ftr = executor.submit(maven.get_artifact_details, group_id=group_id,
                                           artifact_id=artifact_id)

        wait_print_until_complete(lambda: not arti_details_ftr.done())

        latest_version = arti_details_ftr.result().latest_version

        print(f"Latest Version: {latest_version}")
        usr_inp = input("Save??? (y/n): ")
        if usr_inp in ["y", "Y"]:
            with RepoDb() as db:
                db.insert(latest_version.group_id, latest_version.artifact_id)
                print("Saved.")


def search_by_query(query: str):
    with concurrent.futures.ThreadPoolExecutor() as executor:

        page = 1
        start_index = 1
        complete = False
        while not complete:
            data_fr = executor.submit(__get_list_of_results, query, page, start_index)

            wait_print_until_complete(lambda: not data_fr.done())

            data = data_fr.result()

            __print_result(data)
            usr_inp = __get_user_selection()
            if usr_inp in ["m", "M"]:
                page += 1
                start_index += len(data)
                continue

            matches = list(filter(lambda row: row["index"] == usr_inp, data))
            if len(matches) == 0:
                print("Invalid user input")
                print("Exiting....")
                exit()
            selection = matches[0]
            print("You selected: ")
            selection["result"].pretty_print()

            result: SearchResultItem = selection["result"]

            search_artifact(group_id=result.group_id, artifact_id=result.artifact_id)

            complete = True


def __get_list_of_results(query: str, page: int = 1, start_index: int = 1) -> List[dict]:
    page_res = maven.search(query=query, page=page)
    results = page_res.results

    data = []
    for i, res in enumerate(results):
        row = {
            "index": str(i + start_index),
            "result": res
        }
        data.append(row)

    return data


def __print_result(data: List[dict]):
    rows = [list(itertools.chain([res["index"]], res["result"].tabulate_data())) for res in data]
    table = tabulate(rows)
    print(table)


def __get_user_selection():
    sel = input("Choose result(m for more, e for exit): ")
    if sel == "e" or sel == "E":
        exit()
    return sel


def __show_details(self, index: int):
    pass


def __get_user_should_save(self):
    pass


def __store_in_db(self):
    pass


def __show_more(self):
    pass


def __exit(self):
    pass
