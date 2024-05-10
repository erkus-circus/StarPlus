./make-release.sh
clear

for filename in examplePrograms/*.starp; do
    echo ~~~~~~~~~~~~~~~~~~~~~~~~~~
    echo Compiling: $filename ...
    echo ~~~~~~~~~~~~~~~~~~~~~~~~~~
    ./build/starpc $filename
    echo
done