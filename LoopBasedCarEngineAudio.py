import numpy as np
import math
import pyaudio

import time
import wave
import random

import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


def load_wavefile(filename):
  # Open wave file
  wave_file = wave.open(filename, 'rb')

  # Get parameters
  nchannels = wave_file.getnchannels()
  sampwidth = wave_file.getsampwidth()
  framerate = wave_file.getframerate()
  nframes = wave_file.getnframes()

  # Read wave data
  wave_data = wave_file.readframes(nframes)

  # Convert wave data to numpy array
  if sampwidth == 2:
    # 16-bit samples are stored as signed integers
    wave_data = np.frombuffer(wave_data, dtype=np.int16)
    print("16 int") # ensure type is correct
  elif sampwidth == 4:
    # 32-bit samples are stored as floats
    wave_data = np.frombuffer(wave_data, dtype=np.int32)
    print("32 float") # ensure type is correct

  # If stereo, average the channels
  if nchannels == 2:
    wave_data = np.mean(wave_data.reshape((-1, 2)), axis=1)
  
  return wave_data, framerate

# Load wave file
yamaha_audio, srate = load_wavefile('./Audio Samples/Yamaha_24MX/Yamaha_24MX_Single_Repeat_1.wav')
yamaha_audio_deaccelerate, srate = load_wavefile('./Audio Samples/Yamaha_24MX/Yamaha_24MX_Single_Repeat_deacceleration_2.wav')
yamaha_audio_idle_loop, srate = load_wavefile('./Audio Samples/Yamaha_24MX/Yamaha_24MX_Idle_Loop.wav')

wind_audio = load_wavefile('./Audio Samples/wind_loop.wav')[0]

global_time = 0.0

frame_clock = 0.0
max_speed = 1.25
min_speed = 0.9
idle_speed = 0.92
engine_speed = min_speed

speed = min_speed
speed_variation = 0.001

accelerate_sound_gain = 1.1
deaccelerate_sound_gain = 0.75
idle_sound_gain = 0.4

sample_lerp = 1.0 # a value of 1 is acceleration only, a value of 0 is deacceleration only. 0.5 is 50% each
sample_lerp_rate = 0.1

idle_lerp = 0.0
idle_lerp_rate = 0.0001

wind_gain_max = 0.95
wind_gain_min = 0.3

prev_engine_speed = min_speed

def interpolate(minY : float, maxY : float, minX : float, maxX : float, x : float):
    return minY + ((x - minX) * (maxY - minY) / (maxX - minX))

def clamp01(number : float):
    return max(min(number, 1.0), 0.0)

# Define callback for playback
def callback(in_data, frame_count, time_info, status):

    global global_time
    global frame_clock
    global yamaha_audio
    global sample_lerp
    global speed_variation
    global wind_audio
    global wind_gain_max
    global wind_gain_min
    global idle_sound_gain
    global idle_lerp
    global idle_lerp_rate
    global engine_speed

    data = np.zeros(frame_count).astype(np.int16) # ensure type is correct

    for i in range(frame_count):

        # Handle lerping between samples
        if  engine_speed - prev_engine_speed < 0:
            sample_lerp -= sample_lerp_rate
        else:
            sample_lerp += sample_lerp_rate

        # Clamp sample lerp between 0 and 1
        sample_lerp = clamp01(sample_lerp)

        # We lerp between the two samples when because when we start deaccelerating we don't want to create a popping effect
        audio_sample = interpolate(yamaha_audio_deaccelerate * deaccelerate_sound_gain, yamaha_audio * accelerate_sound_gain, 0.0, 1.0, sample_lerp)

        if engine_speed < idle_speed:
            idle_lerp -= idle_lerp_rate
        else:
            idle_lerp += idle_lerp_rate
            
        # Clamp idle lerp between 0 and 1
        idle_lerp = clamp01(idle_lerp)

        # Add a little bit of randomness to the engine RPM
        engine_speed += speed_variation * (random.random() - 0.5)

        # Add engine sound
        frame_lower = math.floor(frame_clock)
        frame_upper = math.ceil(frame_clock)

        lower_to_upper_ratio = frame_clock - math.floor(frame_clock)

        lower_value = audio_sample[frame_lower % yamaha_audio.shape[0]]
        upper_value = audio_sample[frame_upper % yamaha_audio.shape[0]]

        interpolated_value = lower_value + (upper_value - lower_value) * lower_to_upper_ratio

        data[i] += interpolated_value * idle_lerp
        data[i] += yamaha_audio_idle_loop[frame_lower % yamaha_audio_idle_loop.shape[0]] * idle_sound_gain * (1.0 - idle_lerp)

        # Add wind sound
        # Wind gain is based off of speed, more speed -> more wind
        wind_gain = wind_gain_min + (wind_gain_max - wind_gain_min) * ((engine_speed - min_speed) / (max_speed - min_speed))
        data[i] += wind_audio[frame_lower % wind_audio.shape[0]] * wind_gain

        # Increase frame clock
        frame_clock += engine_speed

        # Increase global time
        global_time += 1.0 / srate

    return (data, pyaudio.paContinue)


# Setup pygame window
pygame.init()
win = pygame.display.set_mode((1000, 600))

# Create slider
slider = Slider(win, 200, 100, 600, 40, min=min_speed, max=max_speed, step=0.0001, initial=0.9)
# Create output textbox
output = TextBox(win, 100, 100, 50, 50, fontSize=24)

output.disable()  # Act as label instead of textbox

# Instantiate PyAudio and initialize PortAudio system resources
p = pyaudio.PyAudio()

# Open stream using callback
stream = p.open(format=pyaudio.paInt16, # ensure type is correct
                channels=1,
                rate=srate,
                output=True,
                stream_callback=callback)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

    if run:
        win.fill((255, 255, 255))

        output.setText('{0:.2f}'.format(slider.getValue()))
        engine_speed = slider.getValue()
        pygame_widgets.update(events)
        pygame.display.update()

    time.sleep(0.05)

# Close the stream 
stream.close()

# Release PortAudio system resources
p.terminate()