# DCP-challenge


#### by  Ruge Lin

This is a repository for all code written for the article *A quantum computation capability verification protocol for NISQ devices with dihedral coset problem*. 

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
- `plot.py` is the file to reproduce the Fig.4 in the article, it takes about 3 to 4 hours to run on a CPU of a laptop. 

The parameters to be fixed for a run of the experiment are
- `m`: number of cells, default = 4
- `n`: n+1 for number of qubits in each cells,  default = 3
- `t`: number of iterations, default = 3

The defaut setting takes about 30 seconds to execute on a laptop.

As an example, we fix r=1000, in order to simulate a DCP challenge for m=6, n=5, t=5,
you should execute the following command:

```python
python main.py --m 6 --n 5 --t 5
```

r can be modified in `main.py`,
and the nosie map for noisy circuit simulation can be modified in  `circuit.py`.

#### Results

![prob](/Probability_distribution.png)

The figure includes analytical p_lower and p_upper, one instance of p_clean and one instance of p_error,
and 100 trials of p_bit to see the fluctuation.
p_bit is identical to p_clean, it is just a bitstring simulation instead of a quantum circuit simulation, and much faster.

##### How to cite

If you use this code in your research, please cite it as follows:
Ruge Lin and Weiqiang Wen (2022). A quantum computation capability verification protocol for NISQ devices with dihedral coset problem.
