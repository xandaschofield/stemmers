for file in states/*.gz
do
    cat redostates.condor > special.condor
    echo arguments = $file >> special.condor
    echo queue 1 >> special.condor
    condor_submit special.condor >> logs/redostates.log
done
