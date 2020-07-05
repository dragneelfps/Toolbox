import click

from toolbox.deps.flows import search as search_flow, list_deps


@click.group()
def cli():
    pass


@cli.group()
def deps():
    pass


@deps.command()
@click.argument("query")
def search(query):
    print(query)
    search_flow.execute(query)


@deps.command()
def list():
    list_deps.execute()
