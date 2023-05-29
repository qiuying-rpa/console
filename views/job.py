"""

By Ziqiu Li
Created at 2023/5/26 14:31
"""
from flask import current_app as app
from apiflask.views import MethodView
from schemas.job import JobIn, JobOut
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

    @app.input(JobIn)
    def patch(self, job_id, job_in):
        code, res = job_service.update_job(job_id, job_in)
        return make_resp(code, res, msg="Updated.")


class Jobs(MethodView):
    @app.output(EmptySchema)
    @app.input(IdsIn)
    def delete(self, ids_in):
        job_service.delete_many_job(ids_in["ids"])

    @app.input(JobIn, "query")
    @app.output(JobOut(many=True))
    def get(self, job_in):
        if job_in:
            jobs = job_service.find_jobs_by(job_in)
        else:
            jobs = job_service.list_all_jobs()
        return make_resp(res=jobs)


app.add_url_rule("/console/job/<job_id>", view_func=Job.as_view("job"))
app.add_url_rule("/console/job", view_func=Job.as_view("createJob"))
app.add_url_rule("/console/jobs", view_func=Jobs.as_view("jobs"))
