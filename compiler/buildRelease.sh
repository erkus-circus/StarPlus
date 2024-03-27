# build the python package
mkdir build
zip -r build/starpc.zip *.py libs/*.starp
cd build
echo '#!/usr/bin/env python3' | cat - starpc.zip > starpc
chmod a+x starpc
rm -rf starpc.zip
mv starpc ../../build

# copy the libs folder to the build folder.
cp -r ../libs/ ../../build/libs/

# build the binaries
cd ..
cd ..
cd runtime
/usr/bin/clang -g *.c -o build/starp
cp build/starp ../build/starp

