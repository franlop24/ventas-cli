import click

from clients.services import ClientService
from clients.models import Client

@click.group()
def clients():
    """Manages the clients lifecycle"""
    pass


@clients.command()
@click.option('-n', '--name',
            type=str,
            prompt=True,
            help='The client name')
@click.option('-c', '--company',
            type=str,
            prompt=True,
            help='The client company')
@click.option('-e', '--email',
            type=str,
            prompt=True,
            help='The client email')
@click.option('-p', '--position',
            type=str,
            prompt=True,
            help='The client position')
@click.pass_context
def create(ctx, name, company, email, position):
    """Creates a new client"""

    client = Client(name, company, email, position)
    client_service = ClientService(ctx.obj['clients_table'])

    client_service.create_client(client)


@clients.command()
@click.pass_context
def list(ctx):
    """List all clients"""
    client_service = ClientService(ctx.obj['clients_table'])

    client_list = client_service.list_clients()    

    click.echo('ID\t | NAME\t | COMPANY\t | EMAIL\t | POSITION')
    click.echo('*-*' * 30)
    for client in client_list:
        click.echo(f"{client['uid']}\t | {client['name']}\t | {client['company']}\t | {client['email']}\t | {client['position']}")
        

@clients.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def update(ctx, client_uid):
    """Updates a client"""
    client_service = ClientService(ctx.obj['clients_table'])

    client_list = client_service.list_clients()

    client = [client for client in client_list if client['uid'] == client_uid]
    print(client)

    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)

        click.echo('Client updated')
    else:
        click.echo('Client not found')


@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Deletes a client"""
    client_service = ClientService(ctx.obj['clients_table'])

    client_list = client_service.list_clients()

    client = [client for client in client_list if client['uid'] == client_uid]
    
    if client:
        client_service.delete_client(Client(**client[0]))

        click.echo('Client deleted')
    else:
        click.echo('Client not found')


def _update_client_flow(client):
    click.echo('Leave empty if you dont want to modify de value')

    client.name = click.prompt('New name', type=str, default=client.name)
    client.company = click.prompt('New Company', type=str, default=client.company)
    client.email = click.prompt('New email', type=str, default=client.email)
    client.position = click.prompt('New posotion', type=str, default=client.position)

    return client


all = clients
