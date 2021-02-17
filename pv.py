import click

from clients import commands as clients_commands

CLIENTS__TABLE = '.clients.csv'

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj['clients_table'] = CLIENTS__TABLE

cli.add_command(clients_commands.all)