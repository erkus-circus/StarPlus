# build the python package
mkdir build
cd compiler
zip -r starpc.zip ./*.py
mv starpc.zip ../build

cd ../build
echo '#!/usr/bin/env python3' | cat - starpc.zip > starpc
chmod a+x starpc
rm -rf starpc.zip
cd ..


# copy the libs folder to the build folder.
cp -r compiler/libs/ build/libs/

# build the binaries
cd runtime
### If on a Mac/Linux:
/usr/bin/clang -g *.c -o build/starp
### If on Windows, compile using GCC or a similar C compiler.

cp build/starp ../build/starp

export PATH="$PATH:/Users/eric.diskin/StarPlus/build"

cd ..