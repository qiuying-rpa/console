"""

By Ziqiu Li
Created at 2023/5/25 14:11
"""
from flask import current_app as app
from schemas.robot import RobotIn, RobotOut
from schemas.common import IdsIn
from apiflask.views import MethodView
import services.robot as robot_services
from apiflask.schemas import EmptySchema
from utils.response import make_resp


class Robot(MethodView):
    @app.output(RobotOut)
    def get(self, robot_id):
        code, res = robot_services.find_robot(robot_id)
        return make_resp(code, res)

    @app.input(RobotIn)
    def post(self, robot_in):
        code, res = robot_services.create_robot(
            name=robot_in["name"],
            ip=robot_in.get("ip"),
            desc=robot_in.get("desc"),
            owner_id=robot_in.get("owner_id"),
            group_id=robot_in.get("group_id"),
        )
        return make_resp(code, res, "Created.")

    @app.input(RobotIn)
    def patch(self, robot_id, robot_in):
        code, res = robot_services.update_robot(robot_id, robot_in)
        return make_resp(code, res, "Updated.")


class Robots(MethodView):
    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, ids_in):
        robot_services.delete_many_robots(ids_in["ids"])

    @app.input(RobotIn, "query")
    @app.output(RobotOut(many=True))
    def get(self, robots_in):
        if robots_in:
            robots = robot_services.find_robots_by(robots_in)
        else:
            robots = robot_services.list_all_robot()
        return make_resp(res=robots)


app.add_url_rule("/console/robot/<robot_id>", view_func=Robot.as_view("robot"))
app.add_url_rule("/console/robot", view_func=Robot.as_view("createRobot"))
app.add_url_rule("/console/robots", view_func=Robots.as_view("robots"))
