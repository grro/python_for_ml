import pickle
from sklearn.linear_model import LinearRegression


class HousePriceEstimator:

    def __init__(self):
        self.model = LinearRegression()

    def extract_core_features_list(self, house_list):
        return [self.extract_core_features(house) for house in house_list]

    def extract_core_features(self, house):
        # returns the most relevant features as numeric values
        return [house['MSSubClass'],
                house['LotArea'],
                house['OverallQual'],
                house['OverallCond'],
                int(house['YrSold'])]

    def train(self, house_list, price_list):
        features_list = self.extract_core_features_list(house_list)
        self.model.fit(features_list, price_list)

    def predict_price(self, house):
        return self.predict_prices([house])[0]

    def predict_prices(self, house_list):
        features_list = self.extract_core_features_list(house_list)
        return self.model.predict(features_list)

    def save(self, model_filename: str):
        pickle.dump(self.model, open(model_filename, 'wb'))

    @staticmethod
    def load(model_filename: str):
        estimator = HousePriceEstimator()
        estimator.model = pickle.load(open(model_filename, 'rb'))
        return estimator

