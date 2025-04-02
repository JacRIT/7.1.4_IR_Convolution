# Binaural Convolution Processing

## Setup

`pip install -r requirements.txt`

## File Structure Overview

The **top-level directory** contains multiple **subdirectories**, each representing a person (e.g., `Person1`, `Person2`, etc.). Each **person's directory** contains:

### Impulse Response Files (IRs)

- A set of **stereo `.wav` files** that correspond to the **7.1.4 channel speaker configuration**.
- The file names correspond to the positions in a 7.1.4 surround system:
  - `frontleft.wav`, `frontright.wav`, `frontcenter.wav`
  - `sideleft.wav`, `sideright.wav`
  - `backleft.wav`, `backright.wav`
  - `topfrontleft.wav`, `topfrontcenter.wav`, `topfrontright.wav`
  - `lfe1.wav` (low-frequency effects channel)
  - `voiceofgod.wav` (likely an overhead source)

### "out" Directory

- This subdirectory will store the **binaural output** after processing.

### "in" File (Located in the Top-Level Directory)

- A **12-channel `.wav` file** that serves as the input.
- This file will be **convolved** with the **impulse response files** from each person's folder to generate personalized binaural audio.

## Objective

- The program should iterate through each **person's directory**, access their **7.1.4 stereo impulse response `.wav` files**, and perform convolution with the **12-channel input file** from the `"in"` directory.
- The resulting **binaural output** should be stored in each **person's `"out"` directory**.

## Usage Instructions

1. Place the **12-channel input `.wav` file** inside the `"in"` directory.
2. Organize each person's impulse responses inside their respective subdirectories.
3. Run the Python script to perform convolution and generate binaural audio.
4. The output files will be saved inside each person's `"out"` directory.

## Convolution Method

- The script uses **Scipy's `signal.convolve` function** to convolve the input file with the impulse responses.
- Impulse responses are trimmed to **0.5 seconds** to remove irrelevant tail noise.
- The output is **normalized** before being saved.

## Running the Script

```sh
python binaural_convolution.py
```
