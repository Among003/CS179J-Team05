# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:25:54 2020

@author: tyler
"""

import os, cv2, sys, imutils, time
import numpy as np
import tensorflow as tf

# tensorflow module for utilities using the models research repository
# sys.path.append('D:\school\CS179J\tensorflow\models')
# sys.path.append('D:\school\CS179J\tensorflow\models\research')
# sys.path.append('D:\school\CS179J\tensorflow\models\research\slim')
prev_dir = os.getcwd()
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(cwd, '..'))
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as vis_util
os.chdir(prev_dir)

CLNUM = 2

# font 
font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (50, 50) 
  
# fontScale 
fontScale = 1
   
# Blue color in BGR 
color = (255, 0, 0) 
  
# Line thickness of 2 px 
thickness = 2

DELAY = 250

class Object_Detection:
    def __init__(self, COORDINATE_CLASS, GRAPH_PATH, LABEL_PATH, VIDEO1, VIDEO2, NUM_CLASSES=CLNUM, Verbose=False):
        self.cclass = COORDINATE_CLASS
        self.graph_path = GRAPH_PATH
        self.label_path = LABEL_PATH
        self.video1 = VIDEO1
        self.video2 = VIDEO2
        self.num_classes = NUM_CLASSES
        self.Verbose = Verbose
        
        # Map output nodes to labels for classification
        label_map = label_map_util.load_labelmap(LABEL_PATH)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)
        
        # create graph and load tensorflow model
        self.graph = tf.Graph()
        with self.graph.as_default():
            graph_def = tf.GraphDef()
            with tf.gfile.GFile(GRAPH_PATH, 'rb') as fid:
                serialized_graph = fid.read()
                graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(graph_def, name='')
                self.sess = tf.Session(graph=self.graph)
                
        # Input tensor is the image detected from webcam
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
        ret1, frame1 = self.video1.read()
        if not ret1: return None # Exit with empty values if 
        frame1 = imutils.rotate(frame1, angle=180)
        ret2, frame2 = self.video2.read()
        if not ret2: return None # Exit with empty values if 
        frame2 = imutils.rotate(frame2, angle=90)
        
        # Map colors on image for openCV
        frame_rgb1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame_expanded1 = np.expand_dims(frame_rgb1, axis=0)
        frame_rgb2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        frame_expanded2 = np.expand_dims(frame_rgb2, axis=0)
    
        # This is the part with the actual detection
        (boxes1, scores1, classes1, num1) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: frame_expanded1})
        (boxes2, scores2, classes2, num2) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: frame_expanded2})
        
        # Define predicted class from the highest confidence guess of the image
        predicted_class1 = self.category_index[int(classes1[0][0])]['name']
        try:
            predicted_class2 = self.category_index[int(classes2[0][0])]['name']
        except KeyError:
            print("Error: ", classes2[0][0], "when should be in: ", self.category_index)
            raise KeyError
        
        results = {"video1": {"boxes": boxes1[0][0].tolist(), "scores": scores1[0][0], "classes": predicted_class1},
                   "video2": {"boxes": boxes2[0][0].tolist(), "scores": scores2[0][0], "classes": predicted_class2},
                   "hand_val": predicted_class1}
        #print(category_index)
    
        # Draw the bounding box and prediction
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame1,
            np.squeeze(boxes1),
            np.squeeze(classes1).astype(np.int32),
            np.squeeze(scores1),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)
        
        # Draw the bounding box and prediction
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame2,
            np.squeeze(boxes2),
            np.squeeze(classes2).astype(np.int32),
            np.squeeze(scores2),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)
        
        print("going to coors")
        #results["coors"] = self.cclass.Filter(self.cclass.GetCoors(boxes1[0][0], boxes2[0][0]))
        results["coors"] = self.cclass.GetCoors(boxes1[0][0], boxes2[0][0])
        print("done")
        print(results)
        
        #time.sleep(DELAY)
        
        if self.Verbose:
            text1 = "Top View Values: {} , {} , {}".format(results["coors"][0], results["coors"][1], results["hand_val"])
            text2 = "Side View Values: {}".format(results["coors"][2])
            frame1 = cv2.putText(frame1, text1, org, font,  
                   fontScale, color, thickness, cv2.LINE_AA) 
            frame2 = cv2.putText(frame2, text2, org, font,  
                   fontScale, color, thickness, cv2.LINE_AA) 
            # cv2.imshow("Obj Detect 1: {} , {} , {} , {}".format(results["coors"][0], results["coors"][1], results["coors"][2], results["hand_val"]), frame1)
            # cv2.imshow("Obj Detect 2: {} , {} , {} , {}".format(results["coors"][0], results["coors"][1], results["coors"][2], results["hand_val"]), frame2)
            cv2.imshow("Obj Detect 1", frame1)
            cv2.imshow("Obj Detect 2", frame2)
            if cv2.waitKey(1) == ord('q'):
                return None
        
        return results
            