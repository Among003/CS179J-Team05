# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:25:54 2020

@author: tyler
"""

import os, cv2, sys
import numpy as np
import tensorflow as tf

# tensorflow module for utilities using the models research repository
from utils import label_map_util
from utils import visualization_utils as vis_util

class Object_Detection:
    def __init__(self, GRAPH_PATH, LABEL_PATH, NUM_CLASSES):
        self.graph_path = GRAPH_PATH
        self.label_path = LABEL_PATH
        self.num_classes = NUM_CLASSES
        
        label_map = label_map_util.load_labelmap(LABEL_PATH)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)
        
        self.graph = tf.Graph()
        with self.graph.as_default():
            graph_def = tf.GraphDef()
            with tf.gfile.GFile(GRAPH_PATH, 'rb') as fid:
                serialized_graph = fid.read()
                graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(graph_def, name='')
                self.sess = tf.Session(graph=self.graph)
                
        # Input tensor is the image
        self.image_tensor = self.graph.get_tensor_by_name('image_tensor:0')
        
        # Output tensors are the detection boxes, scores, and classes
        # Bounding box outlines the object and will be used to give location of the hand for control
        self.detection_boxes = self.graph.get_tensor_by_name('detection_boxes:0')
        
        # Scores give confidence value
        # Classes give prediction
        self.detection_scores = self.graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.graph.get_tensor_by_name('detection_classes:0')
        
        # Number of objects detected
        self.num_detections = self.graph.get_tensor_by_name('num_detections:0')
        
    def Detect(self):
        # Get frame, frame is given in 3d array of RGB values
        ret, frame = self.video.read()
        #print(ret)
        if not ret: return {}
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)
    
        # This is the part with the actual detection
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: frame_expanded})
        
        predicted_class = self.category_index[classes[0][0]]['name']
        
        results = {"boxes": boxes[0][0].tolist(), "scores": scores[0][0], "classes": predicted_class}
        #print(category_index)
    
        # Draw the bounding box and prediction
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)
        
        return results
        
    
        

# def InitObjectDetection():
#     # Directory names 
#     GRAPH_FOLDER="inference_graph"
#     GRAPH_FILE="frozen_inference_graph.pb"
#     CWD=os.getcwd()

#     GRAPH_PATH=os.path.join(CWD, GRAPH_FOLDER, GRAPH_FILE)
#     LABEL_PATH=os.path.join(CWD,"training","labelmap.pbtxt")
    
#     NUM_CLASSES=2
    
#     #Load label map
#     #Label map translates the integer output from model to our assigned 
#     #These are tensorflow util functions in the research github
#     label_map = label_map_util.load_labelmap(LABEL_PATH)
#     categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
#     category_index = label_map_util.create_category_index(categories)

#     graph = tf.Graph()
#     with graph.as_default():
#         graph_def = tf.GraphDef()
#         with tf.gfile.GFile(GRAPH_PATH, 'rb') as fid:
#             serialized_graph = fid.read()
#             graph_def.ParseFromString(serialized_graph)
#             tf.import_graph_def(graph_def, name='')

#             sess = tf.Session(graph=graph)
#     return category_index, graph, sess

# def Detect(video, category_index, graph, sess):
#     # Define input and output tensors (i.e. data) for the object detection classifier

#     # Input tensor is the image
#     image_tensor = graph.get_tensor_by_name('image_tensor:0')
    
#     # Output tensors are the detection boxes, scores, and classes
#     # Bounding box outlines the object and will be used to give location of the hand for control
#     detection_boxes = graph.get_tensor_by_name('detection_boxes:0')
    
#     # Scores give confidence value
#     # Classes give prediction
#     detection_scores = graph.get_tensor_by_name('detection_scores:0')
#     detection_classes = graph.get_tensor_by_name('detection_classes:0')
    
#     # Number of objects detected
#     num_detections = graph.get_tensor_by_name('num_detections:0')
    
#     results = []
    
#     while(video.isOpened()):

#         # Get frame, frame is given in 3d array of RGB values
#         ret, frame = video.read()
#         #print(ret)
#         if not ret: break
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame_expanded = np.expand_dims(frame_rgb, axis=0)
    
#         # This is the part with the actual detection
#         (boxes, scores, classes, num) = sess.run(
#             [detection_boxes, detection_scores, detection_classes, num_detections],
#             feed_dict={image_tensor: frame_expanded})
        
#         predicted_class = category_index[classes[0][0]]['name']
        
#         results.append({"boxes": boxes[0][0].tolist(), "scores": scores[0][0], "classes": predicted_class})
#         #print(category_index)
    
#         # Draw the bounding box and prediction
#         vis_util.visualize_boxes_and_labels_on_image_array(
#             frame,
#             np.squeeze(boxes),
#             np.squeeze(classes).astype(np.int32),
#             np.squeeze(scores),
#             category_index,
#             use_normalized_coordinates=True,
#             line_thickness=8,
#             min_score_thresh=0.60)
    
#         # Display the image
#         cv2.imshow('Object detector', frame)
    
#         # Press 'q' to quit
#         if cv2.waitKey(1) == ord('q'):
#             break
        
#     return results
            