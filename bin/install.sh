#!/bin/bash

set -e
set -o pipefail
set -u
set -x

compiler='gcc@8.2.0-spack'
if [ $(uname) = Darwin ]; then
    compiler1='clang@9.1.0'
else
    compiler1="$compiler"       # this is wrong
fi

mv "../spack-tmux.old" "../spack-tmux" 2>/dev/null || true
mv "../spack-tmux" "../spack-tmux.old" 2>/dev/null || true

#TODO spack view -d false hardlink "../spack-tmux" lmod%"$compiler"
spack view -d false hardlink -i "../spack-tmux" rsync # %"$compiler"
spack view -d false hardlink -i "../spack-tmux" tmux%"$compiler"

mv "../spack-view.old" "../spack-view" 2>/dev/null || true;
mv "../spack-view" "../spack-view.old" 2>/dev/null || true;

spack view -d true hardlink -i "../spack-view" cactusext%"$compiler"
spack view -d false hardlink -i "../spack-view" gcc@8.2.0 # %"$compiler1"

easy_install_file="../spack-view/lib/python2.7/site-packages/easy-install.pth"
rm -f "$easy_install_file"
for pkg in $(spack find -d -l cactusext%"$compiler" |
                 perl -p -e 's/\x1B\[[0-9;]*[a-zA-Z]//g' |
                 grep '\^py-' |
                 awk '{ print $1; }'); do
    dir=$(spack find -p "/$pkg" |
              perl -p -e 's/\x1B\[[0-9;]*[a-zA-Z]//g' |
              grep py- |
              awk '{ print $2; }')
    cat "$dir/lib/python2.7/site-packages/easy-install.pth" \
        >>"$easy_install_file" || true
done

echo ['DONE]'

rm -rf "../spack-tmux.old" "../spack-view.old"
