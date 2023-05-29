"""

By Ziqiu Li
Created at 2023/5/26 14:30
"""
from utils import repository
from models.job import Job
from models.process import Process
from models.param_config import ParamConfig
from flask import g


def create_job(
    process_id: str, param_config_id: str, plan_run_time, remark: str
) -> tuple[int, str]:
    process = repository.find_one(Process, process_id)
    if process is None:
        return 1, f"Process {process_id} not found."
    param_config = repository.find_one(ParamConfig, param_config_id)
    if param_config is None:
        return 2, f"Param config {param_config_id} not found."
    job = repository.create_one(
        Job,
        creator_id=g.current_user["id"],
        process_id=process_id,
        param_config_id=param_config_id,
        plan_run_time=plan_run_time,
        remark=remark,
    )
    return 0, job.id


def delete_many_job(job_ids: list[str]) -> None:
    repository.delete_many(Job, job_ids)


def update_job(job_id: str, prop: dict) -> tuple[int, str]:
    return repository.update_one(Job, job_id, **prop)


def find_job(job_id: str):
    job = repository.find_one(Job, job_id)
    if job is None:
        return 1, f"Job {job_id} not found."
    else:
        return 0, job


def find_jobs_by(props: dict):
    return repository.find_many_by(Job, **props)


def list_all_jobs():
    return repository.list_all(Job)
