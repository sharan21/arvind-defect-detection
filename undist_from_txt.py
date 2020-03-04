from undistort_sph_im import undistort

import os
import pandas as pd
import cv2

dist_folder = './test_images'

f = pd.read_csv('./img_list.csv')

paths = f['paths']
focal = f['f_lengths']
distortion = f['dist']

f = 0
dist = 0
images = []


for i in range(len(paths)): 

    idis = cv2.imread('./test_images/'+str(paths[i]))
    xi = distortion[i]
    dist = dist + xi
    (imh, imw, _) = idis.shape
    f_dist = focal[i] + (imw/imh)*(imh/299)
    f = f + f_dist
    u0_dist = imw/2
    v0_dist = imh/2
    params_d = {}
    params_d['f'] = f_dist
    params_d['W'] = int(u0_dist*2)
    params_d['H'] = int(v0_dist*2)
    params_d['xi'] = xi

    params_ud = {}
    params_ud['f'] = f_dist
    params_ud['W'] = int(u0_dist*2)
    params_ud['H'] = int(v0_dist*2)

    image_und = undistort(idis, params_d, params_ud)



# for i=1:length(paths)

#     Idis = imread(paths{i});

#     % xi = 1.08;
#     xi = distortion(i); % distortion
#     dist = dist + xi;
#     [ImH,ImW,~] = size(Idis);
#     % f_dist = 320 * (ImW/ImH) * (ImH/299); 
#     f_dist = focal(i) * (ImW/ImH) * (ImH/299); % focal length
#     f = f + f_dist;
#     u0_dist = ImW/2;
#     v0_dist = ImH/2;
#     Paramsd.f = f_dist;
#     Paramsd.W = u0_dist*2;  
#     Paramsd.H = v0_dist*2;
#     Paramsd.xi = xi;

#     Paramsund.f = f_dist;
#     Paramsund.W = u0_dist*2;  
#     Paramsund.H = v0_dist*2;
    
#     tic
#     Image_und = undistSphIm(Idis, Paramsd, Paramsund);
#     toc

#     %if (size(Image_und,1)~=0)
#         paths_list = strsplit(paths{i}, '/');
#         res1 = strsplit(paths_list{9}, '_');
#         res2 = strsplit(res1{2}, '.')

#         out = str2double(res2{1});
        
#         filename = [sprintf('%04d', out),'.jpg'];
#         fullname = fullfile(dist_folder,filename);
#         imwrite(Image_und,fullname);
#     %end
# end
