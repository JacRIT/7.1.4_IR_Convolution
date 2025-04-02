import os
import numpy as np
import scipy.signal as signal
import soundfile as sf

# Define the top-level directory
top_level_dir = "C:\\RIT\\RIT-24-25\\Spring\\3D\\bin_project\\IRGroup2_LR_SWAP"
input_file = os.path.join(top_level_dir, "in", "Jacob_Canedy_Assignment1.wav")  # 12-channel input file

# Speaker positions in 7.1.4 system
positions = [
    "frontleft", "frontright", "frontcenter", "sideleft", "sideright",
    "backleft", "backright", "topfrontleft", "topfrontcenter", "topfrontright",
    "lfe1", "voiceofgod"
]

# Load the input audio
input_signal, fs = sf.read(input_file)
assert input_signal.shape[1] == 12, "Input file must have 12 channels."

# Iterate through each person's directory
for person in os.listdir(top_level_dir):
    person_dir = os.path.join(top_level_dir, person)
    if not os.path.isdir(person_dir):
        continue
    
    # Load impulse responses
    irs = {}
    for pos in positions:
        ir_path = os.path.join(person_dir, f"{pos}.wav")
        if os.path.exists(ir_path):
            irs[pos], _ = sf.read(ir_path)
    
    # Perform convolution for each channel
    binaural_L, binaural_R = np.zeros_like(input_signal[:, 0]), np.zeros_like(input_signal[:, 0])
    for i, pos in enumerate(positions):
        if pos in irs:
            trim_length = fs // 2  # Trim IR to first 0.5 seconds
            left_ir, right_ir = irs[pos][:trim_length, 0], irs[pos][:trim_length, 1]
            binaural_L += signal.convolve(input_signal[:, i], left_ir, mode='same')
            binaural_R += signal.convolve(input_signal[:, i], right_ir, mode='same')
    
    # Normalize
    max_val = max(np.max(np.abs(binaural_L)), np.max(np.abs(binaural_R)))
    if max_val > 0:
        binaural_L *= 0.98 / max_val
        binaural_R *= 0.98 / max_val
    
    # Save output
    out_dir = os.path.join(person_dir, "out")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "binaural_output.wav")
    sf.write(out_file, np.column_stack((binaural_L, binaural_R)), fs)

print("Processing complete.")
