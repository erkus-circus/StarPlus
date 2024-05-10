./make-release.sh
clear

for filename in examplePrograms/*.starp; do
    echo ~~~~~~~~~~~~~~~~~~~~~~~~~~
    echo Compiling: $filename ...
    ./build/starpc $filename
    echo ~~~~~~~~~~~~~~~~~~~~~~~~~~
    echo
done