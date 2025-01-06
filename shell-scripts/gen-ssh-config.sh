usage() {
    [ $# -ne 0 ] && echo "$*"
    echo 'usage: gen-ssh-config.sh OUTPUT_DIRECTORY'
}

keys_dir="$(realpath "$1")"

if [ $# -eq 0 ]; then
    usage
    exit 2
fi

if [ -f "$keys_dir" ]; then
    usage "$keys_dir is exists and a file"
    exit 2
fi

cat << EOF
HostKey $keys_dir/ssh_host_rsa_key
HostKey $keys_dir/ssh_host_ecdsa_key
HostKey $keys_dir/ssh_host_ed25519_key
PubkeyAuthentication yes
PasswordAuthentication no
AuthorizedKeysFile $keys_dir/authorized_keys
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem       sftp    /usr/lib/openssh/sftp-server
EOF

