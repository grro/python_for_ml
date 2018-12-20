from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from estimator import HousePriceEstimator


class HousePriceEstimatorResource(Resource):

    def __init__(self, price_estimator):
        self.price_estimator = price_estimator

    def post(self):
        house = request.get_json()  # parse the input as json
        predicted_price = self.price_estimator.predict_prices([house])[0]
        return jsonify(price=predicted_price, date=datetime.now())


estimator_app = Flask(__name__)
api = Api(estimator_app)
estimator = HousePriceEstimator.load('estimator.p')
api.add_resource(HousePriceEstimatorResource, '/predict', resource_class_kwargs={'price_estimator': estimator})
estimator_app.run(host="127.0.0.1", port=8080, debug=True)

# curl -H'Content-Type: application/json' -d'{"MSSubClass": 60, "LotArea": 8450, "OverallQual": 67,  "OverallCond": 55, "YrSold": 56}' -XPOST http://127.0.0.1:8080/predict
