# minima
Minima crawls the dependencies of the given file, figures out which ones are used, and returns a summarized version of a file and it's dependencies.

```
$ minipy -h
usage: minipy [-h] [--dependencies] [--tree-shake] [--hide-methods] [--hide-functions] [--depth DEPTH] [--show-return-values] files [files ...]

minima: A Python code analysis tool

positional arguments:
  files                 Paths to the Python files to analyze

options:
  -h, --help            show this help message and exit
  --dependencies        List dependencies
  --tree-shake          Perform tree shaking
  --hide-methods        Omit class methods
  --hide-functions      Omit functions
  --depth DEPTH         Not implemented yet. Depth to resolve dependencies. a value of 2 looks at dependencies of the file, and it's dependencies
  --show-return-values  Show return values, omit the function body
```


## Adding to path (Will be updated in the future)

Clone the repository into a place where you have in your path, e.g i put mine in `~/bin`:

in `.zshrc`:
```
export PATH=$HOME/bin/minima:$PATH
```

## Set up the project:
clone the project to the directory you created for executables:
```
git clone git@github.com:off-by-some/minima.git
```

Install dependencies: 
```shell
pip install rich
```

Create a folder right next to `minima` with the following contents named `minima` (no .py):
```
#!/usr/bin/env python3

from minima.run import main

if __name__ == "__main__":
    main()
```

## Running: 
Now after everything is ran, you should just be able to run `minipy`
```
$ minipy
usage: minipy [-h] [--dependencies] [--tree-shake] [--hide-methods] [--hide-functions]
              [--depth DEPTH] [--show-return-values]
              files [files ...]
minipy: error: the following arguments are required: files
```