import wave
import os


def trim_and_merge_wav_files(input_folder='downloads', output_file='merged_audio.wav', duration=30):
    # Check the output file exists or not
    if os.path.exists(output_file):
        os.remove(output_file)

    output_wave = None

    try:
        for filename in os.listdir(input_folder):
            if filename.endswith('.wav'):
                file_path = os.path.join(input_folder, filename)

                # Open the .wav file
                with wave.open(file_path, 'rb') as wav_file:
                    print(f"Processing {file_path}")

                    # Get audio parameters
                    params = wav_file.getparams()
                    n_channels, sampwidth, framerate, n_frames = params[:4]

                    # Calculate number of frames for the desired duration
                    frames_to_copy = int(framerate * duration)

                    # Read frames from the input .wav file
                    frames = wav_file.readframes(frames_to_copy)

                    # Initialize output file on the first run
                    if output_wave is None:
                        output_wave = wave.open(output_file, 'wb')
                        output_wave.setparams((n_channels, sampwidth, framerate, 0, 'NONE', 'not compressed'))

                    # Write frames to the output file
                    output_wave.writeframes(frames)

                    print(f"Added {filename} to the merged file.")

        print(f"Combined audio saved as {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if output_wave is not None:
            output_wave.close()


if __name__ == "__main__":
    trim_and_merge_wav_files()
