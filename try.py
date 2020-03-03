import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
import cv2 
import pandas as pd

fields = ['filename', 'f_length', 'distortion']
f = open('./img_list.txt', 'r')
data = pd.read_csv("./img_list.txt", delimiter=',', names=fields)
print(data)
exit(0)
filepaths = list(data['filename'])
images = []
image_sizes = []
data_dict = data.set_index('filename').T.to_dict('list')
camera_matrix = []
dist_coeff = []

# assume tangential distortion is 0 (only parallel photos taken)
p1 = 0.0
p2 = 0.0
# we only take first radial distortion parameter 
k2 = 0.0

for f in filepaths:
    
    img = cv2.imread('./test_images/'+f)
    h, w, c = img.shape
    k1 = data_dict[f][1]
    image_sizes.append((h,w,c))
    camera_matrix.append([[data_dict[f][0], 0.0, h/2], [0.0, data_dict[f][0], w/2], [0.0, 0.0, 1.0]]) 
    images.append(img)
    dist_coeff.append([k1,k2,p1,p2])

camera_matrix_np = np.array(camera_matrix)
dist_coeff_np = np.array(dist_coeff)
dst = np.zeros_like(images[0])

dst2 = cv2.undistort(src=images[2], cameraMatrix=camera_matrix_np[2], distCoeffs=dist_coeff_np[2])

# cv2.imshow("d", images[0])
# cv2.waitKey(0)

cv2.imshow("ud", dst2)

cv2.waitKey(0)
pprint(camera_matrix_np[1])
pprint(image_sizes[1])
# pprint(dst2.sum(axis=-1).shape)
# plt.imshow(dst2)
