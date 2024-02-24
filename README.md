# clang-time-trace-analyzer

Analyze clang time-trace JSONs. Application iterates through files and directories for time-trace JSONs to concatenate 
them in one output.


## Running application

To run application execute `python3 -m ctta --help` to receive [cmd help](doc/cmdargs.md).


## Instrumenting clang compiler

To instrument *clang* to generate time trace files you have to pass `-ftime-trace` flag to the compiler. It can be 
achieved by following steps:
- through *CMake*: add following line in *CMakeLists.txt*: `set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -ftime-trace")`
- through *make*: add following parameter during execution: `CXXFLAGS="-ftime-trace"`


## Installation

Installation of package can be done by:
 - to install package from downloaded ZIP file execute: `pip3 install --user file:clang-time-trace-analyzer-master.zip#subdirectory=src`
 - to install package directly from GitHub execute: `pip3 install --user git+https://github.com/anetczuk/clang-time-trace-analyzer.git#subdirectory=src`
 - uninstall: `pip3 uninstall --user ctta`

Installation For development:
 - `install-deps.sh` to install package dependencies only (`requirements.txt`)
 - `install-package.sh` to install package in standard way through `pip` (with dependencies)
 - `install-package-dev.sh` to install package in developer mode using `pip` (with dependencies)


## Similar projects

- [speedscope](https://github.com/jlfwong/speedscope)
- [ClangBuildAnalyzer](https://github.com/aras-p/ClangBuildAnalyzer)


## References

- [time-trace: timeline / flame chart profiler for Clang](https://aras-p.info/blog/2019/01/16/time-trace-timeline-flame-chart-profiler-for-Clang/)
- [TECH : Clang Time Trace Feature](https://www.snsystems.com/technology/tech-blog/clang-time-trace-feature)


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
