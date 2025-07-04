Purpose: This program calculates equivalent elastic properties for thick perforated plates with a square pentration pattern (e.g.: tubesheets).

It is based off Tables B.2 and 4.2 of Thomas Slot's 1972 dissertation titled "Stress Analysis of Thick Perforated Plates" (included for reference).

The subscript "p" denotes the in-plane directions—i.e., a Cartesian plane parallel with the the plate.

The subscript "z" denotes the transverse direction—i.e., the direction of the plate's thickness.

This program outputs the ratio of the orthotropic-to-isotropic stiffness—i.e., (Eₚ or Ez)/E, where E is the isotropic Elastic Modulus. For use in finite element analysis (FEA), you must multiply these calculated ratios by the material's Elastic (Young's) Modulus.

Status: In-progress as of 03 July 2025
