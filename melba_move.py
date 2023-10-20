import pygame
import cv2

import numpy as np
import pasimple
import random
import time

# Set the audio level threshold
audio_threshold = 10.0
# Initialize Pygame
pygame.init()

# Create a Pygame window
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pygame Window")

# Load the PNGs
from PIL import Image

# Open the GIFs
blink1_gif = Image.open("melba_blink/0.gif")
blink2_gif = Image.open("melba_blink/1.gif")
blabber1_gif = Image.open("melba_blabber/0.gif")
blabber2_gif = Image.open("melba_blabber/1.gif")

# Extract the first frame from each GIF
blink1_image = blink1_gif.convert("RGB")
blink2_image = blink2_gif.convert("RGB")
blabber1_image = blabber1_gif.convert("RGB")
blabber2_image = blabber2_gif.convert("RGB")



# Convert the images to Pygame Surfaces
blink1_image = np.array(blink1_image)
blink2_image = np.array(blink2_image)
blabber1_image = np.array(blabber1_image)
blabber2_image = np.array(blabber2_image)
print(blink1_image.shape)

# convert black pixels to green
color_to_replace = np.array([0, 0, 0], dtype=np.uint8)
replacement_color = np.array([0, 255, 0], dtype=np.uint8)

# create a mask of the pixels that are black
def create_mask(image, color_to_replace):
    mask = np.all(image == color_to_replace, axis=-1)
    return mask

# replace the pixels in the mask with the replacement color
def replace_color(image, mask, replacement_color):
    image[mask] = replacement_color
    return image

# create the mask
mask = create_mask(blink1_image, color_to_replace)
# replace the color
blink1_image = replace_color(blink1_image, mask, replacement_color)

# create the mask
mask = create_mask(blink2_image, color_to_replace)
# replace the color
blink2_image = replace_color(blink2_image, mask, replacement_color)

# create the mask
mask = create_mask(blabber1_image, color_to_replace)
# replace the color
blabber1_image = replace_color(blabber1_image, mask, replacement_color)

# create the mask
mask = create_mask(blabber2_image, color_to_replace)
# replace the color
blabber2_image = replace_color(blabber2_image, mask, replacement_color)

# Create a Pygame clock for controlling frame rate
clock = pygame.time.Clock()

# timer for blinking
def random_blink():
    # random blinking

    # random number between 1 and 10
    random_number = random.randint(1, 40)

    if random_number == 1:
        # display blink1
        surface = pygame.surfarray.make_surface(blink2_image)
        # rotate clockwise -90
        surface = pygame.transform.rotate(surface, -90)
        screen.blit(surface, (0, 0))
        # time.sleep(0.5)

pasimple_playback_direction_cfg = pasimple.PA_STREAM_RECORD
pasimple_playback_format_cfg = 3
pasimple_playback_channels_cfg = 1
pasimple_playback_rate_cfg = 40000
pasimple_playback_app_name_cfg = "melba-toast"
pasimple_playback_stream_name_cfg = None
pasimple_playback_server_name_cfg = None
pasimple_playback_device_name_cfg = "alsa_output.pci-0000_0b_00.4.analog-stereo.monitor"

pasimple_cfg_dict = {
        "direction": pasimple_playback_direction_cfg,
        "format": pasimple_playback_format_cfg,
        "channels": pasimple_playback_channels_cfg,
        "rate": pasimple_playback_rate_cfg,
        "app_name": pasimple_playback_app_name_cfg,
        "stream_name": pasimple_playback_stream_name_cfg,
        "server_name": pasimple_playback_server_name_cfg,
        "device_name": pasimple_playback_device_name_cfg,
    }

last = False
audio_playback = pasimple.PaSimple(**pasimple_cfg_dict)
# Initialize PulseAudio context
while True:
    # source_name = 'Virtual_Output.monitor'
    # blit green
    screen.fill((0, 255, 0))
        
    bytes_audio = audio_playback.read(10048)

    if bytes_audio is None:
        break

    # check rms value of audio

    audio_data = np.frombuffer(bytes_audio, dtype=np.int16)
    try:
        rms = np.sqrt(np.mean(np.square(audio_data)))
    except:
        rms = 0.0
    # convert nan to 0.0
    if np.isnan(rms):
        rms = 0.0
    if rms > audio_threshold:
        ran_tr = random.randint(0, 1)
        if ran_tr == 1:
            translate_y = -5
        else:
            translate_y = 0
        print(rms)
        # baseed on last display 0 or 1
        if last:
            surface = pygame.surfarray.make_surface(blabber1_image)
            # rotate clockwise 90
            surface = pygame.transform.rotate(surface, -90)
            
            
            screen.blit(surface, (0, translate_y))
            # screen.blit(surface, (0, 0))
            
        else:
            
            surface = pygame.surfarray.make_surface(blabber2_image)
            # rotate clockwise -90
            surface = pygame.transform.rotate(surface, -90)
            # ran_tr = random.randint(0, 1)
            # if ran_tr == 1:
                # translate_y = -5
            # else:
                # translate_y = 0
            screen.blit(surface, (0, translate_y))
            # screen.blit(surface, (0, 0))
        
        
        

    else:
        # display the png image png_image

        if last:

            surface = pygame.surfarray.make_surface(blink1_image)
            # rotate clockwise -90
            surface = pygame.transform.rotate(surface, -90)
            screen.blit(surface, (0, 0))

        else:
            surface = pygame.surfarray.make_surface(blink1_image)
            # rotate clockwise -90
            surface = pygame.transform.rotate(surface, -90)
            screen.blit(surface, (0, 0))
    last = not last



        # random blinking
    random_blink()

    # print(last)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(12)
    
