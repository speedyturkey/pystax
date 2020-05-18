import os
import re
import subprocess

import click

from pystax.aws import Sts
from pystax.commands import ls


def system(command_string):
    # TODO error handle
    return subprocess.run(command_string.split(" "), capture_output=True).stdout.decode().strip()


class Git:

    @classmethod
    def branch(cls):
        return system("git symbolic-ref --short HEAD")

    @classmethod
    def toplevel(cls):
        return system("git rev-parse --show-toplevel")


class StaxContext:
    """
    For use as a click.Context object
    """
    def __init__(self, app=None, branch=None):
        self.app = app
        self.branch = branch
        self.sts = None

    @property
    def app_name(self):
        if self.app is None:
            return None
        return self.cfn_safe(self.app)

    @property
    def branch_name(self):
        return self.cfn_safe(self.branch)

    @property
    def stack_prefix(self):
        """
        @_stack_prefix | |= [app_name, branch_name].compact.join('-') + '-'
        """
        elements = [self.app_name, self.branch_name]
        elements = list(filter(None, elements))
        return "-".join(elements) + "-"

    @property
    def aws_account_id(self):
        """
        "@_aws_account_id | |= Aws::Sts.id.account"
        """
        if self.sts is None:
            self.sts = Sts()
        return self.sts.account_id

    @property
    def aws_region(self):
        """
        @_aws_region | |= ENV['AWS_REGION']
        """
        return os.environ.get("AWS_REGION")

    @staticmethod
    def cfn_safe(string):
        """
        Cloudformation names consist of alphanumeric characters and dashes only.
        """
        return re.sub(r"[\W_]", "-", string)


default_app = os.path.basename(Git.toplevel())
default_branch = Git.branch()


@click.group()
@click.option("--app", default=default_app, help=f"application name (default {default_app})")
@click.option("--branch", default=default_branch, help=f"git branch to use (default {default_branch})")
@click.pass_context
def cli(ctx, app, branch):
    ctx.obj = StaxContext(
        app=app,
        branch=branch
    )


@cli.command()
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())


cli.add_command(ls)


def main():
    cli()


if __name__ == "__main__":
    main()
