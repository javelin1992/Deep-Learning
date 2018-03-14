import tensorflow as tf
import pickle
import numpy as np
from AMSGrad.AMSGrad import AMSGrad
train_images=np.load('train_images.pk')
train_label=np.load('train_label.pk')
train_label=np.expand_dims(train_label,axis=1)
tf.reset_default_graph()



def get_batch(images,labels,batch_size,epoch):
    num=images.shape[0]
    num_batch=np.ceil(num/batch_size)
    np.random.seed(epoch)
    images=np.random.permutation(images)
    np.random.seed(epoch)
    labels=np.random.permutation(labels)

    for i in range(int(num_batch)):
        if i<(int(num_batch-1)):
            image=images[i*batch_size:(i+1)*batch_size,:,:,:]
            label=labels[i*batch_size:(i+1)*batch_size,:]
            yield image,label
        else:
            image=images[i*batch_size:,:,:,:]
            label=labels[i*batch_size:,:]
            yield image,label

def inception_block(input_data,num_conv1,num_conv2,num_pool,num_conv3,
                   num_conv4,num_conv5,num_conv6,is_train):
    initializer=tf.variance_scaling_initializer()
    conv1=tf.layers.conv2d(input_data,num_conv1,(1,1),strides=(1,1),padding='same',kernel_initializer=initializer,activation=tf.nn.relu)
    # conv1=tf.layers.batch_normalization(conv1,training=is_train)
    conv2=tf.layers.conv2d(input_data,num_conv2,(1,1),strides=(1,1),padding='same',kernel_initializer=initializer,activation=tf.nn.relu)
    # conv2=tf.layers.batch_normalization(conv2,training=is_train)
    max_pool=tf.layers.max_pooling2d(input_data,(2,2),strides=(1,1),padding='same')
    max_pool=tf.layers.batch_normalization(max_pool,training=is_train)
    conv3=tf.layers.conv2d(input_data,num_conv3,(1,1),strides=(1,1),padding='same',kernel_initializer=initializer,activation=tf.nn.relu)
    # conv3=tf.layers.batch_normalization(conv3,training=is_train)
    conv4=tf.layers.conv2d(conv1,num_conv4,(3,3),strides=(1,1),padding='same', kernel_initializer=initializer,activation=tf.nn.relu)
    # conv4=tf.layers.batch_normalization(conv4,training=is_train)
    conv5=tf.layers.conv2d(conv2,num_conv5,(2,2),strides=(1,1),padding='same',kernel_initializer=initializer,activation=tf.nn.relu)
    # conv5=tf.layers.batch_normalization(conv5,training=is_train)
    conv6=tf.layers.conv2d(max_pool,num_conv6,(1,1),strides=(1,1),padding='same',kernel_initializer=initializer,activation=tf.nn.relu)
    # conv6=tf.layers.batch_normalization(conv6,training=is_train)


    output_tensor=tf.concat([conv3,conv4,conv5,conv6],3)
    output_tensor=tf.layers.batch_normalization(output_tensor,training=is_train)
    # output_tensor=tf.layers.dropout(output_tensor,rate=0.2,training=is_train)

    return output_tensor

main_graph=tf.Graph()
initial=tf.variance_scaling_initializer()
with main_graph.as_default():

    input_images=tf.placeholder(tf.float32,[None,75,75,3])
    # input_angle=tf.placeholder(tf.float32,[None,1])
    input_label=tf.placeholder(tf.float32,[None,1])
    is_train=tf.placeholder(tf.bool)

    with tf.name_scope('conv_block_1'):
        conv_1=tf.layers.conv2d(input_images,32,[2,2],strides=(1,1),kernel_initializer=initial,padding='same',activation=tf.nn.relu)
        # conv_1=tf.layers.batch_normalization(conv_1,training=is_train)
        # conv_2=tf.layers.conv2d(conv_1,32,(2,2),strides=(1,1),kernel_initializer=initial,padding='same',activation=tf.nn.relu)
        # conv_2=tf.layers.batch_normalization(conv_2,training=is_train)
        max_pool_1=tf.layers.max_pooling2d(conv_1,(3,3),(2,2),padding='same')
        # max_pool_1=tf.layers.dropout(max_pool_1,rate=0.2,training=is_train)
        max_pool_1=tf.layers.batch_normalization(max_pool_1,training=is_train)
    with tf.name_scope('conv_block_2'):
        conv_3=tf.layers.conv2d(max_pool_1,64,(2,2),strides=(1,1),kernel_initializer=initial,padding='same',activation=tf.nn.relu)
        # conv_3=tf.layers.batch_normalization(conv_3,training=is_train)
        # conv_4=tf.layers.conv2d(conv_3,64,(2,2),strides=(1,1),kernel_initializer=initial,padding='same',activation=tf.nn.relu)
        # conv_4=tf.layers.batch_normalization(conv_4,training=is_train)
        max_pool_2=tf.layers.max_pooling2d(conv_3,(3,3),(2,2),padding='same')
        # max_pool_2=tf.layers.dropout(max_pool_2,rate=0.2,training=is_train)
        max_pool_2=tf.layers.batch_normalization(max_pool_2,training=is_train)
    with tf.name_scope('inception_block_1'):
        incep_1=inception_block(max_pool_2,32,32,32,32,32,32,32,is_train)
        # incep_1=tf.layers.conv2d(max_pool_2,128,(2,2),strides=(1,1),kernel_initializer=initial,padding='same',activation=tf.nn.relu)
        # incep_1=tf.layers.batch_normalization(incep_1,training=is_train)
    # with tf.name_scope('inception_block_2'):
    #     incep_2=inception_block(incep_1,32,32,32,32,32,32,32,is_train)
        # incep_2=tf.layers.conv2d(incep_1,256,(2,2),strides=(1,1),kernel_initializer=initial,padding='same',activation=tf.nn.relu)
        # incep_2=tf.layers.batch_normalization(incep_2,training=is_train)
    with tf.name_scope('inception_block_3'):
        incep_3=inception_block(incep_1,64,64,64,64,64,64,64,is_train)
    # with tf.name_scope('inception_block_4'):
    #     incep_4=inception_block(incep_3,64,64,64,64,64,64,64,is_train)
        # incep_4=tf.layers.conv2d(incep_2,512,(2,2),strides=(1,1),kernel_initializer=initial,padding='same',activation=tf.nn.relu)
        # incep_4=tf.layers.batch_normalization(incep_4,training=is_train)
    # with tf.name_scope('max_pool'):
    #     max_pool_3=tf.layers.max_pooling2d(incep_4,(2,2),(1,1),padding='valid')
    #     max_pool_3=tf.layers.batch_normalization(max_pool_3,training=is_train)
    # with tf.name_scope('flatten'):
    #     flatten=tf.layers.flatten(incep_4)
    # with tf.name_scope('angle_concat'):
    #     features_concat=tf.concat([flatten,input_angle],1)
    #     features_concat=tf.layers.batch_normalization(features_concat,training=is_train)
    # with tf.name_scope('FC_1'):
    #     FC_1=tf.layers.dense(flatten,64,kernel_initializer=initial)
    #     # FC_1=tf.layers.batch_normalization(FC_1,training=is_train)
    #     FC_1=tf.nn.relu(FC_1)
    #     FC_1=tf.layers.batch_normalization(FC_1,training=is_train)
    #     FC_1=tf.layers.dropout(FC_1,rate=0.2,training=is_train)
    with tf.name_scope('global_max_pooling'):
        g_max_pool=tf.reduce_mean(incep_3,[1,2])
        g_max_pool=tf.layers.batch_normalization(g_max_pool,training=is_train)
        # g_max_pool=tf.layers.batch_normalization(g_max_pool,training=is_train)
    # with tf.name_scope('FC_2'):
    #     FC_2=tf.layers.dense(g_max_pool,32,kernel_initializer=initial)
    #     # FC_2=tf.layers.batch_normalization(FC_2,training=is_train)
    #     FC_2=tf.nn.relu(FC_2)
    #     FC_2=tf.layers.batch_normalization(FC_2,training=is_train)

    with tf.name_scope('Logits'):
        logits=tf.layers.dense(g_max_pool,1,kernel_initializer=initial)
        prob=tf.nn.sigmoid(logits)
    with tf.name_scope('loss'):
        Loss=tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=input_label,logits=logits))
    optimizer=AMSGrad(learning_rate=1e-3)
    with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
        train_op=optimizer.minimize(Loss)
    init_op=tf.group(tf.global_variables_initializer(),tf.local_variables_initializer())

save_file='./model_save/CK'
num_epochs=15
batch_size=128
with tf.Session(graph=main_graph) as sess:
    sess.run(init_op)
    for i in range(num_epochs):
        for image,label in get_batch(train_images,train_label,batch_size,i):
            sess.run(train_op,feed_dict={input_images:image,
                                         # input_angle:angle,
                                         input_label:label,
                                         is_train:True})
        loss=sess.run(Loss,feed_dict={input_images:train_images[i:i+600,:,:,:],
                                         # input_angle:train_angle[i:i+200,:],
                                         input_label:train_label[i:i+600],
                                         is_train:False})
        print("Epoch: {}/{}......Loss: {}".format(i+1,num_epochs,loss))
    saver=tf.train.Saver()
    saver.save(sess,save_file)
