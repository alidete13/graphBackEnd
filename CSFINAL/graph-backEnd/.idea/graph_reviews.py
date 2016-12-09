import webapp2

import json

from review import graph_product

from product import Product


class AverageGraphHandler(webapp2.RequestHandler):

    def post(self):

        payload_string = self.request.body
        payload_dict = json.loads(payload_string)
        product_id = payload_dict["graph_id"]
        graphs = sketch_product(product_id)
        graph_len = len(reviews)

        if graph == 0:
            print("graph")
            return

        rating_accumulator = 0.0

        for graph:
            graph_accumulator += graph.rating

        average_rating = graph_accumulator / reviews_len

        product = Product(id=product_id)
        product.average_graph = average_rating
        product.put()

app = webapp2.WSGIApplication([
    webapp2.Route(r'/_ah/queue/average-ratings', handler=AverageRatingsHandler, name='average-ratings-for-product'),
])
