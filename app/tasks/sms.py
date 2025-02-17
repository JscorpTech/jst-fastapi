from app.celery_app import app
from typing import  Union, Optional
from app.services.sms import EskizService

@app.task(name='send_sms')
def send_message(phone: Optional[Union[str, int]], message: Optional[Union[str]]) -> None:
    print(phone, message)
    response = EskizService().send_sms(phone, message)
    print(response)