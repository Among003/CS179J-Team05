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

def InitObjectDetection():
    # Directory names 
    GRAPH_FOLDER="inference_graph"
    GRAPH_FILE="frozen_inference_graph.pb"
    CWD=os.getcwd()

    GRAPH_PATH=os.path.join(CWD, GRAPH_FOLDER, GRAPH_FILE)
    LABEL_PATH=os.path.join(CWD,"training","labelmap.pbtxt")
    
    NUM_CLASSES=2
    
    #Load label map
    #Label map translates the integer output from model to our assigned 
    #These are tensorflow util functions in the research github
    label_map = label_map_util.load_labelmap(LABEL_PATH)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    graph = tf.Graph()
    with graph.as_default():
        graph_def = tf.GraphDef()
        with tf.gfile.GFile(GRAPH_PATH, 'rb') as fid:
            serialized_graph = fid.read()
            graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(graph_def, name='')

            sess = tf.Session(graph=graph)
    return category_index, graph, sess

def Detect(video, category_index, graph, sess):
    # Define input and output tensors (i.e. data) for the object detection classifier

    # Input tensor is the image
    image_tensor = graph.get_tensor_by_name('image_tensor:0')
    
    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = graph.get_tensor_by_name('detection_boxes:0')
    
    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = graph.get_tensor_by_name('detection_scores:0')
    detection_classes = graph.get_tensor_by_name('detection_classes:0')
    
    # Number of objects detected
    num_detections = graph.get_tensor_by_name('num_detections:0')
    
    while(video.isOpened()):

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, frame = video.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)
    
        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})
    
        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)
    
        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
    
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
        
    return (boxes, scores, classes)
            