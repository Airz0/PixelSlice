# PixelSlice
A 2 player python game that uses OpenCV to make your hands from the live feed of a camera the controllers in order to slice 
fruits that appear on the screen to accumulate points. Think of it as human fruit ninja, waving your hands to cut the fruit.

The window size may be unusual as I created this game with the purpose of running on an Adafruit 64x64 rgb led display panel, 
basically I had the game running and the physical hardware components all hooked up on a Raspberry Pi 3b+. The Pi would run
headless and the display panel would mirror the desktop environment of the Pi, then by fitting the resolution and window size
to match the Pi would make the game be displayed across the entire panel.

It was originally on a Pi4 which would have been beneficial as it was faster and could've rendered the game better and less
laggy, but the libraries required for the display panel to mirror the desktop environment were not compatible with the Pi4.

The game however, can still be played as long as a webcam or camera is detected (you might need to tweak the config for your
specific live feed).

I have unfortunately lost the assets for this game so probably isn't playable unless you add in your own.
