#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


SRC_DIR="$SCRIPT_DIR/../src"


generate_tools_help() {
    HELP_PATH=$SCRIPT_DIR/cmdargs.md
    
    echo "## <a name=\"main_help\"></a> python3 -m ctta --help" > ${HELP_PATH}
    echo -e "\`\`\`" >> ${HELP_PATH}

    cd $SRC_DIR
    python3 -m ctta --help >> ${HELP_PATH}

    echo -e "\`\`\`" >> ${HELP_PATH}
}


generate_tools_help


$SCRIPT_DIR/generate_small.sh
