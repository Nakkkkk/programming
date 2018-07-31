import tensorflow as tf
import time

N = 10000

W1 = tf.random_normal((N, N))
W2 = tf.random_normal((N, N))
C = tf.matmul(W1, W2)

myconfig = tf.ConfigProto(
    intra_op_parallelism_threads=5 )

start = time.time()

with tf.Session(config=myconfig) as sess:
    sess.run(tf.global_variables_initializer())
    sess.run([C])
    print("Done")
    print("time = {0}".format(time.time() - start))
