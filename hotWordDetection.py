import JarvisEng
import porcupine as Porcupine
import struct
import time
import pyaudio

library_path = 'lib\\windows\\amd64\\libpv_porcupine.dll'
model_file_path = 'lib\\common\\porcupine_params.pv'
keyword_file_paths = ['assistant_windows.ppn']
sensitivities = [0.5]
handle = Porcupine.Porcupine(library_path, model_file_path, keyword_file_paths=keyword_file_paths, sensitivities=sensitivities)
input_device_index=None

def run():

    def audio_callback(in_data, frame_count, time_info, status):
        pcm = struct.unpack_from("h" * handle.frame_length, in_data)
        result = handle.process(pcm)
        if result:
            print("hotWord detected")
            print(result)
            pass
        return None, pyaudio.paContinue

    try:
        pa = pyaudio.PyAudio()
        sample_rate = handle.sample_rate
        num_channels = 1
        audio_format = pyaudio.paInt16
        frame_length = handle.frame_length

        audio_stream = pa.open(
            rate=sample_rate,
            channels=num_channels,
            format=audio_format,
            input=True,
            frames_per_buffer=frame_length,
            input_device_index=input_device_index,
            stream_callback=audio_callback)

        audio_stream.start_stream()

        while True:
            time.sleep(0.1)
    except Exception:
        None

run()

# while True:
#     pcm = get_next_audio_frame()
#     keyword_index = handle.process(pcm)
#     if keyword_index >= 0:
#         print("It works?")
#         pass