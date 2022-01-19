# DCP-challenge


#### by  Ruge Lin

This is a repository for all code written for the article *Verification of quantum computation capability for NISQ devices with dihedral coset problem*. 

It gives numerical simulations of DCP challenge in [arXiv: 1912.01618](https://arxiv.org/abs/1912.01618).

All code is written Python. Libraries required:

  - matplotlib for plots
  - numpy, scipy
  - Qibo

#### Usage
In this example there are only three files
- `proba.py` contains the classical functions that are needed to run the experiment.
- `circuit.py` encodes all quantum circuits and procedures needed to run the circuits.
- `main.py` is the file calling all other functions. The action of every line of code is commented in the source code.

The parameters to be fixed for a run of the experiment are
- `m`: number of cells
- `n`: n+1 for number of qubits in each cells
- `t`: number of iterations

##### How to cite

If you use this code in your research, please cite it as follows:
Ruge Lin and Weiqiang Wen (2022). Verification of quantum computation capability for NISQ devices with dihedral coset problem. arXiv preprint arXiv:1912.01618.
