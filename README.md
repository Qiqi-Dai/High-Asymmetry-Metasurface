Implementation code and dataset for the paper "High-Asymmetry Metasurface: A New Solution for Terahertz Resonance via Active Learning-Augmented Diffusion Model" at https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508610.

1. The 68 data samples collectd from existing studies are presented in the folder "dataset".
2. The files related to source-code diffusion model are forked from https://github.com/lucidrains/denoising-diffusion-pytorch/tree/main/denoising_diffusion_pytorch, including "__init__.py", "attend.py", "continuous_time_gaussian_diffusion.py", "denoising_diffusion_pytorch.py", "denoising_diffusion_pytorch_1d.py", "elucidated_diffusion.py", "fid_evaluation.py", "guided_diffusion.py"
3. Lumerical FDTD, MATLAB, and PyTorch should be installed before running.
4. Commands for training and testing the model: python train_auto.py.

If any issues, please feel free to contact daiq0004@e.ntu.edu.sg
