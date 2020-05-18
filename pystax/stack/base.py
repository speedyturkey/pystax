from click import get_current_context


class Stack:

    def __init__(self, short_name):
        self.short_name = short_name
        self.context = get_current_context()
        print(self.context.obj.stack_prefix)
        print(self.short_name)

    # not sure the point of this...
    # @property
    # def class_name(self):
    #     """
    #      get name of stack in Staxfile, or infer it from class
    #      @_class_name ||= self.class.instance_variable_get(:@name).to_s || self.class.to_s.split('::').last.underscore
    #     """
    #     return type(self).__name__

    @property
    def stack_name(self):
        """
        build valid name for the stack
        @_stack_name ||= stack_prefix + cfn_safe(class_name)
        """
        obj = self.context.obj
        return obj.stack_prefix + obj.cfn_safe(self.short_name)

