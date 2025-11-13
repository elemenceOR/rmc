# Matrix Calculator

A small GUI utility for computing 4x4 translation, rotation and transformation matrices.

This repository contains a simple Tkinter-based app (`gui.py`) that helps build 4x4 transformation matrices from translation (x, y, z) and Euler rotations (degrees around X, Y, Z). It shows the translation matrix, rotation matrices (X, Y, Z), the combined transformation matrix, and its inverse (if invertible).

## Prerequisites

- Python 3.8+ (Tkinter is part of the standard library on most platforms)
- numpy

Install numpy with pip if you don't have it:

```bash
pip install numpy
```

On Debian/Ubuntu you may need:

```bash
sudo apt-get install python3-tk
```

## Usage

Run the GUI:

```bash
python3 gui.py
```

- Enter translation values (x, y, z) and rotation angles (degrees) for X, Y, Z.
- Click `Compute` to calculate and display the matrices.
- Click `Copy to Clipboard` to copy the last output shown in the text area.
- Click `Clear` to reset inputs to zero and clear the output area.

## Files

- `gui.py` - Main Tkinter GUI application for matrix calculations.
- `matrix.ipynb` - Jupyter notebook (related work / examples).

## Notes

- The GUI uses `tkinter` and `ttk` for the interface and `numpy` for matrix math.
- If the transformation matrix is singular (non-invertible), the inverse will be reported as unavailable.

If you'd like, I can add a quick `requirements.txt`, a basic license, or CI to run linting/tests. 
