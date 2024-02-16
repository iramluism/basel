# Basel Library

![Basel Logo](https://github.com/iramluism/basel/raw/main/docs/images/logo.png)

Basel Library is a powerful tool designed for calculating, reporting, and analyzing the architecture of a project.

## Key Concepts

* **Abstraction**: Level of definition vs implementation inside a component.
* **Stability**: Level of incoming and outgoing dependencies that a component has.

## Installation

```bash
pip install basel
```

## Reports
Abstract/Instability and Component Relationship reports are the main data you can obtain from an architecture. To generate each one, you can use the report and rel options.

### Abstraction/Stability (AE) Report
```
basel report --path ./path/to/project
```
Output:
```
Component                                   I     A     E
----------------------------------------  ----  ----  ----
path/to/project/module1                  0.75   0.2   0.05
path/to/project/module2                     1   0.8   0.8
path/to/project/module3                   0.5     1   0.5
----------------------------------------  ----  ----  ----
Mean                                     0.75  0.67  0.45
```

### Component Relationship (CRel) Report
This report uses a binary matrix, where 1 represents a relation, and 0 does not. All components are assigned to an index. Check the legend below the report to identify each component.

```
basel rel --path ./path/to/project
```
Output:
```
  Components    1    2    3  
------------  ---  ---  ---
           1    0    1    0  
           2    0    0    1  
           3    0    0    0  

Labels:
1: path/to/project/module1
2: path/to/project/module2
3: path/to/project/module3
```

## Formatting
To define a format use the `--format` or the abbreviation `-fmt`.

| Format        | Reports  | Description               |
|:------------- |:--------:|--------------------------:|
| basic         | AE, CRel | Basic and default format  |
| html          | AE, CRel | HTML format               |
| mean_i        | AE       | Only Instability Mean     | 
| mean_a        | AE       | Only Abstraction Mean     |
| mean_e        | AE       | Only Error Mean           |
| mean          | AE       | Only Error Mean           |
| uml           | CRel     | UML code                  |


## Excluding 
You can exclude components in your project, which can be helpful to define boundaries. To exclude, you can use the `-e` or `--exclude` argument.


## Filtering 
Is posible that the report results are very long, to get your desired components you can use the `-f` or `--filter` arguments.


## Contributing

We welcome contributions! If you'd like to contribute to Basel, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Submit a pull request.

Thank you for your contribution!

## Contact

If you have any questions or suggestions, feel free to insert new issue.


## License

This project is licensed under the [MIT License](LICENSE).
