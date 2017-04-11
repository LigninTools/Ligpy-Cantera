# Ligpy-Cantera 
### A Kinetic Model for Lignin Pyrolysis (ligpy - cantera)
UW Direct Capstone Project 

------

Biomass valorization through thermochemical conversion of lignocellulosic feedstocks is limited by our lack of detailed kinetic models. In addition to adding mechanistic understanding, more detailed models are needed to optimize industrial biomass pyrolysis processes for producing fuels and chemicals. To this end, we developed a kinetic model for lignin pyrolysis involving ~100 species and 400 reactions which is capable of predicting the temporal evolution of molecules and functional groups during lignin pyrolysis. The model provides information beyond the lumped yields of common pyrolysis models without any fitting, allowing it to cover a wider range of feedstocks and reaction conditions. Good agreement is observed with slow pyrolysis experiments, and an exhaustive global sensitivity analysis using over two million simulations sheds light on reactions that contribute most to the variance in model predictions (sensitivity analysis results and a package to visualize them are available  [here](https://github.com/houghb/savvy)). Model predictions for fast pyrolysis are available, however, recently developed experimental techniques for kinetically-controlled fast pyrolysis of biomass have yet to be applied to lignin.

This work is a continuing development of the original work **ligpy** by [Blake Hough](https://github.com/houghb). *ligpy* is the package developed to solve the kinetic model we describe in our 2016 IECR paper, ***[Detailed kinetic modeling of lignin pyrolysis for process optimization](http://pubs.acs.org/doi/abs/10.1021/acs.iecr.6b02092)***.

Please read the documentation for instructions on using ligpy.

**ligpy documentation:** [![Documentation Status](https://readthedocs.org/projects/ligpy/badge/?version=latest)](http://ligpy.readthedocs.io/en/latest/?badge=latest)  
**Cite ligpy:** [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.53202.svg)](http://dx.doi.org/10.5281/zenodo.53202)


-------
### Software dependencies and license information

**Programming language:**  
Python version 3.6 (https://www.python.org)

**Python packages needed:**  
NumPy version 1.11.3 </p>
Pandas version 0.19.2

The original ODE solver that we used for our research is a modified version of DDASAC that is unfortunately not open source. We chose this solver because it performed the best on the stiff set of ODEs in this model. One of the main objective of this project is to replace the close-sourced ODE solver DDASAC with [Cantera](http://www.cantera.org/docs/sphinx/html/index.html) or
other ODE solver such as python package scipy.integrate.

**License information:**   
ligpy is licensed under a BSD 2-clause “Simplified” License. The objective behind this choice of licensing is to make the content reproducible and make it useful for as many people as possible. We want to maximize the two-way collaborations with minimum restrictions, so that developers of other projects can easily utilize, patch, improve, and cite this code. Please refer to the [license](https://github.com/LigninTools/Ligpy-Cantera/blob/master/LICENSE) for full details.

----------
### Summary of folder contents

**[ligpy/data](https://github.com/houghb/ligpy/tree/master/ligpy/data)** - Contains data files that define the reactions and kinetic parameters which make up the kinetic model, and define the initial composition of various lignin species in terms of our model components.

**[ligpy/data/DFT](https://github.com/houghb/ligpy/tree/master/ligpy/data/DFT)** - Contains the files required to set up, and the results from, our DFT analysis that was used to estimate kinetic parameters for new reactions in the scheme.

