# -*- coding: utf-8 -*-
"""Untitled17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HmuoPMiFyHlihwzDG2RnhBrKL2maz3eJ
"""

import numpy as np

class SimplifiedBaggingRegressor:
    def __init__(self, num_bags, oob=False):
        self.num_bags = num_bags
        self.oob = oob

    def _generate_splits(self, data: np.ndarray):
        '''
        Generate indices for every bag and store in self.indices_list list
        '''
        self.indices_list = []
        data_length = len(data)
        for bag in range(self.num_bags):
          idx = np.random.choice(data_length, data_length)
          self.indices_list.append(idx)
            # Your Code Here

    def fit(self, model_constructor, data, target):
        '''
        Fit model on every bag.
        Model constructor with no parameters (and with no ()) is passed to this function.

        example:

        bagging_regressor = SimplifiedBaggingRegressor(num_bags=10, oob=True)
        bagging_regressor.fit(LinearRegression, X, y)
        '''
        self.data = None
        self.target = None
        self._generate_splits(data)
        assert len(set(list(map(len, self.indices_list)))) == 1, 'All bags should be of the same length!'
        assert list(map(len, self.indices_list))[0] == len(data), 'All bags should contain `len(data)` number of elements!'
        self.models_list = []
        for bag in range(self.num_bags):
            model = model_constructor()
            data_bag, target_bag = data[self.indices_list[bag]], target[self.indices_list[bag]]# Your Code Here
            self.models_list.append(model.fit(data_bag, target_bag)) # store fitted models here
        if self.oob:
            self.data = data
            self.target = target

    def predict(self, data):
        '''
        Get average prediction for every object from passed dataset
        '''
        # Your code here
        prediction_list = []
        for _, model in enumerate(self.models_list):
          prediction_list.append(model.predict(data))

        result = np.mean(prediction_list, axis = 0)
        return result



    def _get_oob_predictions_from_every_model(self):
        '''
        Generates list of lists, where list i contains predictions for self.data[i] object
        from all models, which have not seen this object during training phase
        '''
        list_of_predictions_lists = [[] for _ in range(len(self.data))]
        # Your Code Here
        for bag in range(self.num_bags):
          model = self.models_list[bag]
          train_indices = self.indices_list[bag]
          for i, item in enumerate(self.data):
            if i not in train_indices:
              list_of_predictions_lists[i].append(model.predict(item.reshape(1, -1)))

        self.list_of_predictions_lists = np.array(list_of_predictions_lists, dtype=object)

    def _get_averaged_oob_predictions(self):
        '''
        Compute average prediction for every object from training set.
        If object has been used in all bags on training phase, return None instead of prediction
        '''
        self._get_oob_predictions_from_every_model()
        self.oob_predictions = []
        for _, item in enumerate(self.list_of_predictions_lists):
          if len(item) == 0:
            self.oob_predictions.append(None)
          else:
            self.oob_predictions.append(np.mean(item))



    def OOB_score(self):
        '''
        Compute mean square error for all objects, which have at least one prediction
        '''
        self._get_averaged_oob_predictions()
        result = 0
        len = 0
        for i, item in enumerate(self.oob_predictions):
          if item != None:
            target = self.target[i]
            result += (item - target)**2
            len += 1
        return result/len

        # Your Code Here