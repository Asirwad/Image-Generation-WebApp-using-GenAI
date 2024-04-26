import torch


def get_gpu_info():
    gpu_info_str = ""

    # Check if CUDA is available
    if torch.cuda.is_available():
        # Get the number of available GPUs
        gpu_count = torch.cuda.device_count()
        gpu_info_str += f"Number of available GPUs: {gpu_count} ,"

        # Iterate through each GPU
        for i in range(gpu_count):
            gpu_device = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024 ** 3)  # Convert bytes to GB
            gpu_info_str += f"GPU {i + 1}: {gpu_device}, Memory: {gpu_memory:.2f}GB\n"
    else:
        gpu_info_str += "CUDA is not available. You are using CPU."

    return gpu_info_str

