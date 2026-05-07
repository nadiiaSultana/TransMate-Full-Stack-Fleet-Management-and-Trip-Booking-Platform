import uuid, requests
from django.conf import settings
class BkashGateway:
    def __init__(self): self.base_url=settings.BKASH_BASE_URL; self.app_key=settings.BKASH_APP_KEY; self.app_secret=settings.BKASH_APP_SECRET; self.username=settings.BKASH_USERNAME; self.password=settings.BKASH_PASSWORD
    def _headers(self, token=None):
        h={'Content-Type':'application/json','x-app-key':self.app_key}
        if token: h['Authorization']=f'Bearer {token}'
        return h
    def grant_token(self):
        if not all([self.app_key,self.app_secret,self.username,self.password]): return {'id_token':'demo-token'}
        r=requests.post(f'{self.base_url}/token/grant',json={'app_key':self.app_key,'app_secret':self.app_secret},headers={'Content-Type':'application/json','x-app-key':self.app_key,'x-app-secret':self.app_secret},auth=(self.username,self.password),timeout=30); r.raise_for_status(); return r.json()
    def create_payment(self,payment):
        if not all([self.app_key,self.app_secret,self.username,self.password]): return {'paymentID':f'DEMO-BKASH-{payment.id}-{uuid.uuid4().hex[:6]}','bkashURL':settings.FRONTEND_PAYMENT_SUCCESS_URL,'demo':True}
        token=self.grant_token().get('id_token'); payload={'mode':'0011','payerReference':str(payment.customer.phone or payment.customer.id),'callbackURL':settings.FRONTEND_PAYMENT_SUCCESS_URL,'amount':str(payment.amount),'currency':'BDT','intent':'sale','merchantInvoiceNumber':f'TM-{payment.id}-{uuid.uuid4().hex[:8]}'}; r=requests.post(f'{self.base_url}/create',json=payload,headers=self._headers(token),timeout=30); r.raise_for_status(); return r.json()
    def execute_payment(self,gateway_payment_id):
        if gateway_payment_id.startswith('DEMO-'): return {'trxID':f'TRX-{uuid.uuid4().hex[:10]}','paymentID':gateway_payment_id,'demo':True}
        token=self.grant_token().get('id_token'); r=requests.post(f'{self.base_url}/execute',json={'paymentID':gateway_payment_id},headers=self._headers(token),timeout=30); r.raise_for_status(); return r.json()
class NagadGateway:
    def create_payment(self,payment): return {'status':'sandbox_placeholder','payment_reference':f'NAGAD-{payment.id}-{uuid.uuid4().hex[:8]}','checkout_url':settings.FRONTEND_PAYMENT_SUCCESS_URL}
    def verify_payment(self,ref): return {'status':'verified_placeholder','payment_reference':ref}
