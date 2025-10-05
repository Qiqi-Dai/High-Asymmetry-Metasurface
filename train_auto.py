import os
import time
import numpy as np
from PIL import Image
import torch
from denoising_diffusion_pytorch import Unet, GaussianDiffusion, Trainer
import matplotlib.pyplot as plt
import scipy.io
import shutil
import imp
lumapi = imp.load_source("lumapi","C:/Program Files/Lumerical/v232/api/python/lumapi.py")
os.add_dll_directory("C:/Program Files/Lumerical/v232/api/python")
import lumapi
import matlab.engine

torch.cuda.set_per_process_memory_fraction(0.8, 0)

it_total = 10

for it_num in range(it_total):

    Data_folder = 'dataset/'
    Result_folder = 'result_it%d/'%(it_num+1)
    Visual_folder = Result_folder + '/visual'
    Loss_folder = Result_folder + '/loss'

    files = os.listdir(Data_folder) 
    num_png = len(files)       
    print(num_png)

    if not os.path.exists(Result_folder):
        os.makedirs(Result_folder)
    if not os.path.exists(Visual_folder):
        os.makedirs(Visual_folder)
    if not os.path.exists(Loss_folder):
        os.makedirs(Loss_folder)

    Image_size = 100
    Batch_size = 16
    train_num_steps = 20000 ### 20000
    save_and_sample_every = 1000 ### 1000
    Num_sampling = 100 ### 100

    model = Unet(
        dim = 64,
        dim_mults = (1, 2, 4),
        channels = 1
    ).cuda()

    diffusion = GaussianDiffusion(
        model,
        image_size = Image_size,
        timesteps = 1000,   # number of steps
        sampling_timesteps = 250
    ).cuda()

    #### Traning
    trainer = Trainer(
        diffusion,
        Data_folder,
        train_batch_size = Batch_size,
        train_lr = 2e-5,
        train_num_steps = train_num_steps,         # total training steps 20000
        save_and_sample_every = save_and_sample_every,   # 1000
        gradient_accumulate_every = 2,    # gradient accumulation steps
        ema_decay = 0.995,                # exponential moving average decay
        results_folder = Result_folder,
        num_samples = 25,
        calculate_fid = True,
        num_fid_samples = 50,
        save_best_and_latest_only = True
    )

    trainer.train()

    #### Plot loss
    x = np.linspace(0, train_num_steps-1, train_num_steps)
    y1 = scipy.io.loadmat(Loss_folder+'/loss_array.mat')
    y2 = scipy.io.loadmat(Loss_folder+'/fid_score_array.mat')

    plt.figure(1)
    plt.plot(x,np.squeeze(y1['loss_array']),'ro-')
    plt.xlim([0,train_num_steps-1])
    plt.xlabel('Training step')
    plt.ylabel('Loss')
    plt.savefig(Loss_folder+'/Loss.jpg')
    plt.close(1)

    plt.figure(2)
    plt.plot(np.squeeze(y2['fid_score_array']),'ro-')
    plt.xlabel('Sampling step')
    plt.ylabel('FID Score')
    plt.savefig(Loss_folder+'/FID.jpg')
    plt.close(2)

    #### Sampling and generate import files
    eng = matlab.engine.start_matlab()
    for num in range(Num_sampling):
        sampled_images = diffusion.sample(batch_size = 1)
        sampled_images = np.array(sampled_images.cpu())
        # print(sampled_images.shape) 
        pred = sampled_images[0].reshape(Image_size, Image_size) * 255
        pred = Image.fromarray(pred)
        pred.convert('L').save(Visual_folder + '/pred_%d.png'%(num))
        # os.system("matlab -nosplash -r \"import_generator('result_it%d/visual/', %d)\" && quit "%(it_num+1, num))
        # time.sleep(1)
        eng.import_generator('result_it%d/visual/'%(it_num+1), num, nargout=0)

    #### Generate fdtd files
    for i in range(Num_sampling):
        if os.path.exists('import_%d.txt'%i):
            print(i)
         
    lumapi.FDTD('simulation_file_generator.lsf')
    for i in range(Num_sampling):
        shutil.move('import_%d.txt'%i,'result_it%d/visual/import_%d.txt'%(it_num+1, i))
        shutil.copyfile('%d.fsp'%i,'result_it%d/visual/%d.fsp'%(it_num+1, i))

    #### Run fdtd files
    lumapi.FDTD('get_para.lsf')
    
    #### Select V1 according to refractive index
    for i in range(Num_sampling):
        # os.system("matlab -nosplash -r \"select_V1('result_it%d/visual/V1/', %d)\" && quit"%(it_num+1, i))
        # time.sleep(1)
        eng.select_V1('result_it%d/visual/V1/'%(it_num+1), i, nargout=0)
    
    #### Save all the simulation results
    for i in range(Num_sampling):
        shutil.move('results_%d.mat'%i,'result_it%d/visual/results_%d.mat'%(it_num+1, i))

    #### Select V2 according to FoM
    # os.system("matlab -nosplash -r \"select_V2('result_it%d/visual/', 'result_it%d/visual/V1/', 'result_it%d/visual/V2/', 'dataset/')\" && quit"%(it_num+1, it_num+1, it_num+1))
    # time.sleep(10)
    eng.select_V2('result_it%d/visual/'%(it_num+1), 'result_it%d/visual/V1/'%(it_num+1), 'result_it%d/visual/V2/'%(it_num+1), 'dataset/', nargout=0)
    eng.quit()

    #### Delete the simulated files
    for i in range(Num_sampling):
        os.remove("%d.fsp"%i)
        os.remove("%d_p0.log"%i)
        time.sleep(1)      
    


