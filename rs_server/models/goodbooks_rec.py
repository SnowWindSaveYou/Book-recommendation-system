#!/usr/bin/python

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from math import sqrt
import time
import psutil
import os
import pickle


def load_data():
	header = ['book_id', 'user_id', 'rating']
	dataset = pd.read_csv("./ratings.csv")
	train, test = train_test_split(dataset, test_size=0.2)
	n_users = len(dataset.user_id.unique())
	n_books = len(dataset.book_id.unique())
	print(n_users, n_books)
	return dataset, train, test, n_users, n_books

def cal_sim(dataset_data, train_data, test_data, n_users, n_books):

#	def _cosine_similarity(vector1, vector2):
#		new_vector1 = []
#		new_vector2 = []
#		for i, cur in enumerate(vector1):
#			if vector1[i] != 0 and vector2[i] != 0:
#				new_vector1.append(vector1[i])
#				new_vector2.append(vector2[i])
#		dot_product = 0.0
#		normA = 0.0
#		normB = 0.0
#		for a, b in zip(new_vector1, new_vector2):
#			dot_product += a * b
#			normA += a ** 2
#			normB += b ** 2
#		if normA == 0.0 or normB == 0.0:
#			return 0
#		else:
#			return round(dot_product / ((normA**0.5)*(normB**0.5)), 2)

	train_data_matrix = np.zeros((n_users, n_books))
	for line in train_data.values:
		train_data_matrix[int(line[1])-1, int(line[0])-1] = line[2]
		
	test_data_matrix = np.zeros((n_users, n_books))
	for line in test_data.values:
		test_data_matrix[int(line[1]) - 1, int(line[0]) - 1] = line[2]
	
#	for i in range(n_users):
#		for j in range(n_books):
#			if train_data_matrix[i][j] == 0:
#				train_data_matrix[i][j] = 3
#			if test_data_matrix[i][j] == 0:
#				test_data_matrix[i][j] = 3
	dataset_data_matrix = np.zeros((n_users, n_books))
	for line in dataset_data.values:
		dataset_data_matrix[int(line[1]) - 1, int(line[0]) - 1] = line[2]
	
	item_similarity = cosine_similarity(train_data_matrix.T, dense_output=True)
# 	item_similarity = np.zeros((n_books, n_books))
#	for i, cur in enumerate(item_similarity):
#		for j,v in enumerate(cur):
#			if item_similarity[i][j] == 0:
#				item_similarity[i][j] = _cosine_similarity(train_data_matrix.T[i], train_data_matrix.T[j])
#				item_similarity[j][i] = item_similarity[i][j]
				
#	print(train_data_matrix, test_data_matrix, item_similarity)
	print(item_similarity.shape)
	print(item_similarity)
	return dataset_data_matrix, train_data_matrix, test_data_matrix, item_similarity
	
def predict(ratings, similarity):
	pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
	for line in pred:
		line[np.isnan(line)] = np.nanmean(line)
	print (pred.shape)
	print (pred)
	return pred

#def predict(ratings, similarity, n_users, n_books):
#	pred = np.zeros((n_users, n_books))
#	for i, cur in enumerate(pred):
#		for j,v in enumerate(cur):
#			fenzi = 0
#			fenmu = 0
#			for k, x in enumerate(ratings[i]):
#				if x != 0:
#					fenzi += x*similarity[j][k]
#					fenmu += np.abs(similarity[j][k])
#			if fenmu == 0:
#				pred[i][j] = 3
#			else:
#				pred[i][j] = fenzi/fenmu
#	for line in pred:
#		line[np.isnan(line)] = np.nanmean(line)
#	print (pred.shape)
#	print (pred)
#	return pred

		
def rmsefun(prediction, ground_truth):
	prediction = prediction[ground_truth.nonzero()].flatten()
	ground_truth = ground_truth[ground_truth.nonzero()].flatten()
	return sqrt(mean_squared_error(prediction, ground_truth))

def write_res_to_file():
	begin = time.time()
	dataset, train, test, n_users, n_books = load_data()
	dataset_data_matrix, train_data_matrix, test_data_matrix, item_similarity = cal_sim(dataset, train, test, n_users, n_books)
	item_pred = predict(train_data_matrix, item_similarity)
	item_rmse = rmsefun(item_pred, test_data_matrix)
	print("item_rmse model RMSE : %.3f"%(item_rmse))
	pkl_item_pred = []
	pkl_item_sim = []
	# rec
	for i, line in enumerate(item_pred):
		for j, cur in enumerate(line):
			if dataset_data_matrix[i][j] > 0:
				item_pred[i][j] = 0
		pkl_item_pred.append(np.argmax(line) + 1)
	for i, line in enumerate(item_similarity):
		for j, cur in enumerate(line):
			if i == j:
				item_similarity[i][j] = 0
		pkl_item_sim.append(np.argmax(line) + 1)
	f1 = open("./item_pred.pkl", "wb")
	f2 = open("./item_similarity.pkl", "wb")
	pickle.dump(pkl_item_pred, f1)
	pickle.dump(pkl_item_sim, f2)
#		print("recommend " + str(i) + "th user " + str(np.argmax(line) + 1) + "th book")
	end = time.time()
	print("cost time : " + str(round(end - begin)) + "s")
	info = psutil.virtual_memory()
	print('cost memory' + str(psutil.Process(os.getpid()).memory_info().rss) + "kb")

def get_item_results(user_id):
	f1 = open("./item_pred.pkl", "rb")
	reslist = pickle.load(f1)
	print("recommend " + str(user_id) + "th user " + str(reslist[user_id-1]) + "th book")
	
def get_simi_item_results(item_id):
	f2 = open("item_similarity.pkl", "rb")
	itemlist = pickle.load(f2)
	print("The book " + str(item_id) + " most sim book is " + str(itemlist[item_id-1]) + "th book")
	
if __name__ == '__main__':
	write_res_to_file()
	get_item_results(100)
	get_simi_item_results(100)
	
	
	