#!/bin/bash

set -e
set -o pipefail
set -u
set -x

mv "../spack-tmux.old" "../spack-tmux" 2>/dev/null || true
mv "../spack-tmux" "../spack-tmux.old" 2>/dev/null || true

spack view -d false hardlink "../spack-tmux" lmod%gcc@6.3.0-spack
spack view -d false hardlink "../spack-tmux" rsync%gcc@6.3.0-spack
spack view -d false hardlink "../spack-tmux" tmux%gcc@6.3.0-spack

mv "../spack-view.old" "../spack-view" 2>/dev/null || true;
mv "../spack-view" "../spack-view.old" 2>/dev/null || true;

spack view -d true hardlink "../spack-view" cactusext%gcc@6.3.0-spack
spack view -d true hardlink "../spack-view" gcc@6.3.0

easy_install_file="../spack-view/lib/python2.7/site-packages/easy-install.pth"
rm -f "$easy_install_file"
for pkg in $(spack find -d -l cactusext%gcc@6.3.0-spack |
                 perl -p -e 's/\x1B\[[0-9;]*[a-zA-Z]//g' |
                 grep '\^py-' |
                 awk '{ print $1; }'); do
    dir=$(spack find -p /$pkg |
              perl -p -e 's/\x1B\[[0-9;]*[a-zA-Z]//g' |
              grep py- |
              awk '{ print $2; }')
    cat "$dir/lib/python2.7/site-packages/easy-install.pth" \
        >>"$easy_install_file" || true
done

echo ['DONE]'

rm -rf "../spack-tmux.old"
rm -rf "../spack-view.old"
