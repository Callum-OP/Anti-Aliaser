# How to run
Replace the "LineDrawing.png" file with whatever image you want (keeping the same name - "LineDrawing.png"), then simply run the file as you would any python file, eg
  python -u "main.py"
Although make sure your in the same directory as the file

# About the program
I wanted a program that would apply anti-aliasing to an existing digital line drawing that didn't have anti-aliasing, so I created this simple Python program.

By placing and naming a file "LineDrawing.png" and running the program, it will be modified to have an anti-aliasing effect and the modified version will placed in "output.png". It does not matter if the line drawing is transparent or not as this program will automatically make the final image transparent by removing white space.

This program does not work for coloured images and is only designed for line art.

This program works by thinning the lines in the image and then blending it with itself to create an anti-aliasing effect, it then slightly blurs and darkens the blended result and then overlays it with a 1 pixel line version of the image to ensure there is always at least a 1 pixel line remaning. The image will have any white space removed from it and the semi-transparent pixels will be darkened. The final image is then overlayed over itself to create a stronger/darker line drawing. The result is the final image will likely look more smooth and slightly thinner as if it was drawn with a brush with anti-aliasing as well as be transparent so it is ready to be used.


Below is a before and after image.

<img width="569" alt="Anti-Aliaser" src="https://github.com/user-attachments/assets/5d64b860-0849-4bc8-8ae8-d0ec4f6307d6" />
