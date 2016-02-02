#!/bin/sh

NAME=$(rpm -q --specfile *.spec --qf "%{name}\n" | head -n1)
VERSION=$(rpm -q --specfile *.spec --qf "%{version}\n" | head -n1)

tar cavf $NAME-$VERSION.tar.xz $NAME-$VERSION
