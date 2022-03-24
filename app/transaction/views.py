from django.http import Http404
from rest_framework import viewsets, views, response, status

from .models import Transaction, TransactionAccount
from .serializers import TransactionSerializer, TransactionAccountSerializer


class TransactionAccountViewSet(viewsets.ModelViewSet):
    queryset = TransactionAccount.accounts.all()
    serializer_class = TransactionAccountSerializer


class TransactionListView(views.APIView):

    def get(self, request):
        transfers = Transaction.objects.all()
        serializer = TransactionSerializer(transfers, many=True)
        return response.Response(data=serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(views.APIView):

    def get_object(self, pk):
        try:
            Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        transfer = self.get_object(pk=pk)
        serializer = TransactionSerializer(transfer)
        return response.Response(serializer.data)

    def delete(self, request, pk):
        transfer = self.get_object(pk=pk)
        transfer.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

