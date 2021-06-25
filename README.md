## Multilayer Perceptron
Perceptron is the first generation and basic building block of neural networks and it is a simply computational model. There are two kinds of perceptron models. One of them is single layer perceptron and the other one is multilayer perceptron. The first perceptron model contains just input layer and output layer. There are no hidden layers in this model. The difference between the single layer perceptron and multilayer perceptron is that the multilayer perceptron contains hidden layers. The perceptron models consist of different parts such as input values, weight & bias, net sum and activation function.
Multilayer perceptron was designed to solve XOR problem. It is used to classify and generalize the data. The structure is shown in the figure below.

![alt text](https://github.com/erkanfatma/MultilayerPerceptron/blob/main/img/perceptron.png)

Multilayer perceptron can contain more than one hidden layer. The number of hidden layers can be changed depend on the problem. Every element after a calculation connected to other neurons. Different activation functions are used for the model. Sigmoid, tang, linear, threshold and hard limiter functions are most used mathematical functions.
In this assignment, I worked on basic of neural network, Multilayer perceptron, as well as an algorithm that responsible for its learning called as backpropagation. This kind of neural network model has served as a basic for complex models existing today such as Convolutional Neural networks. The idea behind the backpropagation algorithm is based on error calculation in another saying loss calculation. It states that the calculation of error between network prediction and the real value. Then, it recalculates all weights values from the last layer to the first layer. The main aim of this steps to decrease the error of neural network.
Backpropagation algorithm consists of some steps:
1. Define all weights with small values that are random.
2. Feed the data into the model. Figure out the value of error function. Compare the value with expected output. It is the most important point that the error function is differentiable.
3. To decrease error, the gradient of error function with respect to each weight is calculated. Gradient vector indicates the direction of highest increase of a function. If we want to move the weights in the direction of highest decrease of error function, we take the opposite direction of the gradient vector.
4. After calculating the gradient vector, every weight is updated in an iterative way.
5. These steps are recalculated until the error becomes lower than a certain established threshold. After algorithm ends, the model is well trained.
