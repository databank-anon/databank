# The Databank

This Git repository contains the supplementary material and artifacts of the paper "Data Protection Using Taints and Monitors" submitted at PETS'23.

## Source code

The *src/* folder contains the source code of the prototype (thereafter called "Databank") presented in Section 6 of the paper, while the *monpoly/* folder contains the source code of the modified MonPoly monitor, forked from [here](https://bitbucket.org/jshs/monpoly).

Two example applications are provided:
* A toy application called "Test" (in src/collection/test.py) running the code given in Figure 5 of the paper.
* The meeting management application called "Meet" (in src/collection/meet.py) used for evaluation in Section 7 of the paper.
* The Twitter-like application "Minitwit" (in src/collection/minitwit.py) discussed in the evaluation in Section 7 of the paper.

To install the prototype from the source, clone this repository and execute (or follow the steps in) install.sh. Required is a 64-bit Debian-based system. The prototype was tested under Ubuntu 20.04.2 LTS and Debian 10.10.0 using Python 3.6.5. To run the evaluation scripts, you additionally need to add [Geckodriver 0.29.1](https://github.com/mozilla/geckodriver/releases) to your path.

## VirtualBox

Alternatively, a VirtualBox containing a ready-to-use installation of the Databank prototype is available for download [here](https://drive.google.com/file/d/1l1sByhZAtfFd9yjLGlvh1-LIPJaOGzm4/view?usp=sharing). The session password for user "user" is "user". The Databank and a Firefox browser will start automatically after logging in. The code is located in ~/Databank.

Two users "Alice" and "Bob" are defined in the provided instance of the "Meet" application. The Databank password of both users is "test".

## Data and evaluation scripts

The evaluation scripts used to produce the results from Section 7 can be found in the *evaluation/* folder, also available in the provided VirtualBox. Script *evaluation.py* runs the experiments, writing the results in *log.json*, and *evaluation_graphs.py* produces the tables and graphs in Figure 11. The provided *log.json* file contains the data used in the paper.

Usage:
* Before running the experiments, the previously running instance of the Databank should be terminated (e.g. by `killall python3`).
* Run `cd src && python3 ../evaluation/evaluation.py` to run the experiments (note the different base folder!). This can be repeated several times; every run adds 5 data points for LIST and COMPLEX and 25 data points for INSERT, DELETE and VIEW.
* Run `cd evaluation && python3 evaluation_graphs.py` to generate the graphs from *log.json*.