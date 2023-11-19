
## Basel Library

### Installation for development using Docker and Docker-compose


#### Clone repository

````
git clone
````

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


#### Languages and frameworks of project
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

Run from project root directory

````
poetry run pytest -vv
````

To check the test coverage run:
```
poetry run coverage run -m pytest -vv
poetry run coverage report
```

### Basic Usage

Warning: These instructions are for local development, still is not ready to implement witt pre-commit or as any python package distribution.

1. Clone the repository on your local machine
   ```
   git clone git@github.com:iramluism/basel.git
   ```
2. Go to your desired project 
3. install the base library as editable mode 
   
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
In this repository there are two differents project that can help you to understand how basel works. In this little projects the components are mixed and related to all of them, and with diferents kind of python importations, with abstract class. check the `tests/stubs` for more details. We can try with one of them

First and the main command on this library is `report`. 
```
python -m basel report --path python -m basel report --path tests/stubs/stub_project_a
```
You can look something like that
```
Component                                          I    A     D
----------------------------------------------  ----  ---  ----
tests.stubs.stub_project_a                      1     1    1
tests.stubs.stub_project_a.module_1             1     0    0
tests.stubs.stub_project_a.package_b.module_b3  1     1    1
tests.stubs.stub_project_a.package_b.module_b1  0.5   0    0.5
tests.stubs.stub_project_a.package_b            1     1    1
tests.stubs.stub_project_a.package_b.module_b2  1     0    0
tests.stubs.stub_project_a.package_a.module_a2  0     0.5  0.5
tests.stubs.stub_project_a.package_a.module_a1  0.33  1    0.33
tests.stubs.stub_project_a.package_a            1     1    1
Mean Distance: 0.59
```
This command print a table with the components, the instability (I), the abstractions (A) and the distance from this point (I,A) to the main sequence

Check the `tests.stubs.stub_project_a` component, this has an abstraction and an instability of 1, it mean that this component is unusefull. If you check in the project this is a python package, and there are nothing in the ``__init__.py``. 

Also, you can ignore some dependencies throught the software evaluation.
To do this use the `--ignore-dependencies` argument.

```
 python -m basel report --path tests/stubs/stub_project_a --ignore-dependencies="tests.stubs.stub_project_a.package_a.module_a1"
```
You can see something like that
```
Component                                         I    A    D
----------------------------------------------  ---  ---  ---
tests.stubs.stub_project_a                        1  1    1
tests.stubs.stub_project_a.module_1               1  0    0
tests.stubs.stub_project_a.package_b.module_b3    1  1    1
tests.stubs.stub_project_a.package_b.module_b1    0  0.5  0.5
tests.stubs.stub_project_a.package_b              1  1    1
tests.stubs.stub_project_a.package_b.module_b2    1  0.5  0.5
tests.stubs.stub_project_a.package_a.module_a2    0  0.5  0.5
tests.stubs.stub_project_a.package_a.module_a1    1  1    1
tests.stubs.stub_project_a.package_a              1  1    1
Mean Distance: 0.72
```

We are ignoring the `tests.stubs.stub_project_a.package_a.module_a1` components.  If you note, before that this module had an abstraction of 1 and instability of 0.33 and right now has 1 to both metrics. So, we are isolation this component from the rest of the architecture. This is useful when you can ignore the incoming dependencies of a specific module and evaluate the project stability with the rest of the components, e.x Evaluate the domain and infrastructure layers independently.