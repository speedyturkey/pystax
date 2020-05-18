import click

from pystax import stax
from pystax.aws import Cfn


@click.command()
@click.option("--prefix", default=None)
@click.option("--account", is_flag=True, help="list all running stacks in account")
@click.option("--all", "all_", is_flag=True, help="list all running stacks with our prefix")
@click.option("--existing", is_flag=True, help="list just existing stacks")
@click.pass_obj
def ls(context, existing, all_, account, prefix):
    if account:
        ls_account_stacks()
    elif all_:
        ls_stacks_with_prefix(prefix, context.stack_prefix)
    else:
        ls_staxfile_stacks(existing)


def ls_account_stacks():
    """
    print_table Aws::Cfn.stacks.map { |s|
        [s.stack_name, s.creation_time, color(s.stack_status, Aws::Cfn::COLORS), s.template_description]
    }.sort
    """
    stacks = [
        [
            s["StackName"],
            s["CreationTime"],
            stax.color(s["StackStatus"], Cfn().COLORS),
            s["TemplateDescription"],
        ]
        for s in Cfn().stacks()
    ]
    stax.print_table(sorted(stacks))


def ls_stacks_with_prefix(prefix, stack_prefix):
    """
      def ls_stacks_with_prefix(prefix)
        print_table Aws::Cfn.stacks.select { |s|
          s.stack_name.start_with?(prefix || stack_prefix)
        }.map { |s|
          [s.stack_name, s.creation_time, color(s.stack_status, Aws::Cfn::COLORS), s.template_description]
        }.sort
      end
    """
    stacks = [
        [
            s["StackName"],
            s["CreationTime"],
            stax.color(s["StackStatus"], Cfn().COLORS),
            s["TemplateDescription"],
        ]
        for s in Cfn().stacks() if s["StackName"].startswith(prefix or stack_prefix)
    ]
    stax.print_table(sorted(stacks))


def ls_staxfile_stacks(existing):
    """
    stacks = Aws::Cfn.stacks.each_with_object({}) { |s, h| h[s.stack_name] = s }
    print_table Stax.stack_list.map { |id|
      name = stack(id).stack_name
      if (s = stacks[name])
        [s.stack_name, s.creation_time, color(s.stack_status, Aws::Cfn::COLORS), s.template_description]
      else
        options[:existing] ? nil : [name, '-']
      end
    }.compact
    """
    stacks = {
        stack["StackName"]: stack for stack in Cfn().stacks()
    }
    staxfile_stacks = []
    for stack in stax.stack_list:
        stack_class = stax.find_or_create_stack(stack)
        s = stacks.get(stack_class.stack_name)
        if s:
            staxfile_stacks.append([
                s["StackName"],
                s["CreationTime"],
                stax.color(s["StackStatus"], Cfn().COLORS),
                s["TemplateDescription"]
            ])
    stax.print_table(sorted(staxfile_stacks))

