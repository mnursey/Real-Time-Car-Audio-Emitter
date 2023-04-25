# Real-Time-Car-Audio-Emitter
[Spring 2023] [CSC 484D] [Course Project] - UVic Synthesizer Programming

Presentation Slide Link: https://docs.google.com/presentation/d/14MYn41PeIaqVWwxh4L8cEHkZZcycujDyKeh9A1HltZY/edit?usp=sharing

Youtube Presentation Link - Sampling: https://youtu.be/QNdy--hwCQ0

Youtube Presentation Link - Physical Modelling: https://youtu.be/0-ayraie2ws

## Proposal
Virtual cars in racing video games produce engine sounds that mimic their real life counter parts, and modern electric cars often produce artificial sounds. As the speed (RPM) of the engine varies, the frequencies and amplitude of the engine change. These changes in sound provide information to the driver of the state of their vehicle, pedestrians concerned about their safety may listen for these sounds. Youtuber AngeTheGreat created a virtual engine simulator which supports any kind of engine configuration, this tool produces realistic sounding engine audio. Unfortunately, this project requires a significant amount of processing resources to run at real time, and requires an understanding of ICE (Internal Combustion Engines) to configure. The goal of this project is to create a synthesizer to produce realistic car audio sounds at real time with simplified parameters. The sound produced by the synthesizer will depend on engine RPM. As the project develops the goal is for the synthesizer to support customization and engine presets which produce unique waveforms based on existing internal combustion engines.
 
Some parameters may include:
Number of cylinders
Cylinder size
Engine layout: Inline vs Boxster vs V* (V4, V6, V8, etc) vs Rotary
Engine stroke: 2-Stroke vs 4-Stroke

## Project Description
For our Real Time Car Audio Emmitter project we've decided to implement a few different methods for generating car audio sounds and comparing them. We're going to try a sampling based method, a physically based modeling method. In the resources section there are several papers explaining different methods for designing physically based models.

## Code

In this repository there are attached python notebooks containing code. Please download and run the cells in the notebooks to explore our codebase.

For the loop based car engine audio: \
Please run `python3 LoopBasedCarEngineAudio.py` \
This python code requires the following python libraries installed: 
- numpy
- pyaudio
- pygame
- pygame-widgets

For development we used `Python 3.9+`

## Milestones

- Build sampling based method. Can be verified by generating simple engine sounds.
- Improve features to sampling based method. Can be verified by generating complete engine sounds with high audio quality.
- Research papers about physically based model method. Can be verified by writing out a plat for the physically based model method.
- Build physically based model method. Can be verified by generating simple engine sounds.
- Improve / tune physically based model method. Can be verified by generating complete engine sounds with high audio quality.
- Research 3rd sound generation method.
- Begin writting paper.
- Complete paper.

Worst Case: Get physical based and sampling methods working \
Expected Case: Make sure both physical based and sampling methods are comparable and have a rich set of feature. Sound quality should be high.
Best case: Implement a 3rd sound generation method


## Resources:
AngeTheGreat engine simulator: https://www.youtube.com/@angethegreat https://www.engine-sim.parts/ https://github.com/ange-yaghi/engine-sim 

ICE audio clips: http://www.crankcaseaudio.com/conent 

Examples of audio in racing games: https://youtu.be/R0WYMskS6UM

Tesla Electric cars sounding like ICE cars: https://youtu.be/VLtw-KJBrkQ

Sounds of Formula-E (Electric open wheel race cars): https://youtu.be/OHlqXfG78Rs

Car audio based on Designing Sound writing in SuperCollider: https://en.wikibooks.org/wiki/Designing_Sound_in_SuperCollider/Cars

Sample-based engine noise synthesis using a harmonic synchronous overlap-and-add method : https://hal.science/hal-00661228/file/Sample_based_engine_noise_synthesis_JAGLA_ICASSP12.pdf

Physically informed car engine sound synthesis for virtual and augmented environments : https://ieeexplore.ieee.org/abstract/document/7361287

## Members
Mitchell Nursey \
Sarah Delorme

## Project work distribution
Mitchell : Developed sample based car engine audio, updated github, researched methods for generating car audio, populated resources, setup milestones and project proposal.

Sarah : Developed car engine simulation from the Design Sound book.

## Tech Stack
- Python 3.9+
- Jupyter notebooks


## Loop Based Car Engine Audio Explanation

For the loop based method we load four audio wave files:
- Acceleration Loop
- Deceleration Loop
- Idle Loop
- Wind audio Loop

For the acceleration, deceleration, and idle loop we've taken audio from a Yamaha 24MX motorcycle engine. This engine is a 125cc dirt bike engine. Although this engine isn't from a car, we've choosen this engine as it is mechanically simple, has only a single cylinder, and there is plenty of references online for how this engine should sound. We also have experience hearing a similar  type of engine, which we will use as a comparison later.

For the acceleration, deceleration, and idle samples that are loaded by our Python code, we have edited them to only contain one cycle from the engine. We loaded the original source loops into Audacity, and identified where the engine audio repeats. We only used one cycle in our audio samples as we wanted finer control over the audio sound. We can below that each cycle has a small amount of difference from the previous cycle. This is something we wanted control over.

The acceleration and deceleration samples are identical besides differences in EQ we've applied using Audacity. The acceleration sample is the sound for when the engine throttle is open, while the deceleration sample is for when the engine is closed.

![Screenshot of Engine Audio Looping](/Audio%20Samples/Yamaha_24MX/repeating_loops.PNG "Repeating Cycles of engines audio")

We use a real-time callback based audio stream with pyaudio to play the audio. The audio generation is performed in the callback function.

The adjustable parameters inlude:
- `max_speed`: This is a how many multiples the reference sample can be speedup by. For example, a value of 2 would mean the reference sample can be played back at a maximum of double the speed.
- `min_speed`: This is how many multiples the reference sample can be slowndown by. For example, a value of 0.5 would mean the reference sample can be played back at a minimum of half the speed.
- `idle_speed` : If the engine speed is below this value the idle sample begins to fade in and the acceleration/deceleration loops fade out. Above this value the opposite occurs.
- `accelerate_sound_gain`: How 'loud' the acceleration sample is played back.
- `deaccelerate_sound_gain`: How 'loud' the deceleration sample is played back.
- `idle_sound_gain`: How 'load' the idle sample is played back.
- `speed_variation`: The amount of random variation in the playback speed of the samples from the desired engine speed. This adds in random variation.
- `wind_gain_max`: The maximum 'volume' for the wind sample, this is the value when the engine is at its max speed.
- `wind_gain_min`: THe minimum 'volume' for the wind sample, this is the value when the engine is it its min speed.
- `idle_lerp_rate`: How quickly the engine fades from idle to acceleration / deceleration samples.
- `sample_lerp`: How quickly the engine fades from acceleration to deceleration samples. This value can be changed to change how 'laggy' the engine is.
- `engine_speed` : The speed at which the engine is at. This value determins how much or little the samples are speed up or slowed down. 

The only parameter which can be adjusted at realtime is `engine_speed` using the GUI slider, the rest of the parameters can be adjusted within the code. The GUI slider is displayed using the PyGame library.

As a reference of the audio we're trying to achieve this YouTube video by Aaron Smith 1975 is a good refernce. 

https://youtu.be/G9QmB2Kjhpc

Although the engine in this video isn't identical to the Yamaha 24MX the mechnical behaviour is similar enough to be a valid comparison. In this video the audio recorded with a GoPro camera and contains a lot of wind noise. We've decided to emulate the wind noise by using a wind audio sample. In both the video reference and our sample based method the engine speed increases the wind playback speed and volume increase.

The benefits to the sample based methods include:
- Computationally inexpensive
- Easy to tune, few parameters
- Easy to get audio to sound realistic

Disadvantages: 
- Not very expressive
- Requires recorded samples of engine sounds 
