from django.http import HttpResponse
import sys
sys.path.append('.\\Testtask\Transaction')
from . import models
from django.shortcuts import render
from .forms import Button
import json


import requests

from pycoin.solve.utils import build_hash160_lookup, build_p2sh_lookup, build_sec_lookup
from pycoin.ecdsa.secp256k1 import secp256k1_generator
import sys
import sendtranslib
from .models import Data_base_Transaction


def send_transaction():
    user = sendtranslib.User()
    transaction = sendtranslib.Transaction(user, int(1e8))
    bcs_network = sendtranslib.Bcs_network()
    bcs_network.create_tx(user, transaction, solver_f=build_hash160_lookup, generator=secp256k1_generator)
    tx = bcs_network.signed_new_tx_hex

    requests.post("http://bcs_tester:iLoveBCS@45.32.232.25:3669",
                            json={'method': 'sendrawtransaction', 'params': [tx]})


    return requests.post("http://bcs_tester:iLoveBCS@45.32.232.25:3669",
                                     json={'method': 'decoderawtransaction', 'params': [tx]})

def post_new(request):
    return render(request,
                  "base_generic.html")

def button_pushed(request):
    if request.method == 'POST':
        result = send_transaction()
        tx = models.Data_base_Transaction()
        tx.Txid = json.loads(result.text)['result']['txid']
        tx.description = ''
        tx.save()

    return render(request,
                  "base_generic.html")