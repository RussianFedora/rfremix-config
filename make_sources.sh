#!/bin/sh

NR=$(rpm -q --specfile rfremix-config.spec --qf "%{name}-%{version}")

cp -r rfremix-config $NR
tar cjf $NR.tar.bz2 $NR
rm -rf $NR
