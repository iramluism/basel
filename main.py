


from basel.client import Basel 
from basel.components import ComponentLoader
from basel.views import ConsoleView


def setup() -> Basel:

    loader = ComponentLoader()
    view = ConsoleView()
    
    basel = Basel(
        loader=loader,
        view=view,
    )
    
    return basel
