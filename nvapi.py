from nvidia_smi import (
    NVML_TEMPERATURE_GPU,
    NVMLError,
    nvmlInit, nvmlShutdown,
    nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetTemperature, nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetEnforcedPowerLimit, nvmlDeviceGetPowerUsage,
    nvmlDeviceGetUtilizationRates
)


import pprint

KB = 1024.0
MB = KB * 1024
GB = MB * 1024



def nvapi():
    nvmlInit()
    ret = {}
    n_gpus = int(nvmlDeviceGetCount())
    ret['n_gpus'] = n_gpus
    for i in range(n_gpus):
        gpu_str = '{}.'.format(i)
        gpu_obj = nvmlDeviceGetHandleByIndex(i)
        ret[gpu_str + 'temp'] = nvmlDeviceGetTemperature(gpu_obj, NVML_TEMPERATURE_GPU)
        this_ram = nvmlDeviceGetMemoryInfo(gpu_obj)
        ret[gpu_str + 'ram.used'] = this_ram.used / MB
        ret[gpu_str + 'ram.total'] = this_ram.total / MB
        ret[gpu_str + 'power.current'] = nvmlDeviceGetPowerUsage(gpu_obj) / 1000.0
        ret[gpu_str + 'power.limit'] = nvmlDeviceGetEnforcedPowerLimit(gpu_obj) / 1.0
        ret[gpu_str + 'util'] = nvmlDeviceGetUtilizationRates(gpu_obj).gpu / 1.0
    nvmlShutdown()
    return ret

if __name__ == '__main__':
    pprint.pprint(nvapi())
