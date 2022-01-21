# DCP-challenge


#### by  Ruge Lin

This is a repository for all code written for the article *Verification of quantum computation capability for NISQ devices with dihedral coset problem*. 

It gives numerical simulations of DCP challenge.

All code is written Python. Libraries required:

  - matplotlib for plots
  - numpy, statistics, random, time, argparse
  - Qibo

#### Usage
In this example there are only three files
- `proba.py` contains probability calculation and classical simulation.
- `circuit.py` contains functions for quantum circuits simulation.
- `main.py` is the file calling all other functions. The action of every line of code is commented in the source code.

The parameters to be fixed for a run of the experiment are
- `m`: number of cells
- `n`: n+1 for number of qubits in each cells
- `t`: number of iterations

As an example, we fix r=1000, in order to simulate a DCP challenge for m=4, n=3, t=3,
you should execute the following command:

```python
python main.py --m 4 --n 3 --t 3
```

Nosie map for noisy circuit simulation can be modified in  `circuit.py`.

#### Results


##### How to cite

If you use this code in your research, please cite it as follows:
Ruge Lin and Weiqiang Wen (2022). Verification of quantum computation capability for NISQ devices with dihedral coset problem.
