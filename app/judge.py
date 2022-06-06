import docker
from app.database import TestResult

def report_success(job, connection, result, *args, **kwargs):
    from app import create_app, db

    app = create_app()
    app.app_context().push()

    if result['is_match']:
        test_result = TestResult(result['assignment_id'], result['testcase_id'], True, '')
    else:
        test_result = TestResult(result['assignment_id'], result['testcase_id'], False, 'Testcase mismatch')

    db.session.add(test_result)
    db.session.commit()

def report_failure(job, connection, type, value, traceback):
    print(traceback)

def start_judgement_docker(**kwargs):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    #print("ok")
    
    target_lang = "java" #hardcoded
    target_launchname = kwargs['judge_order']['filename'].split(".")[0]

    if target_lang == 'java':
        #print(judge_order['assignment_id'])
        #print(target_launchname)
        #print(io_order['input'])
        image, logs = client.images.build(path="./", dockerfile="dockerfiles/java.dockerfile", buildargs={'assignment_id': str(kwargs['judge_order']['assignment_id'])})

        #for chunk in logs:
        #    if 'stream' in chunk:
        #        for line in chunk['stream'].splitlines():
        #            print(line)
        env = ["MAIN_CLASS=" + target_launchname, "TEST_INPUT=" + kwargs['io_order']['input']]
        print(env)
        output = client.containers.run(image, auto_remove=False, environment=env, stdout=True, stderr=True)

        print("Got this: ", output.decode('UTF-8').strip())
        print("expected: ", kwargs['io_order']['output'])

        if output.decode('UTF-8').strip() == kwargs['io_order']['output']:
            return {'assignment_id': kwargs['judge_order']['assignment_id'], 'testcase_id': kwargs['io_order']['id'], 'is_match': True}
        else:
            return {'assignment_id': kwargs['judge_order']['assignment_id'], 'testcase_id': kwargs['io_order']['id'], 'is_match': False}