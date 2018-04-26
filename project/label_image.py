import tensorflow as tf
import sys
import overlay
import cv2

#지금 이 프로그램은 hood-t 메뉴에서 black과 white를 오버레이 했을때 score가
#더 높게 나온 옷을 추천하게 구현했다.

# change this as you see fit
#image_path = sys.argv[1]
def Reco(title,body,clothes):
    i=0
    NUM = 5

    while(i<NUM):
        original_clothes = cv2.imread('original.png')

        for (x, y, w, h) in body:
            body_mask = cv2.imread(clothes[i])
            overlay.masked_Operation(x,y,w,h,original_clothes,body_mask,clothes[i],270,1)

        i = i+1
                             
    image_path = ['overlay_black.png', 'overlay_blue.png', 'overlay_gray.png','overlay_white.png','overlay_beige.png']
    
#image_path 는 오버레이 한 이미지 즉 5가지 이미지가 찍힌다.
#그 5가지 이미지 사진을 비교해서 점수가 가장 높은 이미지를 찾아서 해당 옷을 추천
    count=0
    # Read in the image_data
    best_score = 0
    best_clothes = 'default'
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')
    while(count<NUM):
        image_data = tf.gfile.FastGFile(image_path[count], 'rb').read()


        # Loads label file, strips off carriage return
        label_lines = [line.rstrip() for line
                           in tf.gfile.GFile("retrained_labels.txt")]

        # Unpersists graph from file
        

        with tf.Session() as sess:
            
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})
            
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            better_score = 0
            better_clothes = 'default'
            
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                if(better_score<score):
                    better_score = score
                    better_clothes = human_string
                print('%s (score = %.5f)' % (human_string, score))

            print(better_clothes)
            print(better_score)
            

        if(best_score<better_score):
            best_score = better_score
            best_clothes = better_clothes
        count=count+1

    print(best_clothes)
    print(best_score)
    return best_clothes

        
    

        
