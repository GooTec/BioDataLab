import tensorflow as tf
import random
import numpy as np
import math

# import matplotlib.pyplot as plt

# from tensorflow.examples.tutorials.mnist import input_data

tf.set_random_seed(777)  # reproducibility

train_x = np.genfromtxt ('/Users/taewan/Downloads/ToyData/ToyVar30.csv', delimiter=",")
train_y = np.genfromtxt ('//Users/taewan/Downloads/ToyData/CancerResult.csv', delimiter=",")
# Check out https://www.tensorflow.org/get_started/mnist/beginners for
# more information about the mnist dataset

train_x = train_x[:,~np.isnan(train_x).all(0)]
train_x = train_x[~np.isnan(train_x).all(1)]
train_x = train_x[:,:-1]
train_y = train_y[:-1]
train_x = train_x.transpose()
train_y = train_y.transpose()
cnt_train = len(train_x[1,:])
print(cnt_train)
train_y = np.reshape(train_y, (-1, 1))
train_y

# parameters
learning_rate = 0.001
training_epochs = 3
batch_size = 100
X = tf.placeholder(tf.float32, [None, cnt_train])
Y = tf.placeholder(tf.float32, [None, 1])

W1 = tf.Variable(tf.random_normal([cnt_train, 100]), name='weight1')
b1 = tf.Variable(tf.random_normal([100]), name='bias1')
layer1 = tf.sigmoid(tf.matmul(X, W1) + b1)

W2 = tf.Variable(tf.random_normal([100, 100]), name='weight2')
b2 = tf.Variable(tf.random_normal([100]), name='bias2')
layer2 = tf.sigmoid(tf.matmul(layer1, W2) + b2)

W3 = tf.Variable(tf.random_normal([100, 10]), name='weight3')
b3 = tf.Variable(tf.random_normal([10]), name='bias3')
layer3 = tf.sigmoid(tf.matmul(layer2, W3) + b3)

W4 = tf.Variable(tf.random_normal([10, 1]), name='weight4')
b4 = tf.Variable(tf.random_normal([1]), name='bias4')
hypothesis = tf.sigmoid(tf.matmul(layer3, W4) + b4)

# cost/loss function
cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) *
                       tf.log(1 - hypothesis))

train = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

# Accuracy computation
# True if hypothesis>0.5 else False
predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))
with tf.Session() as sess:
    # Initialize TensorFlow variables
    sess.run(tf.global_variables_initializer())

    for step in range(10000):
        sess.run(train, feed_dict={X: train_x, Y: train_y})
        if step % 1000 == 0:
            print(step, sess.run(cost, feed_dict={
                  X: train_x, Y: train_y}), sess.run([W1, W2]))

    # Accuracy report
    h, c, a = sess.run([hypothesis, predicted, accuracy],
                       feed_dict={X: train_x, Y: train_y})
    print("\nHypothesis: ", h, "\nCorrect: ", c, "\nAccuracy: ", a)
