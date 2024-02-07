import os
from pydub import AudioSegment
import matplotlib.pyplot as plt
from mutagen.flac import FLAC
import hashlib

def get_audio_codec(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()[1:]  # Removing the dot at the beginning

def get_flac_info(file_path):
    def plot_spectrogram(audio):
        plt.specgram(audio.get_array_of_samples(), Fs=audio.frame_rate, cmap='viridis')
        plt.title('Spectrogram')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.show()

    result = {}

    if os.path.isfile(file_path) and file_path.lower().endswith('.flac'):
        audio = AudioSegment.from_file(file_path, format="flac")

        # Plot spectrogram
        plot_spectrogram(audio)

        # Extract other parameters
        result['duration'] = audio.duration_seconds
        result['sample_rate'] = audio.frame_rate
        result['channels'] = audio.channels
        result['bits_per_sample'] = audio.sample_width * 8
        result['bitrate'] = audio.frame_rate * audio.sample_width * 8 * audio.channels / 1000
        result['codec'] = get_audio_codec(file_path)  # Dynamically determine codec
        result['encoding'] = audio.sample_width * 8
        result['tool'] = FLAC(file_path).get('tool', [''])[0]
        result['embedded_cuesheet'] = 'Yes' if 'cuesheet' in FLAC(file_path) else 'No'

        # Calculate MD5 hash of audio data
        with open(file_path, 'rb') as flac_file:
            audio_data = flac_file.read()
            md5_hash = hashlib.md5(audio_data).hexdigest()
            result['audio_md5'] = md5_hash

    else:
        print("Invalid FLAC file path.")

    return result

# Example usage:
flac_file_path = r"C:\Users\ork\Downloads\spam\Petar Dundov - At The Turn Of Equilibrium (2016)(FLAC)(CD)\1-01. Petar Dundov - Then Life.flac"
flac_info = get_flac_info(flac_file_path)
print(flac_info)
