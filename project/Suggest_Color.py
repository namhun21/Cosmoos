import queue
import cv2
import sys
import tensorflow as tf

#텐서와 관련된 기본적 구조를 차재성 학생이 작성하였고 김동균 학생이
#추천 시스템에 맞게 코드를 작성하였습니다.
def Suggest_color(frame, faceList, my_q):
    
    
        
    image_path = 'face_original.jpeg'

    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels(color).txt")]
    print("here1")
    with tf.gfile.FastGFile("retrained_graph(color).pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    print("here2")
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
    print("finish_color")
