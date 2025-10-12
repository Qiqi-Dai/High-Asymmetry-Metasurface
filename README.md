Implementation code and dataset for the paper "High-Asymmetry Metasurface: A New Solution for Terahertz Resonance via Active Learning-Augmented Diffusion Model" at https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508610.

1. The 68 data samples collectd from existing studies are presented in the folder "dataset".
2. The files related to source-code diffusion model are directly forked from https://github.com/lucidrains/denoising-diffusion-pytorch/tree/main/denoising_diffusion_pytorch, including "init.py", "attend.py", "continuous_time_gaussian_diffusion.py", "denoising_diffusion_pytorch.py", "denoising_diffusion_pytorch_1d.py", "elucidated_diffusion.py", "fid_evaluation.py", "guided_diffusion.py", "karras_unet.py", "karras_unet_1d.py", "karras_unet_3d.py", "learned_gaussian_diffusion.py", "simple_diffusion.py", "v_param_continuous_time_gaussian_diffusion.py", "version.py", and "weighted_objective_gaussian_diffusion.py". 
3. Lumerical FDTD, MATLAB, and PyTorch should be installed before running.
4. Commands for automatically training and testing the iterative model: python train_auto.py.

If any problems, please release them in Issues.
