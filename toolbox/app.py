import click

from toolbox.deps.flows import search as search_flow, list_deps


@click.group()
def cli():
    pass


@cli.group()
def deps():
    pass


@deps.command()
@click.argument("query", required=False)
@click.option("-g", "--group", required=False)
@click.option("-a", "--artifact", required=False)
def search(query, group, artifact):
    if query is None:
        if group is not None and artifact is not None:
            search_flow.execute(group_id=group, artifact_id=artifact)
        else:
            raise click.UsageError("Invalid usage")
    elif group is not None or artifact is not None:
        raise click.UsageError("Invalid usage")
    else:
        search_flow.execute(query=query)


@deps.command()
def list():
    list_deps.execute()
