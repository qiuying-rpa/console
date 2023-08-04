"""

By Ziqiu Li
Created at 2023/5/26 14:31
"""
from flask import current_app as app
from apiflask.views import MethodView
from schemas.job import JobIn, JobOut, JobQuery
from apiflask.schemas import EmptySchema
from schemas.common import IdsIn
import services.job as job_service
from utils.response import make_resp
from datetime import datetime


class Job(MethodView):
    @app.output(JobOut)
    def get(self, job_id):
        code, res = job_service.find_job(job_id)
        return make_resp(code, res)

    @app.input(JobIn)
    def patch(self, job_id, job_in):
        code, res = job_service.update_job(job_id, job_in)
        return make_resp(code, res, msg="Updated.")

    @app.output(EmptySchema)
    def delete(self, job_id):
        job_service.delete_job(job_id)


class Jobs(MethodView):
    @app.input(JobIn)
    def post(self, job_in):
        code, res = job_service.create_job(
            process_id=job_in["process_id"],
            param_config_id=job_in["param_config_id"],
            remark=job_in.get("remark"),
            plan_run_time=job_in.get("plan_run_time")
            if job_in.get("plan_run_time")
            else datetime.now(),
        )
        return make_resp(code, res, msg="Created.")

    @app.output(EmptySchema)
    @app.input(IdsIn)
    def delete(self, ids_in):
        job_service.delete_jobs(ids_in["ids"])

    @app.input(JobQuery, "query")
    @app.output(JobOut(many=True))
    def get(self, job_in):
        pagination = job_service.find_jobs(job_in)
        return make_resp(pagination=pagination)


app.add_url_rule("/console/job/<job_id>", view_func=Job.as_view("job"))
app.add_url_rule("/console/jobs", view_func=Jobs.as_view("jobs"))
