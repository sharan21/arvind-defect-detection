import numpy as np
from math import sqrt
from scipy import interpolate


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
    img_und = np.zeros((params_ud['H'], params_ud['W'], 3))

    for c in range(3):
        image_und[:,:,c] = interpolate.interp2d(idis[:,:,c], x_d, y_d, kind="cubic")

    
    # for c in range(1,3,1):
        
    # for c=1:3
    # Image_und(:,:,c) = interp2(im2double(Idis(:,:,c)), X_d, Y_d, 'cubic');
    # [Im_und.H, Im_und.W, ~] = size(Image_und);
    
    # # %ROI
    # min(X_d(:)), max(X_d(:));
    # min(Y_d(:)), max(Y_d(:));
    # size(Idis);

# if __name__ = "__main__":
#     params_d = {'W':10, 'H':1
                
