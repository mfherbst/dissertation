#!/bin/bash
THIS_DIR=$(dirname ${BASH_SOURCE[0]})

# Decrypt key locally and add it to the ssh agent
openssl aes-256-cbc -pass "pass:$SSH_SECRET" -in $THIS_DIR/sshkey_overlay.enc \
	-out $THIS_DIR/sshkey_overlay -d -a
chmod 0400 $THIS_DIR/sshkey_overlay
ssh-add -D
ssh-add $THIS_DIR/sshkey_overlay

# Clone repo
git clone --depth=50 "git@github.com:mfherbst/dissertation-build-overlay.git"
