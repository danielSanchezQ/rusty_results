#!/usr/bin/env bash

SCRIPTS_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$SCRIPTS_DIRECTORY/clean.sh
$SCRIPTS_DIRECTORY/build.sh
