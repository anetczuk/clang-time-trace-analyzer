#!/bin/bash

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

SRC_DIR="$SCRIPT_DIR/../../src"

OUT_DIR="$SCRIPT_DIR/out"

mkdir -p "${OUT_DIR}"


cd $SRC_DIR


python3 -m ctta analyze \
        --exclude "/usr/include/*" "/usr/lib/*" "/usr/local/*" "/opt/ros/*" \
        -d "$SCRIPT_DIR" \
        --outfile "$OUT_DIR/compile_data.txt" \
        $@

python3 -m ctta flamegraph \
        -f "$SCRIPT_DIR/TikZConverter.cpp.json" \
        --outfile "/tmp/ctta_tikz_flamegraph.svg" \
        $@

# echo "converting svg to png"
# time convert -strip -density 80 "$OUT_DIR/flamegraph.svg" "$OUT_DIR/flamegraph.png"

# python3 -m ctta flamegraphs \
#         -d "$SCRIPT_DIR" \
#         $@

# python3 -m ctta callgrind \
#         -d "$SCRIPT_DIR" \
#         $@
#         # --outfile "$OUT_DIR/callgrind.txt" \


source $SCRIPT_DIR/../../doc/generate_small.sh
