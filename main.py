import sys
import click
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    'info': 'bold white',
    'success': 'bold green',
    'warning': 'bold yellow',
    'danger': 'bold red'
})

console = Console(theme=custom_theme)

@click.group
def mycommands():
    console.line()
    console.rule("TODO", style='info')
    console.line()


PRIORITIES = {
    'o': 'Optional',
    'l': 'Low',
    'm': 'Medium',
    'h': 'High',
    'c': 'Critical'
}



def user_input():
    console.line()
    console.rule("TODO", style='info')
    console.line()
    description = """
    Please choose an option:
    
    1: Add TODO
    2: Delete TODO
    3: List TODOs
    4: Exit
    """
    console.print(description)
    console.line()

    while True:
        s = input("Please select the data you want: ")

        # Match to the user's input 
        match s:
            case "1":
                return add_todo()
            case "2":
                return delete_todo()
            case "3":
                return list_todos()
            case "4":
                exit_message()
                return sys.exit()
            case _:
                print("Please choose an option above.")


@click.command()
@click.argument('priority', type=click.Choice(PRIORITIES.keys()), default='m')
@click.argument('todofile', type=click.Path(exists=False), required=0)
@click.option('-n', '--name', prompt='Enter the todo name', help='The name of the todo')
@click.option('-d', '--desc', prompt='Describe the todo', help='The description of the todo')
def add_todo(name, desc, priority, todofile):
    filename = todofile if todofile is not None else 'TODO.md'
    priority_val = PRIORITIES[priority]
        
    with open(filename, 'a+') as f:
        f.write(f"[ ] {name}: {desc} [Priority: {PRIORITIES[priority]}]")
        f.write('\n')
        console.line()
        console.rule('[bold green]Success[/]', style='success')
        console.line()
        console.print(f'Your TODO [bold green]{name}[/] with a priority of {priority_val} has been added!')
        console.line()


@click.command()
@click.argument('idx', type=int, required=1)
def delete_todo(idx):
    with open('TODO', 'r') as f:
        todo_list = f.read().splitlines()
        todo_list.pop(idx)
    with open('TODO', 'w') as f:
        f.write('\n'.join(todo_list))
        f.write('\n')



@click.command()
@click.option('-p', '--priority', type=click.Choice(PRIORITIES.keys()))
@click.argument('todofile', type=click.Path(exists=True), required=0)
def list_todos(priority, todofile):
    filename = todofile if todofile is not None else 'TODO.md'
    with open(filename, 'r') as f:
        todo_list = f.read().splitlines()
    if priority is None:
        for idx, todo in enumerate(todo_list):
            print(f"({idx}) - {todo}")

def exit_message():
    console.line()
    console.print('You selected to exit!', style='warning')
    console.line()
    console.rule('Goodbye', style='warning')
    console.line()


mycommands.add_command(add_todo)
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)



if __name__ == "__main__":
    # mycommands()
    user_input()
