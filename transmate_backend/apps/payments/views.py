from django.utils import timezone
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import *
from .gateways import BkashGateway, NagadGateway
from .invoice import generate_invoice_pdf
from apps.users.permissions import IsCustomerUserRole, IsAdminUserRole
class CustomerPaymentListCreateView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request): return Response(PaymentDetailSerializer(Payment.objects.filter(customer=request.user).order_by('-created_at'),many=True).data)
    def post(self,request):
        s=PaymentCreateSerializer(data=request.data, context={'request':request})
        if s.is_valid(): p=s.save(); return Response({'message':'Payment record created successfully.','payment':PaymentDetailSerializer(p).data}, status=201)
        return Response(s.errors,status=400)
class CustomerPaymentDetailView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request,payment_id):
        try:p=Payment.objects.get(id=payment_id,customer=request.user)
        except Payment.DoesNotExist:return Response({'detail':'Payment not found.'},status=404)
        return Response(PaymentDetailSerializer(p).data)
class CustomerConfirmPaymentView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def patch(self,request,payment_id):
        try:p=Payment.objects.get(id=payment_id,customer=request.user)
        except Payment.DoesNotExist:return Response({'detail':'Payment not found.'},status=404)
        if p.status not in ['PENDING','INITIATED']: return Response({'detail':'Only pending payments can be confirmed.'},status=400)
        s=PaymentConfirmSerializer(data=request.data)
        if s.is_valid(): p.status='PAID'; p.transaction_id=s.validated_data.get('transaction_id',p.transaction_id); p.paid_at=timezone.now(); p.save(); return Response({'message':'Payment confirmed successfully.','payment':PaymentDetailSerializer(p).data})
        return Response(s.errors,status=400)
class CustomerInitiateGatewayPaymentView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def patch(self,request,payment_id):
        try:p=Payment.objects.get(id=payment_id,customer=request.user)
        except Payment.DoesNotExist:return Response({'detail':'Payment not found.'},status=404)
        if p.status not in ['PENDING','FAILED']: return Response({'detail':'Only pending or failed payments can be initiated.'},status=400)
        try:
            gw = BkashGateway() if p.payment_method=='BKASH' else NagadGateway() if p.payment_method=='NAGAD' else None
            if not gw: return Response({'detail':'Gateway initiation is only available for BKASH and NAGAD.'},status=400)
            res=gw.create_payment(p); p.gateway_payment_id=res.get('paymentID') or res.get('payment_reference'); p.gateway_callback_url=res.get('bkashURL') or res.get('checkout_url'); p.gateway_response=res; p.status='INITIATED'; p.save(); return Response({'message':f'{p.payment_method} payment initiated.','checkout_url':p.gateway_callback_url,'payment':PaymentDetailSerializer(p).data})
        except Exception as exc: p.status='FAILED'; p.gateway_response={'error':str(exc)}; p.save(); return Response({'detail':'Payment gateway initiation failed.','error':str(exc)},status=400)
class CustomerExecuteBkashPaymentView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def patch(self,request,payment_id):
        try:p=Payment.objects.get(id=payment_id,customer=request.user)
        except Payment.DoesNotExist:return Response({'detail':'Payment not found.'},status=404)
        if p.payment_method!='BKASH': return Response({'detail':'This endpoint is only for bKash payments.'},status=400)
        res=BkashGateway().execute_payment(p.gateway_payment_id); p.transaction_id=res.get('trxID'); p.gateway_response=res; p.status='PAID' if p.transaction_id else 'FAILED'; p.paid_at=timezone.now() if p.transaction_id else None; p.save(); return Response({'message':'bKash payment execution completed.','payment':PaymentDetailSerializer(p).data})
class CustomerDownloadInvoiceView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request,payment_id):
        try:p=Payment.objects.get(id=payment_id,customer=request.user)
        except Payment.DoesNotExist:return Response({'detail':'Payment not found.'},status=404)
        if p.status!='PAID': return Response({'detail':'Invoice is only available for paid payments.'},status=400)
        return FileResponse(generate_invoice_pdf(p), as_attachment=True, filename=f'transmate_invoice_{p.id}.pdf')
class AdminPaymentListView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request):
        qs=Payment.objects.all().order_by('-created_at'); sf=request.query_params.get('status'); mf=request.query_params.get('method')
        if sf: qs=qs.filter(status=sf.upper())
        if mf: qs=qs.filter(payment_method=mf.upper())
        return Response(PaymentDetailSerializer(qs,many=True).data)
class AdminPaymentDetailView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request,payment_id):
        try:p=Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:return Response({'detail':'Payment not found.'},status=404)
        return Response(PaymentDetailSerializer(p).data)
class AdminRefundPaymentView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self,request,payment_id):
        try:p=Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:return Response({'detail':'Payment not found.'},status=404)
        if p.status!='PAID': return Response({'detail':'Only paid payments can be refunded.'},status=400)
        p.status='REFUNDED'; p.save(); return Response({'message':'Payment refunded successfully.','payment':PaymentDetailSerializer(p).data})
