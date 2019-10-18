import torch
from models.NeuMF import NeuMF

NUM_USERS = 53375
NUM_ITEMS = 10000
device = torch.device("cpu")


# NeuMF_model = NeuMF.NeuMF(NUM_USERS+1,NUM_ITEMS+1,16,8).to(device)
# NeuMF_model.load_state_dict(torch.load("./checkpoints/neumf_899.pkg",map_location='cpu'))
neu_model = torch.load("./checkpoints/neumf_model.pkg",map_location='cpu')