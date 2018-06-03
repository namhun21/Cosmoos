import queue
import cv2
import sys
import tensorflow as tf


def Suggest(frame, faceList, my_q):
    framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    for (x, y, w, h) in faceList:
        cv2.imwrite('face_original.png', framegray[y-70:y+h+20, x-20:x+w+20])
             
        print('finish1')
    total = 0
    for i in range(1, 10000000):
        total += i
        
    image_path = 'face_original.png'

    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]

    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        best_score = 0
        best_color = 'default'
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            if(best_score<score):
                best_score = score
                best_color = human_string 
            print('%s (score = %.5f)' % (human_string, score))
        print(best_color)

    
    my_q.put(best_color)
    print('finish2')
