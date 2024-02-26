## <a name="main_help"></a> python3 -m ctta --help
```
usage: __main__.py [-h] [--listtools]
                   {analyze,flamegraph,flamegraphs,callgrind} ...

clang-time-trace-analyzer

optional arguments:
  -h, --help            show this help message and exit
  --listtools           List tools

subcommands:
  use one of tools

  {analyze,flamegraph,flamegraphs,callgrind}
                        one of tools
    analyze             perform simple analysis of JSON files
    flamegraph          draw JSON file as flame graph
    flamegraphs         draw JSON files as flame graphs next to given JSONs
    callgrind           display JSON files in kcachegrind viewer
```



## <a name="analyze_help"></a> python3 -m ctta analyze --help
```
usage: __main__.py analyze [-h] [-la] [-f FILES [FILES ...]]
                           [-d DIRS [DIRS ...]]
                           [--exclude EXCLUDE [EXCLUDE ...]]
                           [--outfile OUTFILE]

perform simple analysis of JSON files

optional arguments:
  -h, --help            show this help message and exit
  -la, --logall         Log all messages
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Files to analyze
  -d DIRS [DIRS ...], --dirs DIRS [DIRS ...]
                        Directories to analyze (will recursively search for
                        JSON files)
  --exclude EXCLUDE [EXCLUDE ...]
                        Space separated list of items to exclude. e.g.
                        '/usr/*'
  --outfile OUTFILE     Path to output file
```



## <a name="flamegraph_help"></a> python3 -m ctta flamegraph --help
```
usage: __main__.py flamegraph [-h] [-la] -f FILE [--outfile OUTFILE]

draw JSON file as flame graph

optional arguments:
  -h, --help            show this help message and exit
  -la, --logall         Log all messages
  -f FILE, --file FILE  JSON file to analyze
  --outfile OUTFILE     Path to output file
```



## <a name="flamegraphs_help"></a> python3 -m ctta flamegraphs --help
```
usage: __main__.py flamegraphs [-h] [-la] [-f FILES [FILES ...]]
                               [-d DIRS [DIRS ...]]

draw JSON files as flame graphs next to given JSONs

optional arguments:
  -h, --help            show this help message and exit
  -la, --logall         Log all messages
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Files to analyze
  -d DIRS [DIRS ...], --dirs DIRS [DIRS ...]
                        Directories to analyze (will recursively search for
                        JSON files)
```



## <a name="callgrind_help"></a> python3 -m ctta callgrind --help
```
usage: __main__.py callgrind [-h] [-la] [-f FILES [FILES ...]]
                             [-d DIRS [DIRS ...]]

display JSON files in kcachegrind viewer

optional arguments:
  -h, --help            show this help message and exit
  -la, --logall         Log all messages
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Files to analyze
  -d DIRS [DIRS ...], --dirs DIRS [DIRS ...]
                        Directories to analyze (will recursively search for
                        JSON files)
```
