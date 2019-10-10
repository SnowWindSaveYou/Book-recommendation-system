import torch
import numpy as np

USER_BIAS = 7

def use_cuda(enabled, device_id=0):
    if enabled:
        assert torch.cuda.is_available(), 'CUDA is not available'
        torch.cuda.set_device(device_id)

def predict(user_id):
    user_id -= USER_BIAS
    user_rating_pair = [(np.zeros((num_items)) + user_id),np.arange(0,num_items,1)]
    local_batch  = torch.tensor(user_rating_pair).type(torch.long).to(device)
    with torch.no_grad():
        y_preds = NeuMF_model(local_batch[0], local_batch[1])
    return y_preds