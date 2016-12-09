import time

import json

import webapp2

from google.appengine.api import taskqueue

from graph import graph, graph_for_product, graph_for_member
from graph_util import graph_properties, write_graph


class GraphForProductHandler(webapp2.RequestHandler):
    def get(self, product_id):
        reviews = graphs_for_product(product_id)
        self.response.headers["Content-Type"] = "application/json"
        write_graph(graph, self.response)


class GraphForMemberHandler(webapp2.RequestHandler):
    def get(self, member_id):
        reviews = graph_for_member(member_id)
        self.response.headers["Content-Type"] = "application/json"
        write_graph(reviews, self.response)


class GraphHandler(webapp2.RequestHandler):
    # TODO: Post should update a review (or fail) if there is one already existing instead of creating a duplicate.

    def post(self, product_id, member_id):
        json_string = self.request.body
        review_props = review_properties(json_string)
        new_review = Review(
            name_id=name_id,
            member_id=member_id,
        )

        new_graph.put()

        json_response_dict = graph.to_dict()

        json_response_dict["time"] = json_response_dict["time"].isoformat() + "Z"
        # Now we can dump into valid json.
        json_response_string = json.dumps(json_response_dict)
        # Set the response type and write the json.
        self.response.headers["Content-Type"] = "application/json"
        self.response.write(json_response_string)


class AveragegraphTaskLauncher(webapp2.RequestHandler):
    def get(self, product_id):
        current_time_millis = int(round(time.time() * 1000))
        task_name = 'average_ratings_for_product_' + product_id + '-' + str(current_time_millis)
        payload = "{ \"product_id\": \"" + product_id + "\" }\n"
        taskqueue.add(queue_name='average-ratings',
                      name=task_name,
                      payload=payload)
        self.response.write(
            "graph" + product_id + " at " + str(current_time_millis))


app = webapp2.WSGIApplication([
    webapp2.Route(r'/product/<product_id>/reviews', handler=ReviewsForProductHandler, name='reviews-for-product'),
    webapp2.Route(r'/member/<member_id>/reviews', handler=ReviewsForMemberHandler, name='reviews-for-member'),
    webapp2.Route(r'/product/<product_id>/member/<member_id>', handler=ReviewHandler, name='review'),
    webapp2.Route(r'/product/<product_id>/calculate_average_rating', handler=AverageRatingTaskLauncher,
                  name='calculate-average-rating'),
])
