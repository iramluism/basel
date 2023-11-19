


from basel.client import Basel 
from basel.components import ComponentLoader
from basel.views import ConsoleView
from basel import config

import argparse

def setup() -> Basel:

    loader = ComponentLoader()
    view = ConsoleView()
    
    basel = Basel(
        loader=loader,
        view=view,
    )
    
    return basel

parser = argparse.ArgumentParser(
    prog=config.PROJECT_NAME,
    description="Calculate the abstraction and stability"
)

parser.add_argument("report")
