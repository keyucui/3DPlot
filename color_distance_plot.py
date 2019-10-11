#ecoding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import cv2
from mpl_toolkits.mplot3d import Axes3D

def load_image(fi_name='heart.jpg', standard_size=100):
    '''
    :param fi_name:  the name/path of the 2d image
    :param standard_size:  the size of processed 3d image
    :return: 2 dim ndarray image, distance to adjust to make the image central
    '''
    img = cv2.imread(fi_name, 0)
    shapes = img.shape
    if shapes[0] >= shapes[1]:
        rate = standard_size/shapes[0]
    else:
        rate = standard_size/shapes[1]
    img = cv2.resize(img, (int(rate * shapes[0]), int(rate * shapes[1])))
    return img, int(standard_size/2)


img, width = load_image(fi_name='name1.png')

#process the image ------------>
shapes = img.shape
x_set = []
z_set = []
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if img[i][j] < 230:
            z_set.append(i)
            x_set.append(j)
x_set = np.asarray(x_set)
z_set = np.asarray(z_set)
x_adj = int(shapes[0]/2)
z_adj = int(shapes[1]/2)
x_set -= x_adj
z_set -= z_adj
z_set *= -1

#根据距离分类，max_dis为最大距离点
centre_distance = np.sqrt(x_set**2 + z_set**2)
max_dis = np.max(centre_distance)

sorts_num = 5
intern = np.linspace(0, max_dis, sorts_num)
points_set = [[[], []] for _ in range(sorts_num - 1)]
for ii in range(len(centre_distance)):
    for jj in range(len(intern)):
        if centre_distance[ii] >= intern[jj]:
            continue
        else:
            points_set[jj - 1][0].append(x_set[ii])
            points_set[jj - 1][1].append(z_set[ii])
            # break

colmap = ['#FF4333', '#FF7833', '#FFA133', '#FFCA33'][::-1]
# colmap = ['black', 'red', 'blue','green']


y_list = np.linspace(-4, 4, 8)
alpha_list = np.linspace(0.2, 0.1, len(y_list))

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.set_ylim([-width, width])
ax.set_xlim([-width, width])
ax.set_zlim([-width, width])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.view_init(25, 290)
ax.grid(False)
# plt.ion()
for k in range(sorts_num - 1):
    for ii in range(y_list.shape[0]):
        ax.scatter(
            points_set[k][0], y_list[ii], points_set[k][1],
            zdir='z',
            # marker='*',
            s=4,
            c=colmap[k],
            alpha=alpha_list[ii]
        )
        # plt.pause(0.001)


# 双环特效
print(max_dis)
cycle = np.linspace(0, 2 * np.pi, 100)
cycle1_x = np.sin(cycle) * 40
cycle1_y = np.cos(cycle) * 40
ax.scatter(cycle1_x, y_list[0], cycle1_y)



# ax.axis('equal')
plt.show()
