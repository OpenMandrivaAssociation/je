#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-sources VERSION"
    exit 1
fi

VERSION=${1}
NAME="je"

wget http://download.oracle.com/berkeley-db/${NAME}-${VERSION}.tar.gz
tar -xf ${NAME}-${VERSION}.tar.gz
rm ${NAME}-${VERSION}.tar.gz
find ./${NAME}-${VERSION} -name "*.jar" -delete
find ./${NAME}-${VERSION} -name "*.class" -delete
# Remove unused files
rm -Rf ./${NAME}-${VERSION}/docs/*
rm -Rf ./${NAME}-${VERSION}/lib
tar cJf ${NAME}-${VERSION}-clean.tar.xz ./${NAME}-${VERSION}