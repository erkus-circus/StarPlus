./make-release.sh
clear

for filename in examplePrograms/*.starpc; do
    echo ~~~~~~~~~~~~~~~~~~~~~~~~~~
    echo Running: $filename ...
    echo ~~~~~~~~~~~~~~~~~~~~~~~~~~
    ./build/starp $filename
    echo
done