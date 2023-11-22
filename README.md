
## Basel Library

This library calculates the abstraction and the stability of a project


#### Structure of project

````
/src
    |-client          (the main client)
    |-components      (module components and handlers)
    |-config          (configuration file)
    |-dtos            (data transfer objects)
    |-icomponents     (interface components)
    |-views           (views, console, etc)
````


#### Languages and frameworks of the project
````
* Python 3.10.12

````

#### Install Poetry

Check the [Link](https://python-poetry.org/docs/#installing-manually)

#### Install Dependencies

```
poetry install
```

#### Run tests

Run from the project root directory

````
poetry run pytest -vv
````

To check the test coverage run:
```
poetry run coverage run -m pytest -vv
poetry run coverage report
```

### Basic Usage

> [!WARNING] 
> These instructions are for local development, still not ready to implement with pre-commit or as any Python package distribution.

1. Clone the repository on your local machine
   ```
   git clone git@github.com:iramluism/basel.git
   ```
2. Go to your desired project 
3. install the basel library in editable mode 
   
   Using pip
   ```
   pip install ./path/to/basel_repo -e 
   ```
   
   Using Poetry
   ```
   poetry add ./path/to/basel_repo -e
   ```
4. Run the library 

    ```
    python -m basel report --path ./path/to/desired-project
    ```

### Examples
In this repository, two different projects can help you to understand how Basel works. In these little projects, the components are mixed and related to all of them, and with different kinds of Python importations, with abstract classes. check the `tests/stubs` for more details. We can try with one of them

The first and main command in this library is `report`. 
```
basel report --path tests/stubs/stub_project_a
```
You can look something like that
```
Component                                             I    A     D
-------------------------------------------------  ----  ---  ----
tests/stubs/stub_project_a/__init__.py             1     1    1
tests/stubs/stub_project_a/module_1.py             1     0    0
tests/stubs/stub_project_a/package_b/module_b3.py  1     1    1
tests/stubs/stub_project_a/package_b/module_b1.py  0.5   0    0.5
tests/stubs/stub_project_a/package_b/__init__.py   1     1    1
tests/stubs/stub_project_a/package_b/module_b2.py  1     0    0
tests/stubs/stub_project_a/package_a/module_a2.py  0     0.5  0.5
tests/stubs/stub_project_a/package_a/module_a1.py  0.25  1    0.25
tests/stubs/stub_project_a/package_a/__init__.py   1     1    1
Mean Distance: 0.58
```
This command prints a table with the components, the instability (I), the abstractions (A), and the distance (D) from this point (I, A) to the main sequence

Check the `tests/stubs/stub_project_a/__init__.py` component, this has an abstraction and an instability of 1, which means that this component is unuseful. If you check in the project this is a Python package, and there is nothing in the ``__init__.py``. 

Also, you can ignore some dependencies throughout the software evaluation.
To do this use the `--ignore-dependencies` argument.

```
basel report --path tests/stubs/stub_project_a --ignore-dependencies="tests/stubs/stub_project_a/package_a/module_a1.py"
```
You can see something like that
```
Component                                            I    A    D
-------------------------------------------------  ---  ---  ---
tests/stubs/stub_project_a/__init__.py               1  1    1
tests/stubs/stub_project_a/module_1.py               1  0    0
tests/stubs/stub_project_a/package_b/module_b3.py    1  1    1
tests/stubs/stub_project_a/package_b/module_b1.py    0  0    1
tests/stubs/stub_project_a/package_b/__init__.py     1  1    1
tests/stubs/stub_project_a/package_b/module_b2.py    1  0    0
tests/stubs/stub_project_a/package_a/module_a2.py    0  0.5  0.5
tests/stubs/stub_project_a/package_a/module_a1.py    1  1    1
tests/stubs/stub_project_a/package_a/__init__.py     1  1    1
Mean Distance: 0.72
```

We are ignoring the `tests/stubs/stub_project_a/package_a/module_a1.py` component.  If you note, in the above command output this module had an abstraction of 1 and instability of 0.25 and right now has 1 to both metrics. So, we are isolation this component from the rest of the architecture. This is useful when you can ignore the incoming dependencies of a specific module and evaluate the project stability with the rest of the components, e.x Evaluate the domain and infrastructure layers independently.