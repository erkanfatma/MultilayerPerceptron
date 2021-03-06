

import numpy as np
import matplotlib.pyplot as plt
import random
import os, sys

TrainDataFile = 'Ricetrain.csv'
TestDataFile = "Ricetest.csv" 
numberNeuronsOutputLayer= 4
numberNeuronsHiddenLayer = 5

CLASSES = 4
EPOCHS = 1000
NUMBER_LAYER = 2
LEARNING_RATE = 0.2

class Neuron: 
    __slots__= ( 'num_inputs','num_outputs','weights','input','activation' )

    def __init__(self,inputs,outputs): 
        self.num_inputs=inputs
        self.num_outputs=outputs
        self.weights=self.__init_weight__(self.num_inputs)
        self.input=None
        self.activation=None

    def __init_weight__(self,num_input): 
        weights=[]
        for i in range(num_input):
            weights.append(random.uniform(-1, 1))
        weights=np.array(weights)
        return weights

    def __sigmoid__(self,input): 
        return 1/(1+np.exp(-1*input))

    def __activation__(self,inputs): 
        activation=0
        for counter in range(self.num_inputs):
            activation+=self.weights[counter]*inputs[counter]
        return self.__sigmoid__(activation)

    def response(self,inputs): 
        self.input=inputs
        activation=self.__activation__(inputs)
        self.activation=activation
        return activation

    def get_weights(self): 
        return self.weights


    def set_weights(self,weights): 
        self.weights=weights

class Layer: 
    __slots__= ( 'num_inputs','num_outputs','num_neurons','neurons' )

    def __init__(self,num_inputs=1,num_outputs=1,num_neuron=1): 
        self.num_inputs=num_inputs
        self.num_outputs=num_outputs
        self.num_neurons=num_neuron
        self.neurons=self.__init_neurons(num_neuron,num_inputs,num_outputs)

    def __init_neurons(self,num_neurons,inputs,outputs): 
        neurons=[]
        for _ in range(num_neurons):
            neurons.append(neuron(inputs,outputs))
        return neurons

    def response(self,inputs): 
        response=[]
        for neuron in self.neurons:
            response.append(neuron.response(inputs))
        return response

    def get_neurons(self): 
        return self.neurons

    def get_num_neurons(self): 
        return self.num_neurons

class MultiLayerPerceptron: 
    __slot__= ( 'network' )
    def __init__(self,num_input,num_output): 
        a_hidden_layer = layer(num_input, numberNeuronsHiddenLayer + 1, numberNeuronsHiddenLayer)
        a_Output_layer = layer(numberNeuronsHiddenLayer + 1, num_output, numberNeuronsOutputLayer)
        self.network=list([a_hidden_layer,a_Output_layer])

    def forward_prop(self,input): 
        activation=input
        for layer in range(NUMBER_LAYER):
            activation=self.network[layer].response(activation)
            if layer == 0:
                activation.insert(0,1)
        return activation



    def network_update(self,weights): 
        for layer_counter in range(len(self.network)):
            neurons=self.network[layer_counter].get_neurons()
            for neuron_counter in range(len(neurons)):
                neurons[neuron_counter].set_weights(weights[layer_counter][neuron_counter])

    def get_netWork_weights(self): 
        weights=[]
        for layer in self.network:
            weights.append([])
            for neuron in layer.get_neurons():
                weights[-1].append(neuron.get_weights())
        return weights

  

def back_prop(mlp, old_weight,error): 
    net_output_layer=mlp.network[-1] # 1 output layer
    output_neurons=net_output_layer.get_neurons()
    previous_delta=[]
    for neuron_counter in range(len(output_neurons)): #
        activation=output_neurons[neuron_counter].activation
        input=output_neurons[neuron_counter].input #list
        dsigmoid = activation*(1-activation)#[ acti * (1 - acti) for acti in activation] # 2 sigmoid
        delta = error[neuron_counter]*dsigmoid#[ err * dsig for err, dsig in zip(error, dsigmoid)] # 2 delta
        dw = [ LEARNING_RATE * delta* inp for inp in input]  # will be a dot product in future
        old_weight[-1][neuron_counter]+=dw #temperary
        previous_delta.append(delta)

    net_hidden_layer = mlp.network[-2]  # 2nd layer
    hidden_neurons = net_hidden_layer.get_neurons() # 3 neuron
    output_weights = []
    for neu in output_neurons:
        output_weights.append( neu.get_weights() ) # 2 list of 4 element each

    hidden_delta = []
    for neuron_counter in range(len(hidden_neurons)):  # 3 neurons
        acti = hidden_neurons[neuron_counter].activation  # 1 activation
        input = hidden_neurons[neuron_counter].input  # 3 elements
        delta = 0
        for delta_counter in range(len(previous_delta)):
            delta += previous_delta[delta_counter] * \
                    output_weights[delta_counter][neuron_counter + 1]
        hidden_delta.append(delta * acti * (1 - acti))
        dw = [LEARNING_RATE * hidden_delta[neuron_counter] * inp for inp in
              input]
        old_weight[-2][neuron_counter] += dw  # temperary
    return old_weight

def load_dataset(file_name): 
    data=[]
    with open(file_name) as data_file:
        for line in data_file:
            line_list=line.strip().split(",")
            data.append([])
            data[-1].append(float(1))
            data[-1].append(float(line_list[0]))
            data[-1].append(float(line_list[1]))
            if float(line_list[2]) == 1.0:
                data[-1].extend([float(1),float(0),float(0),float(0)])
            if float(line_list[2]) == 2.0:
                data[-1].extend([float(0),float(1),float(0),float(0)])
            if float(line_list[2]) == 3.0:
                data[-1].extend([float(0),float(0),float(1),float(0)])
            if float(line_list[2]) == 4.0:
                data[-1].extend([float(0),float(0),float(0),float(1)])

    data=np.array(data)
    label = data[:, 3:7]
    attributes = data[:, 0:3]
    return attributes,label

def gradient_descent(network, data_file): 
    #loading data
    attributes,label=load_dataset(data_file)

    #initalizing sum of square error
    SSE_History=[] #list for storing sse after each epoch
    num_samples=attributes.shape[0]
    epochs = int(sys.argv[2])

    wt_file = WEIGHTS_FILE + "_" + str(epochs) + ".csv"
    if os.path.isfile(wt_file):
        os.remove(wt_file)

    for epoch in range(epochs):
        SSE = 0
        new_weight=network.get_netWork_weights()
        for sample in range(num_samples):
            prediction=network.forward_prop(attributes[sample])
            error=[]
            for bit_counter in range(len(label[sample])):
                error.append(label[sample][bit_counter] - prediction[bit_counter])
            for bit_error in error:
                SSE+=(bit_error)**2
            new_weight=\
            back_prop(network, new_weight,error)
        network.network_update(new_weight)
        #storing the Sum of squre error after each epoch
        SSE_History.append(SSE)
        write_csv(network)
        print("After epoch "+str(epoch+1)+ "  SSE: "+str(SSE ))
    # write_csv(network)
    return network, SSE_History


 
def SSE_vs_epoch_curve(figure, loss_matrix): 
    loss__curve = figure.add_subplot(111)
    loss__curve.plot(loss_matrix, label='Training')
    loss__curve.set_title("SSE vs Epochs")
    loss__curve.set_xlabel("Epochs count")
    loss__curve.set_ylabel("SSE")
    loss__curve.legend()

def main():  
    network = MLP(3, 4)
    trained_network,SSE_History = gradient_decent(network, sys.argv[1])
    figure = plt.figure()
    SSE_vs_epoch_curve(figure, SSE_History)
    figure.show()
    plt.show()

if __name__=="__main__":
    main()
