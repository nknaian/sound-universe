from scipy.fftpack.basic import ifft
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
from pygame import mixer
  
# init pygame
mixer.init()

### Get sound to play around with ###

rate, data = wav.read('Wav_868kb.wav')
fft_out = fft(data)
# Instead of using ifft here, make a 1d np array
# based on the coordinates the player is in. (what are the max and min)
# max and min...16-bit PCM -32768 +32767 int16
data = ifft(fft_out)
data = data.astype(np.int16)

samplerate = 44100
wav.write("example.wav", samplerate, data)

# Make sound in pygame
sound = mixer.Sound("example.wav")

# infinite loop
while True:
      
    print("Press 'p' to play the sound")
    query = input("  ")

    if query == 'p':
        # Play the sound
        mixer.Sound.play(sound)