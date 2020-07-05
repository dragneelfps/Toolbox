import concurrent.futures

from toolbox.deps.clients import maven
from toolbox.deps.db import RepoDb
from toolbox.utils import wait_print_until_complete


def execute():
    with RepoDb() as db:
        all_saved = db.get_all()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            detail_ftrs = [executor.submit(maven.get_artifact_details, saved[0], saved[1]) for saved in all_saved]

            wait_print_until_complete(lambda: not all([ftr.done() for ftr in detail_ftrs]))

            all_artifacts = [ftr.result() for ftr in detail_ftrs]

            for artifact in all_artifacts:
                print(artifact.latest_version)
