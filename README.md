# Battery Thermal Managment System on Digital Twin Feasibility Study

A feasibility study to prove digital twins application for real-time monitoring, prediction and control of a battery's thermal state. Validated via HIL testing on dSPACE hardware, the digital twin will be hosted in the cloud and a Raspberry Pi used to interface the connection. 

<img width="671" height="154" alt="BTM on Digital Twin drawio" src="https://github.com/user-attachments/assets/6f79c625-aff8-4c71-80f0-1f1c24d77fa2" />

- **Battery System - dSPACE:** The 'plant', a real-time model emulated on dSPACE platform that simulates the battery's thermal dynamics and produces sensor data
- **Network Gateway (Raspberry Pi):** The 'edge computing', connected to dSPACES I/O via CAN it facilitates bi-directional communication between the cloud and allows metric measuremnts
- **Digital Twin (Cloud-Hosted):** The 'brain', a system capable of varying functionality from simple feedback control to SOX, predictive control and model training
