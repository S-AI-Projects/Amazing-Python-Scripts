# R29 T017 resize_image runnable example checks

resize_image is defined in Image Manipulation Script image_manipulation.py at line 4.

## Preconditions and Source Anchors
Precondition anchor at line 43: new_size = (800, 600).
Image loading at line 16: image = Image.open(input_image).
Image resizing at line 17: resized_image = image.resize(new_size).
Image saving at line 18: resized_image.save(output_image).

## Decisive State Transition
The decisive transition occurs when image.resize(new_size) creates a new image surface with the target dimensions.
The saved file on disk reflects this exact transition.

## Executable Examples Tested
1. Smallest valid input: new_size = (1, 1). File saved and validated to have dimensions (1, 1).
2. Ordinary input: new_size = (800, 600). File saved and validated to have dimensions (800, 600).
3. Docstring example execution: executes the example documented in code.
