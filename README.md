# Battery Thermal Managment System on Digital Twin Feasibility Study

A feasibility study to prove digital twins application for real-time monitoring, prediction and control of a battery's thermal state. Validated via HIL testing on dSPACE hardware, the digital twin will be hosted in the cloud and a Raspberry Pi used to as gateway between CAN bus and internet. 

<img width="681" height="599" alt="system (1)" src="https://github.com/user-attachments/assets/19861aae-242e-472c-9a13-4db33e2b5341" />

This repository contains code and scripts developed during my internship project on a feasibility study of a cloud-based digital twin for EV battery thermal management (BTM).  
The system integrates a **dSPACE hardware-in-the-loop setup**, a **Raspberry Pi CAN gateway**, and a **Google Cloud–hosted Recursive Least Squares (RLS) estimator**.

## Project Overview
- **Objective:** Evaluate the feasibility of using a cloud-hosted estimator to update the internal resistance parameter (`Rbat`) of a battery in real time and feed it back into a model predictive controller (MPC).
- **Hardware:** dSPACE MicroAutoBox II, Raspberry Pi with CAN HAT.
- **Software:** MATLAB/Simulink, Python (CAN interface, cloud communication), Google Cloud Functions (RLS estimator).

## Repository Contents
- `/edge-node/` — Python scripts for Raspberry Pi CAN communication and cloud API calls.  
- `/cloud-function/` — Cloud Function code for RLS estimator implementation.  
- `/Resources/Final-Test` — Dataset and Jupyter notebook script from final tests

