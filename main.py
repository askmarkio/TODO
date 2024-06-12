import click

@click.group
def mycommands():
    pass


PRIORITIES = {
    'o': 'Optional',
    'l': 'Low',
    'm': 'Medium',
    'h': 'High',
    'c': 'Critical'
}

@click.command()
@click.argument('priority', type=click.Choice(PRIORITIES.keys()), default='m')
@click.argument('todofile', type=click.Path(exists=False), required=0)
@click.option('-n', '--name', prompt='Enter the todo name', help='The name of the todo')
@click.option('-d', '--desc', prompt='Describe the todo', help='The description of the todo')
def add_todo(name, desc, priority, todofile):
    filename = todofile if todofile is not None else 'TODO.md'
    with open(filename, 'a+') as f:
        f.write(f"{name}: {desc} [Priority: {PRIORITIES[priority]}]")



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





mycommands.add_command(add_todo)
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)



if __name__ == "__main__":
    mycommands()
