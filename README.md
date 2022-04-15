# DCP-challenge


#### by  Ruge Lin

This is a repository for all code written for the article *A quantum computation capability verification protocol for NISQ devices with dihedral coset problem*. 

It gives numerical simulations of DCP challenge.

All code is written Python. Libraries required:

  - matplotlib for plots
  - numpy, statistics, scipy, random, time, argparse
  - Qibo

#### Usage
In this example there are six files
- `proba.py` contains probability calculation and classical simulation.
- `circuit.py` contains functions for quantum circuits simulation.
- `compare.py` is the file to reproduce the FIG.5, the FIG.6 and the FIG.7. 
-  `verification.py` is the file to reproduce the FIG.8. 
-  `benchmarking.py` is the file to reproduce the FIG.9. 
-  `IBM.py` is the file to reproduce the FIG.18. 

The nosie map for noisy circuit simulation can be modified in  `circuit.py`.


##### How to cite

If you use this code in your research, please cite it as follows:
Ruge Lin and Weiqiang Wen, [A quantum computation capability verification protocol for NISQ devices with dihedral coset problem](https://arxiv.org/abs/2202.06984).
