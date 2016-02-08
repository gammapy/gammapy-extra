#!/bin/bash

init_conda
init_gammapy-extra

gammapy-spectrum all spectrum_analysis_example.yaml

cp test_dir/spectrum.yaml .
cp test_dir/fitfunction.yaml .
