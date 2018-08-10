import click
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.completion import WordCompleter, Completer
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls

from pygments.lexers.python import Python3Lexer
from pygments.styles import get_style_by_name

from .engine import VirtualLiasisMachine

liasis = VirtualLiasisMachine()
completer = WordCompleter([
    'function'
])
style = style_from_pygments_cls(get_style_by_name('monokai'))


class LiasisComleter(Completer):
    def get_completions(self, document, complete_event):
        pass


def run_input():
    user_input = 'start'
    session = PromptSession()
    while user_input != 'exit':
        user_input = session.prompt('>>> ',
            completer=completer, lexer=PygmentsLexer(Python3Lexer), style=style,
            include_default_pygments_style=False)
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
def repl():
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


def main():
    cli()

if __name__ == '__main__':
    main()
