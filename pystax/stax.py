import importlib
import os
import re

import click

from pystax.stack import Stack
from pystax.cli import cli

root_path = None
staxfile = None
stack_list = []


def find_staxfile():
    global staxfile
    path = os.getcwd()
    while True:
        staxfile = os.path.join(path, 'Staxfile')
        if os.path.isfile(staxfile):
            return path
        path = os.path.dirname(path)
        if path == os.path.dirname(path):
            raise FileNotFoundError("Unable to locate Staxfile")


def load_staxfile():
    global root_path, staxfile, stack_list
    root_path = root_path or find_staxfile()
    staxfile = staxfile or os.path.join(root_path, 'Staxfile')
    print(f"found {staxfile}")
    with open(staxfile, "r") as file:
        stack_list = [stack for stack in file.read().split("\n") if stack]  # not sure about this...
    require_stacks()


def require_stacks():
    for stack in stack_list:
        module = f"lib.stack.{stack}"
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            pass


def stack_command_factory(stack_name):
    """
    Return a decorated click.command
    """
    @click.command(name=stack_name, short_help=f"{stack_name} stack commands")
    def inner_command():
        print(f"hello from inside {stack_name}")
    return inner_command


def stack_name_to_class_name(stack_name):
    """
    remove delimiters, camel case the stack name
    """
    delimiters = ["_", "-"]
    names = re.split("|".join(delimiters), stack_name)
    return "".join([name.title() for name in names])


def add_stack(stack_name, opts=None):
    """
    add a stack by name, creates class as needed
    """
    if opts is None:
        opts = {}
    stack_list.append(stack_name)
    class_name = stack_name_to_class_name(stack_name)
    stack_class = locals().get(class_name)
    if not stack_class:
        stack_class = Stack(stack_name)
    stack_command = stack_command_factory(stack_name)
    cli.add_command(stack_command)
    # TODO include mixin stuff here
    # TODO imports, type, groups (whatever those are)


def color(string, color_dict):
    """
    def color(string, hash)
        set_color(string, hash.fetch(string.to_sym, :yellow))
      end
    """
    return click.style(string, color_dict.get(string, "yellow"))


def print_table(array):
    if not array:
        return
    for row in array:
        click.echo(f"{' '.join([str(field) for field in row])}")


def find_or_create_stack(stack_name):
    """
    stax calls this variable `id` but it seems to be the stack name
    """
    class_name = stack_name_to_class_name(stack_name)
    stack_class = locals().get(class_name)
    if not stack_class:
        stack_class = Stack(stack_name)
    return stack_class
