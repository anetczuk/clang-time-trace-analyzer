# clang-time-trace-analyzer

Analyze clang time-trace JSONs. Application iterates through files and directories for time-trace JSONs to concatenate 
them in one output.

Features:
- generation of flame graph from single JSON file
- viewing multiple JSON files at once in *KCachegrind*


## Examples

Example output of `analyze` tool: [sorted files](examples/tikz/out/compile_data.txt).

Example output of `flamegraph` tool:
[![flamegraph example](examples/tikz/out/flamegraph_svg-small.png "flamegraph example")](examples/tikz/out/flamegraph_svg.png)

After running `callgrind` tool *KCachegrind* will be used to present results. Example view can be seen in following screen:
[![KCachegrind example](examples/tikz/out/kcachegrind_screen-small.png "KCachegrind example")](examples/tikz/out/kcachegrind_screen.png)


## Running application

To run application execute `python3 -m ctta --help` to receive [cmd help](doc/cmdargs.md).

Showing multiple files placed in pointed directory in KCachegrind:

`python3 -m ctta callgrind -d /path/to/build/dir`


## Instrumenting clang compiler

To instrument *clang* to generate time trace files you have to pass `-ftime-trace` flag to the compiler. It can be 
achieved by following steps:
- through *CMakeLists.txt*: `set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -ftime-trace")`
- through *cmake* cmd line: `cmake -DCMAKE_CXX_FLAGS="-ftime-trace" .`


## Installation

Installation of package can be done by:
 - to install package from downloaded ZIP file execute: `pip3 install --user -I file:clang-time-trace-analyzer-master.zip#subdirectory=src`
 - to install package directly from GitHub execute: `pip3 install --user -I git+https://github.com/anetczuk/clang-time-trace-analyzer.git#subdirectory=src`
 - uninstall: `pip3 uninstall ctta`

Installation For development:
 - `install-deps.sh` to install package dependencies only (`requirements.txt`)
 - `install-package.sh` to install package in standard way through `pip` (with dependencies)
 - `install-package-dev.sh` to install package in developer mode using `pip` (with dependencies)


## Similar projects

- [ClangBuildAnalyzer](https://github.com/aras-p/ClangBuildAnalyzer)
- [speedscope](https://github.com/jlfwong/speedscope)
- [crofiler](https://github.com/HadrienG2/crofiler/)


## References

- [time-trace: timeline / flame chart profiler for Clang](https://aras-p.info/blog/2019/01/16/time-trace-timeline-flame-chart-profiler-for-Clang/)
- [TECH : Clang Time Trace Feature](https://www.snsystems.com/technology/tech-blog/clang-time-trace-feature)
- [The trace-event file format](https://github.com/catapult-project/catapult/wiki/Trace-Event-Format)
- [Callgrind Format Specification](https://valgrind.org/docs/manual/cl-format.html)


## License

BSD 3-Clause License

Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
