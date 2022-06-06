from flask import Blueprint, request
from redis import Redis
from rq import Queue
from rq.job import Job

bp = Blueprint("job", __name__)

redis = Redis()
rqueue = Queue(connection=redis)

@bp.route('/job', methods=['POST'])
def add_job():
    from app.judge import start_judgement_docker, report_success, report_failure
    from app.database import Testcase

    if not request.is_json:
        return {"error": "WTF, it's not a json"}, 400

    params = request.get_json()

    for case in params['testcase_ids']:
        #print(case)
        testcase = Testcase.query.filter_by(id=case).first()
        input_output = {'id': testcase.id, 'input': testcase.input, 'output': testcase.output}

        try:
            job = Job.create(start_judgement_docker, kwargs={'judge_order': params, 'io_order': input_output}, connection=redis, on_success=report_success, on_failure=report_failure)
            rqueue.enqueue_job(job)
            #result = start_judgement_docker(params, input_output)
            #print(result)
            #return '', 200
        except Exception as e:
            return {"error": str(e)}, 400

    return '', 200