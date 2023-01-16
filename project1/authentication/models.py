from django.db import models
from twilio.rest import Client
# Create your models here.
class Database(models.Model):
    entry=models.IntegerField()

class Score(models.Model):
    result=models.PositiveIntegerField()

    def __str__(self):
        return str(self.result)

    def save(self,*args,**kwargs):
        if self.result == 0 or 1:
            x=self.result
            m=""
            if x==1:
                m=f'Machine Has Been Turned ON !'
            else :
                m=f'Machine Has Been Turned OFF !'    
            account_sid ='account_sid'
            auth_token = 'auth_token'
            client = Client(account_sid,auth_token)
            message =client.messages.create(
                body=m,
                from_='number',
                to='+918899858191'
            )
            print(message.sid)
        return super().save(*args,**kwargs)       
