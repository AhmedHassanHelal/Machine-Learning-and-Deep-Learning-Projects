from mnist import MNIST
import numpy as np
import random

NUM_DIGItS = 10

mndata = MNIST('/home/ahmed/MyWorkspace/Hand Writing Digits Recognizer/samples')

images_train_orig, labels_train_orig = mndata.load_training()
images_test, labels_test_orig = mndata.load_testing()

X_train = np.asarray(images_train_orig).T
Y_ORIG_train = np.asarray(labels_train_orig)
Y_ORIG_train = Y_ORIG_train.reshape((Y_ORIG_train.shape[0], 1)).T

Y_Expected_Train = np.zeros((NUM_DIGItS, Y_ORIG_train.shape[1]))

for i in range(NUM_DIGItS):
    Y_Expected_Train[i,:] = np.isin(Y_ORIG_train, [i]).astype(int)


X_test = np.asarray(images_test).T
Y_ORIG_test = np.asarray(labels_test_orig)
Y_ORIG_test = Y_ORIG_test.reshape((Y_ORIG_test.shape[0], 1)).T

Y_Expected_Test = np.zeros((NUM_DIGItS, Y_ORIG_test.shape[1]))

for i in range(NUM_DIGItS):
    Y_Expected_Test[i,:] = np.isin(Y_ORIG_test, [i]).astype(int)


#m_train = X_train.shape[1]

#m_test = X_test.shape[1]

#image_size = X_train.shape[0]

index = random.randrange(0, len(images_test))

print(mndata.display(images_test[index]))



def sigmoid(z):
    s = 1/(1+np.exp(-z))
    return s



def initialize_with_zeros(dim):    
    w = np.zeros((dim, NUM_DIGItS))#np.random.randn(dim, NUM_DIGItS)*0.001
    b = np.zeros((NUM_DIGItS,1))
    return w, b


def propagate(w, b, X, Y):
    m = X.shape[1]
    Z = np.dot(w.T, X)+b
    A = sigmoid(Z)
    
    cost = ((- 1.0 / m) * np.sum(Y * np.log(A) + (1 - Y) * (np.log(1 - A)), axis = 1)).reshape(NUM_DIGItS, 1)
    
    dw = (1.0 / m) * np.dot(X, (A - Y).T)
    
    db = ((1.0 / m) * np.sum(A - Y, axis = 1) ).reshape(NUM_DIGItS, 1)
    
    cost = np.squeeze(cost)
    
    grads = {"dw": dw,
             "db": db}
    
    return grads, cost


def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost = False):
    costs = []
    
    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)
        dw = grads["dw"]
        db = grads["db"]

        w = w - learning_rate * dw
        b = b - learning_rate * db

        if i % 100 == 0:
            costs.append(cost)
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" % (i, cost))
    
    params = {"w": w,
              "b": b}
    
    grads = {"dw": dw,
             "db": db}
    
    return params, grads, costs



def predict(w, b, X):
    m = X.shape[1]
    Y_prediction = np.zeros((NUM_DIGItS, m))
    w = w.reshape(X.shape[0], NUM_DIGItS)
    A = sigmoid(np.dot(w.T, X) + b)
    
    Y_prediction = (np.sign(A-0.5)+1)/2
    
    return Y_prediction




def model(X_train, Y_train, X_test, Y_test, num_iterations=2000, learning_rate=0.5, print_cost=False):
	w, b = initialize_with_zeros(X_train.shape[0])

	for i in range(num_iterations/20):
		parameters, grads, costs = optimize(w, b, X_train, Y_train, 20, learning_rate, print_cost)

		w = parameters["w"]
		b = parameters["b"]
    
		Y_prediction_test = predict(w, b, X_test)
		Y_prediction_train = predict(w, b, X_train)
		print(num_iterations/20-i)
		print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100))
		print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100))


	d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test, 
         "Y_prediction_train" : Y_prediction_train, 
         "w" : w, 
         "b" : b,
         "learning_rate" : learning_rate,
         "num_iterations": num_iterations}
	
	return d

d = model(X_train, Y_Expected_Train, X_test, Y_Expected_Test, num_iterations = 40, learning_rate = 0.00001, print_cost = False)


my_image = (X_test[:, index]).reshape(X_test.shape[0], 1)
my_predicted_image = predict(d["w"], d["b"], my_image)
print("y = " + str(np.squeeze(my_predicted_image)))

for i in range(NUM_DIGItS):
	if(my_predicted_image[i] == 1):
		print('The number you wrote: ' + str(i))

values_of_w = open("values_of_w.txt", "w")
values_of_w.write(str(d["w"]))
