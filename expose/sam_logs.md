START RequestId: 1a77b531-492f-4814-8032-dc4d85b122c9 Version: $LATEST
2021-06-09 10:25:17.463426: W tensorflow/stream_executor/platform/default/dso_loader.cc:60] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2021-06-09 10:25:17.465301: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2021-06-09 10:25:20.572871: I tensorflow/compiler/jit/xla_cpu_device.cc:41] Not creating XLA devices, tf_xla_enable_xla_devices not set
2021-06-09 10:25:20.594936: W tensorflow/stream_executor/platform/default/dso_loader.cc:60] Could not load dynamic library 'libcuda.so.1'; dlerror: libcuda.so.1: cannot open shared object file: No such file or directory
2021-06-09 10:25:20.595244: W tensorflow/stream_executor/cuda/cuda_driver.cc:326] failed call to cuInit: UNKNOWN ERROR (303)
2021-06-09 10:25:20.595946: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (6c02c8600b47): /proc/driver/nvidia/version does not exist
2021-06-09 10:25:20.604994: I tensorflow/core/platform/cpu_feature_guard.cc:142] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
2021-06-09 10:25:20.606725: I tensorflow/compiler/jit/xla_gpu_device.cc:99] Not creating XLA devices, tf_xla_enable_xla_devices not set
2021-06-09 10:25:20.836480: W tensorflow/core/framework/cpu_allocator_impl.cc:80] Allocation of 64000000 exceeds 10% of free system memory.
2021-06-09 10:25:21.049686: W tensorflow/core/framework/cpu_allocator_impl.cc:80] Allocation of 64000000 exceeds 10% of free system memory.
END RequestId: 1a77b531-492f-4814-8032-dc4d85b122c9
REPORT RequestId: 1a77b531-492f-4814-8032-dc4d85b122c9  Init Duration: 0.83 ms  Duration: 4817.60 ms    Billed Duration: 4900 ms        Memory Size: 128 MB        Max Memory Used: 128 MB