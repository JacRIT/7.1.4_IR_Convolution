import os
import json
import numpy as np
import scipy.signal as signal
import soundfile as sf

# === Load Input File ===
input_file_name = input("Enter test WAV filename (no .wav, in /in): ").strip()
input_file = os.path.join("in", f"{input_file_name}.wav")

input_signal, fs = sf.read(input_file)

# Ensure input is 2D [samples, channels]
if input_signal.ndim == 1:
    input_signal = input_signal[:, np.newaxis]  # mono → shape (n, 1)

num_channels = input_signal.shape[1]

# === Load Channel Map ===
with open("input_channel_map.json", "r") as f:
    channel_map = json.load(f)

index_to_position = {int(k): v for k, v in channel_map.items()}

# === Load IRs and Process ===
ir_group_dir = "IR-directory"
output_base = os.path.join("out", "test")

for person in os.listdir(ir_group_dir):
    person_dir = os.path.join(ir_group_dir, person)
    if not os.path.isdir(person_dir):
        continue

    print(f"Testing IRs for {person}...")

    # Load this person's IRs
    irs = {}
    for pos in index_to_position.values():
        ir_path = os.path.join(person_dir, f"{pos}.wav")
        if os.path.exists(ir_path):
            ir_data, _ = sf.read(ir_path)
            irs[pos] = ir_data
        else:
            print(f"  Skipping missing IR for: {pos}")

    out_dir = os.path.join(output_base, person)
    os.makedirs(out_dir, exist_ok=True)

    for chan_idx in range(num_channels):
        mapped_pos = index_to_position.get(chan_idx)

        for pos, ir_data in irs.items():
            # 🧠 Logic:
            # - For multichannel: use the mapped input channel only
            # - For mono/stereo: apply to all positions

            if num_channels > 2 and pos != mapped_pos:
                continue  # Skip if this IR doesn't match current channel in mapped mode

            # Grab the IR
            trim_len = fs // 2
            left_ir, right_ir = ir_data[:trim_len, 0], ir_data[:trim_len, 1]

            # Grab the input channel
            input_chan = input_signal[:, chan_idx]

            # Convolve
            out_L = signal.convolve(input_chan, left_ir, mode='same')
            out_R = signal.convolve(input_chan, right_ir, mode='same')

            # Normalize
            max_val = max(np.max(np.abs(out_L)), np.max(np.abs(out_R)))
            if max_val > 0:
                out_L *= 0.98 / max_val
                out_R *= 0.98 / max_val

            # Name output
            suffix = f"{pos}_from_channel{chan_idx}.wav" if num_channels > 2 else f"{pos}_from_input_channel{chan_idx}.wav"
            out_path = os.path.join(out_dir, suffix)

            sf.write(out_path, np.column_stack((out_L, out_R)), fs)

print("✅ Test processing complete.")
