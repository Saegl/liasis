import click
from engine import VirtualLiasisMachine

liasis = VirtualLiasisMachine()


def run_input():
    user_input = 'start'
    while user_input != 'exit':
        user_input = input('>>> ')
        try:
            liasis.execute(user_input)
        except Exception as e:
            print(e)
        if liasis.last_result:
            click.echo(liasis.last_result.repr())


@click.group()
def cli():
    pass


@cli.command()
def run():
    click.echo("Liasis v0.0.1")
    run_input()


@cli.command("file")
@click.argument('path', type=click.Path(exists=True))
@click.option('-i', '--interactive', is_flag=True)
def file(path, interactive):
    click.echo(f'load from file: {path}')
    with open(path) as f:
        liasis.execute(f.read())
    if interactive:
        run_input()


if __name__ == '__main__':
    cli()
