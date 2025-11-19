import numpy as np
import os
import random
import math


def rotate(data, angle):     
    "rotate plane"
    
    rotation_angle = math.radians(angle)
    cosval = np.cos(rotation_angle)
    sinval = np.sin(rotation_angle)
    rotation_matrix = np.array([
            [1, 0, 0],
            [0, cosval, sinval],
            [0, -sinval, cosval]
        ])
    rotated_data = np.dot(data, rotation_matrix)
    return rotated_data

def gaussian_noise(mu, sigma, size=0.5):  
    "Generating Guassian noise"
    return np.random.normal(mu, sigma, size)

def square_num_plane(lines_num_points,plane_num_points,line_len, plane_width, facade_clip, angle): 
    " Generating simulation plane"
    
    #Generating road boundary (Eq: ax + by + c = 0, a and c = 0, b = 1)
    x1 = np.random.uniform(0, line_len, lines_num_points).reshape(-1, 1)
    y1 = np.random.uniform(0,0, lines_num_points).reshape(-1, 1)
    z1 = np.zeros((lines_num_points, 1))
    line= np.hstack((x1, y1, z1))


    #Generating road plane
    x_min, x_max = 0, line_len
    y_min, y_max = 0, plane_width 
   
    x2 = np.random.uniform(x_min, x_max, plane_num_points).reshape(-1, 1)
    y2 = np.random.uniform(y_min, y_max, plane_num_points).reshape(-1, 1)
    z2 = np.zeros((plane_num_points, 1))
    plane = np.hstack((x2, y2, z2))

    
    #Generating road facade 
    facade = rotate(plane, angle)
    index = facade[:, 2] <= facade_clip
    facade = facade[index, :]
    
    #initial simulation road section
    road_section = np.vstack((line, plane, facade))
    
    #Add the Guassian noise
    mu = 0  # mean
    sigma = 0.0025 # standard deviation
    for i in range(road_section.shape[0]):
        road_section[i, 0] += gaussian_noise(mu, sigma, 1)
        road_section[i, 1] += gaussian_noise(mu, sigma, 1)
        road_section[i, 2] += gaussian_noise(mu, sigma, 1)

    #simulation samples
    label = np.zeros((road_section.shape[0], 1))
    label[0:lines_num_points, :] = 1
    road_section = np.hstack((road_section, label))
    return road_section




plane_width = round(random.uniform(1.5, 2.5), 3)  
root = 'E:/plane/paris'
plane_point_num = 7500

   
for i in range(0,500):
    
  length =  round(random.uniform(4, 5), 3) 
  width = round(random.uniform(1.5, 2.5), 3) 
  high= round(random.uniform(0.1, 0.2), 3) 
  random_num = round(random.uniform(0.013, 0.041), 3) #the proportion of line point
  angle = np.random.uniform(87, 93)
  
  num= int(round(random_num * (plane_point_num  + plane_point_num  * high), 0))
  produce_plane=square_num_plane(num,plane_point_num ,length, width, high, angle)

  locate=os.path.join(root,'plane_cloud_{}.txt'.format(i))
  np.savetxt(locate, produce_plane, fmt = ['%.6f', '%.6f','%.6f','%.1f'])    
