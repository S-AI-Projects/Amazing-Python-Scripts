# FlappyBird
This repository contains the implementation of two OpenAI Gym environments for the Flappy Bird game. The implementation of the game's logic and graphics was based on the FlapPyBird project.<br>

### In this flappy.py file I train the Neural Network model with reinforcement learning approach.
## Performance of trained Agent
https://user-images.githubusercontent.com/51924622/121337387-1dca1080-c93a-11eb-9b9f-61bf00bc327f.mp4 

<br>
To check the performance and visualize the agent uncomment the agent.perform() and comment the agent.train() in the flappy.py file. <br>
if __name__ == '__main__':<br>
    &nbsp; agent = DQNAgent()<br>
    &nbsp; #agent.train()<br>
    &nbsp; agent.perform()<br>
    
    
### Perform Function:<br>

![Capture1](https://user-images.githubusercontent.com/51924622/121318965-5f9e8b00-c929-11eb-86d3-96ea6abb43b6.PNG)

## Train the Agent
 For train the agent uncomment the agent.train() in the .py file.<br>
 if __name__ == '__main__':<br>
    &nbsp; agent = DQNAgent()<br>
    &nbsp; agent.train()<br>
    &nbsp; #agent.perform()<br>
 
 ### Train Function:<br>
![Capture](https://user-images.githubusercontent.com/51924622/121318915-52819c00-c929-11eb-9062-cf8e6ce1c795.PNG)<br>

### After training the model is saved by name "flappybrain.h5" shown in this repository.<br>
## Requirements:
- flappy-bird-gym
- numpy
- tensorflow 
### Fork and Run the flappy.py file to see the result.

## NeuralNetwork worked example

`NeuralNetwork(input_shape, output_shape)` builds and compiles a model; it does not train the model. Source lines 20–32 define the model construction. For a four-value state and two possible actions, the first three dense layers produce intermediate vectors of widths 512, 256, and 64, and the final layer produces two linear action scores. The numeric scores depend on the model's initialized or trained weights, so the example reports the prediction shape rather than treating arbitrary scores as expected values.

<!-- runnable example -->
```python
from Flappy import NeuralNetwork

input_shape = (4,)
output_shape = 2
state = [[0.25, 0.75, 0.5, 0.0]]
model = NeuralNetwork(input_shape, output_shape)
dense_widths = [layer.units for layer in model.layers if getattr(layer, "units", None) is not None]
q_values = model.predict(state, verbose=0)
print("state:", state)
print("dense widths:", dense_widths)
print("model output shape:", model.output_shape)
print("Q-value shape:", (len(q_values), len(q_values[0])))
print("loss:", model.loss)
```

After the Keras model summary, the example prints (the numeric Q-values are intentionally not displayed):

```text
state: [[0.25, 0.75, 0.5, 0.0]]
dense widths: [512, 256, 64, 2]
model output shape: (None, 2)
Q-value shape: (1, 2)
loss: mse
```

Run `python3 work/R29-T047/check.py` to execute this exact code block with mocked Keras builders, assert its displayed output, and check the smallest one-feature shape alongside the ordinary four-feature shape. The runner does not require TensorFlow, Gym, a game window, or external files.

