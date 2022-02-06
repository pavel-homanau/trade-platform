from fastapi import FastAPI

app = FastAPI()


@app.get('/ping')
def ping():
    return {'ping': 'pong',
            'other': []}


@app.get('/')
def test():
    # send_email_task()
    return 'success'
