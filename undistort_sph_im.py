import numpy as np
from math import sqrt
from scipy import interpolate
from utils import interp2linear
import cv2

def diskradius(xi, f):

    return np.sqrt(-(f*f)/(1-xi*xi))

def undistort(idis, params_d, params_ud):


    # not sure why there was an * 3 in the rhs
    params_ud['W'] = params_d['W']
    params_ud['H'] = params_d['H']

    # Parameters of the camera to generate
    f_dist = params_d['f']
    u0_dist = params_d['W']/2  
    v0_dist = params_d['H']/2

    f_undist = params_ud['f']
    u0_undist = params_ud['W']/2  
    v0_undist = params_ud['H']/2
    
    xi = params_d['xi']

    # (Imd.H, Imd.W, ~] = size(Idis);

    # 1. Projection on the image 
    x = np.arange(params_d['W'])
    y = np.arange(params_d['H'])

    
    grid_x, grid_y = np.meshgrid(x, y, sparse=True)
    x_cam = np.divide(grid_x, f_undist) - u0_undist/f_undist
    y_cam = np.divide(grid_y, f_undist) - v0_undist/f_undist
    z_cam = np.ones((params_ud['H'], params_ud['W'])) 

    # 2. Image to sphere cart
    xi1 = 0

    alpha_cam_1 = (xi1*z_cam + np.sqrt(z_cam*z_cam + ((1-xi1*xi1)*(x_cam*x_cam + y_cam*y_cam))))
    alpha_cam_2 = (x_cam*x_cam+y_cam*y_cam+z_cam*z_cam)

    alpha_cam = alpha_cam_1/alpha_cam_2

    x_sph = x_cam * alpha_cam
    y_sph = y_cam * alpha_cam
    z_sph = z_cam * alpha_cam - xi1 

    # 3. reprojection on distorted
    den = xi*(np.sqrt(x_sph*x_sph + y_sph*y_sph + z_sph*z_sph)) + z_sph 
    x_d = ((x_sph*f_dist)/den) + u0_dist
    y_d = ((y_sph*f_dist)/den) + v0_dist
 
    # %4. Final step interpolation and mapping
    im_und = np.zeros((params_ud['H'], params_ud['W'], 3))
    
    # for c in range(3):
    #     im_und[:,:,c] = interp2linear(idis[:,:,c], x_d, y_d)

    im_und = interp2linear(idis, x_d, y_d)


    # im_trans = np.transpose(im, (1,0,2))

    # r = diskradius(xi, f_dist)

    # DIM = im.shape
    # ci = (np.round(DIM[0]/2), np.round(DIM[1]/2))
    # xx, yy = np.meshgrid(range(DIM[0])-ci[0], range(DIM[1])-ci[1])
    # mask = np.double((np.multiply(xx,xx)+np.multiply(yy,yy))<r*r)
    # mask_3channel = np.stack([mask,mask,mask],axis=-1)
    # print(mask_3channel.shape)
    # print(im_trans.shape)
    # im_und = np.array(np.multiply(im_trans, mask_3channel),dtype=np.uint8)

    cv2.imshow("try", im_und)
    cv2.waitKey(0)


                
