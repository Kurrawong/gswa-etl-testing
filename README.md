# GSWA ETL Testing

This repository contains a small part of GSWA's ETL Python code and demonstrates the use of functional programming and testing frameworks.

Points of interest:

### 1.  Python _module_

All the application code in this repository is not stored in the repository root directory, but a single subdirectory - `etl/`. There is also an empty Python file alled `__init__.py` within that subdirectory. this turns the subdirectory int a Python _module_ that can be accessed from elsewhere in a Pythonic way (`import`) and it separates the application code from tests, installation mechanisms and so on.

### 2. Poetry

[Python's Poetry](https://python-poetry.org/) package manager is used for code dependencies. The following command line commands were issed for this:

```
~$ pip install poetry
~$ poetry init
~$ poetry add rdflib
~$ poetry add --group dev pytest
~$ poetry add --group dev black
```

This installs Poetry, creates the Poetry config, adds `rdflib` to the main application dependencies and installs it and adds `pytest` & `black` to the development dependencies - all in pyproject.toml. 

### 3. pytest

To use the automated testing framework _pytest_, testing code is put in a folder called `tests`, in the repository main folder and as a peer to the `etl` module.

A file called `test_xxx.py` for every file, `xxx` in the main module is added that tests all the functions in that file.

Each function `yyy()` in the main module files is tested with a function called `test_yyy()` in its testing file.

Test functions follow a predictable patter of:

* declare static inputs
* make a comparison object
* execute the function being tested
* print test output
* compare comparison object to function being tested's output

These steps are annotated in the two example test functions.

_pytest_ is then run from the command line, in the root directory of the repository:

```
~$ python -m pytest
```

To trigger the print statements in the testing functions:

```
~$ python -m pytest -s
```

To run just one function, in one file:

```
~$ python -m pytest tests/test_funcs.py::test_tenement
```

### 4. black

_black_ is a Python code formatter.

Install it via Poetry and then run as a Python module, like pytest:

```
python -m black .
```

This will automatically reformat files to "standard" Python formatting.


### 5. Functional Code with type annotations

Functional Code means code containing functions that hav clearly defined inputs & outputs, not secret dependencies and no side effects from running, only the specified outputs.

This is not an absolute but a nice-to-have and it leads to easy to manage, atomic, functions.

See `tenement2()` in `etl/funcs.py`: See the function parameters have types indicated and the compound objects of `subject` has been replaced with a more explicit object: a string called `tenement_id`. Now the function's operations and clearer: it needs to be fed a `tenement)id` directly, not extract it from an object. So the code that calls this function will have to extract the `tenement_id` from whatever object it came in (likely, a DB/PANDAS cursor/dataframe).

The type annotations apply to the function return value (`-> Graph`) telling the user what kind of object is returned.



## Author

**Nicholas J. Car**  
<nick@kurrawong.ai>>  
[KurrawongAI](https://kurrawong.ai)  

###