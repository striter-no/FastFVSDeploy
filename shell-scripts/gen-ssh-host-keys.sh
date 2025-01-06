#!/usr/bin/env sh

usage() {
    [ $# -ne 0 ] && echo "$*"
    echo 'usage: gen-ssh-host-keys.sh SSH_KEYS_DIRECTORY'
}

out="$1"

if [ $# -eq 0 ]; then
    usage
    exit 2
fi

if [ -f "$out" ]; then
    usage "$out is exists and a file"
    exit 2
fi

mkdir -p "$out"

temp="$(mktemp -d)"
mkdir -p "$temp/etc/ssh"
ssh-keygen -A -f "$temp"
cp "$temp"/etc/ssh/* "$out"
rm -r "$temp"

