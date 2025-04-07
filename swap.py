import os
import wave

# Define the top-level directory
TOP_LEVEL_DIR = "IR-directory"

def swap_channels(file_path):
    with wave.open(file_path, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())
    
    # Ensure it's a stereo file (2 channels)
    if params.nchannels != 2:
        print(f"Skipping {file_path} (not stereo)")
        return

    # Swap left and right channels
    swapped_frames = bytearray()
    for i in range(0, len(frames), 4):  # Each frame has 4 bytes (16-bit stereo)
        swapped_frames.extend(frames[i+2:i+4])  # Right channel
        swapped_frames.extend(frames[i:i+2])    # Left channel

    # Write back the modified data
    with wave.open(file_path, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(swapped_frames)


def process_directory(top_dir):
    for root, _, files in os.walk(top_dir):
        for file in files:
            if file.lower().endswith(".wav"):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                swap_channels(file_path)

if __name__ == "__main__":
    process_directory(TOP_LEVEL_DIR)
