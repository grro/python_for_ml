from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from estimator import HousePriceEstimator


class HousePriceEstimatorResource(Resource):  # inherits from Resource

    def __init__(self, estimator):
        self.estimator = estimator

    def post(self):
        house = request.get_json()  # parse the request payload as json
        predicted_price = self.estimator.predict_prices([house])[0]
        return jsonify(price=predicted_price,
                       date=datetime.now())


estimator = HousePriceEstimator.load('estimator.p')
estimator_app = Flask(__name__)  # application object used by the WSGI server
api = Api(estimator_app)
api.add_resource(HousePriceEstimatorResource, '/predict', resource_class_kwargs={'estimator': estimator})


estimator_app.run(host="127.0.0.1", port=8080, debug=True)
# curl -H'Content-Type: application/json' -d'{"MSSubClass": 60, "LotArea": 8450, "OverallQual": 67,  "OverallCond": 55, "YrSold": 56}' -XPOST http://127.0.0.1:8080/predict
