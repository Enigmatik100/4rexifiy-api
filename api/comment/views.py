from flask_restx import Namespace, Resource

comment_namespace = Namespace('comment', description="a namespace for the comment")


@comment_namespace.route('/comments')
class AddCommentToPost(Resource):

    def post(self):
        return {"message": "Helo post"}
