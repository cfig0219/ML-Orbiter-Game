# Reinforcement Learning for Spacecraft Orbits 🚀

> **Note:** Before running the programs, please download the project ZIP file. Google Colab cannot display the Pygame GUI window required for the simulation.
> **Google Drive Project Link:** [Access Project Folder](https://drive.google.com/drive/u/1/folders/1W4WUmXCi9fNiQrCzKVU22w2Nz-zeFdQ1)

## 📖 Overview
This project features an autonomous spacecraft's mastery of orbital dynamics around procedurally generated planets. By combining **Fuzzy Logic** and **Neural Networks**, the system implements a reinforcement learning loop that dictates the precise maneuvers required to achieve a stable orbit based on real-time physics parameters.

## 📁 File Descriptions

### `PlanetOrbiter.py`
* **Purpose:** Serves as the **Base Game Engine**.
* **Functionality:** This script contains the core Pygame environment, including the physics engine for gravitational attraction ($G$), collision detection, and the rendering of planetary textures. It allows for manual or scripted flight without the active reinforcement learning training loop.

### `PlanetOrbiterNotebook.ipynb`
* **Purpose:** The **Reinforcement Learning Implementation**.
* **Functionality:** This Jupyter Notebook contains the integrated training environment. It utilizes a **Dynamic Regressor Network** to process state variables—such as gravity, speed, apoapsis, periapsis, and eccentricity—to maximize rewards upon successful orbit achievement.

## 🛠️ Requirements

### Required Environments
* **Anaconda** (Recommended for dependency management)
* **Jupyter Notebook** (To run the RL training session)

### Required Libraries

  pip install pygame numpy matplotlib scikit-fuzzy scikit-learn torch

## 🤖 Technical Implementation
1. **The spacecraft’s autonomous guidance is driven by:**

* **State & Reward System:** Based on crucial orbital mechanics, including **Specific Orbital Energy** and **Semi-Major Axis** calculations.
* **Fuzzy Logic:** Utilized to convert "crisp" physics values into linguistic variables to streamline the decision-making process.
* **Neural Network:** A `Torch`-based architecture that refines maneuver thresholds to minimize loss and optimize the flight path.
