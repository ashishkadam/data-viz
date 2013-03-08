This folder contains the following files:

1) connectome.csv - connectivity table from the "Connectome" tab of the condensed connectivity spreadsheet 

2) neurons.csv - neuron table condensed from the "Single Neurons" tab of the regular connectivity spreadsheet 

3) simpleatlas.csv - second connectivity table of the "Neuronal Connectivity" tab of the regular connectivity spreadsheet 

4) wormatlas.csv - first connectivity table of the Neuronal Connectivity" tab of the regular connectivity spreadsheet

5) worm2hive.py - Python script that converts the connectivity info (specifically from connectome.csv and neurons.csv) into the jhive format.

6) *.png - some Hive Plots made with jhive and edited with MS Paint.

To run the script just go to this folder on the command line (on any OS with Python 2.7) and type "python worm2hive.py". The result will be stored on worms.txt, so now with jhive you can open it and make your own hive plots.

To color gap junctions, just write this on the rules and apply: e(synapse=GapJunction) [thickness=1;rgb=2;opacity=50].

To separate nodes into neuron types, just choose axis x:$ntype and type:
a1: 'x'=='interneuron'
a2: 'x'=='motor'
a3: 'x'=='sensory'

You can do much more than this, but you will have to learn to work with jhive and take a look at worms.txt to see what properties can be used for plotting.
