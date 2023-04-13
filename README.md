# Real-Time-Car-Audio-Emitter
[Spring 2023] [CSC 484D] [Course Project] - UVic Synthesizer Programming

## Proposal
Virtual cars in racing video games produce engine sounds that mimic their real life counter parts, and modern electric cars often produce artificial sounds. As the speed (RPM) of the engine varies, the frequencies and amplitude of the engine change. These changes in sound provide information to the driver of the state of their vehicle, pedestrians concerned about their safety may listen for these sounds. Youtuber AngeTheGreat created a virtual engine simulator which supports any kind of engine configuration, this tool produces realistic sounding engine audio. Unfortunately, this project requires a significant amount of processing resources to run at real time, and requires an understanding of ICE (Internal Combustion Engines) to configure. The goal of this project is to create a synthesizer to produce realistic car audio sounds at real time with simplified parameters. The sound produced by the synthesizer will depend on engine RPM. As the project develops the goal is for the synthesizer to support customization and engine presets which produce unique waveforms based on existing internal combustion engines.
 
Some parameters may include:
Number of cylinders
Cylinder size
Engine layout: Inline vs Boxster vs V* (V4, V6, V8, etc) vs Rotary
Engine stroke: 2-Stroke vs 4-Stroke

## Project Description
For our Real Time Car Audio Emmitter project we've decided to implement a few different methods for generating car audio sounds and comparing them. We're going to try a sampling based method, a physically based modeling method, and possibly one more. In the resources section there are several papers explaining different methods for designing physically based models.

## Code

In this repository there are attached python notebooks containing code. Please download and run the cells in the notebooks to explore our codebase.

## Milestones

- Build sampling based method. Can be verified by generating simple engine sounds.
- Improve features to sampling based method. Can be verified by generating comple engine sounds with high audio quality.
- Research papers about physically based model method. Can be verified by writing out a plat for the physically based model method.
- Build physically based model method. Can be verified by generating simple engine sounds.
- Improve / tune physically based model method. Can be verified by generating comple engine sounds with high audio quality.
- Research 3rd sound generation method.
- Begin writting paper.
- Complete paper.

Worst Case: Get physical based and sampling methods working \
Expected Case: Make sure both physical based and sampling methods are comparable and have a rich set of feature. Sound quality should be high.
Best case: Implement a 3rd sound generation method

Mitchell will be getting the sampling based method complete then helping Sarah complete the physical based method. Both members will equally work on the project report.

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
Sarah Chasauce
 
## Tech Stack
Python 3.10
Jupyter notebooks

