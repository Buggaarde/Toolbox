import platform
if platform.python_version() == '2.7.9':
    import toolbox.Alternate_solvers as solvers
    __all__ = ['plotting',
               'graph_generators',
               'decorators',
               'solvers']
else:
    __all__ = ['plotting',
               'graph_generators',
               'decorators']
