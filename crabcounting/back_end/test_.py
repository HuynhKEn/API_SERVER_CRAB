import os
import torch
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

from back_end.src.crowd_count import CrowdCounter
from back_end.src import network
from back_end.src.data_loader_ import ImageDataLoader
from back_end.src import utils

os.environ["CUDA_VISIBLE_DEVICES"] = "0"   
np.warnings.filterwarnings('ignore')
# dataset, model, and pooling method    
datasets = ['shtechA', 'shtechB']     # datasets
models = ['base', 'wide', 'deep']     # backbone network architecture
pools = ['vpool','stackpool','mpool']    #  vpool is vanilla pooling; stackpool is stacked pooling; mpool is multi-kernel pooling

###
dataset_name = datasets[0]   # choose the dataset
model = models[2]          # choose the backbone network architecture
pool = pools[1]          # choose the pooling method 
method=model+'_'+pool

name = dataset_name[-1]

def call_test(url_file_name):
    data_path =  url_file_name
    model_path = "save_models/deep_mpool_shtechA_976.h5"
    print('Testing %s' % (model_path))

    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True
    vis = False
    save_output = True    

    output_dir = './output/'
    model_name = os.path.basename(model_path).split('.')[0]
    file_results = os.path.join(output_dir,'results_' + model_name + '_.txt')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_dir = os.path.join(output_dir, 'density_maps_' + model_name)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    net = CrowdCounter(model,pool)      
    trained_model = os.path.join(model_path)
    network.load_net(trained_model, net)
    net.cuda()
    net.eval()

    if model in ['base','wide']:
        scaling = 4
    if model=='deep':
        scaling = 8

    #load test data
    data_loader = ImageDataLoader(data_path, shuffle=False, gt_downsample=True, pre_load=False, batch_size=1, scaling=scaling)

    mae = 0.0
    mse = 0.0
    num = 0
    for blob in data_loader:
        num+=1
        im_data = blob['data']
        density_map = net(im_data)
        density_map = density_map.data.cpu().numpy()
        et_count = np.sum(density_map)
        print(blob['fname'].split('.')[0])
        print("predict",et_count)
        print(100*"-")
        if vis:
            utils.display_results(im_data, gt_data, density_map)
        if save_output:
            utils.save_density_map(density_map, output_dir, 'output_' + blob['fname'].split('.')[0] + '.png')
        if num%100==0:
            print('%d/%d' % (num,data_loader.get_num_samples()))

    return et_count
