import requests
from pycoin.encoding.hexbytes import h2b
from pycoin.solve.utils import build_hash160_lookup, build_p2sh_lookup, build_sec_lookup
from pycoin.ecdsa.secp256k1 import secp256k1_generator
import sys
sys.path.append('.\\Testtask\Transaction')
import sendtranslib
import json

def send_transaction():
    user = sendtranslib.User()
    transaction = sendtranslib.Transaction(user, int(1e8))
    bcs_network = sendtranslib.Bcs_network()
    bcs_network.create_tx(user, transaction, solver_f=build_hash160_lookup, generator=secp256k1_generator)
    tx = bcs_network.signed_new_tx_hex

    request = requests.post("http://bcs_tester:iLoveBCS@45.32.232.25:3669",
                            json={'method': 'sendrawtransaction', 'params': [tx]})

    decorate_request = requests.post("http://bcs_tester:iLoveBCS@45.32.232.25:3669",

                      json={'method': 'decoderawtransaction', 'params': [tx]})

    return decorate_request

if __name__ == '__main__':
    result = send_transaction()
    print(json.loads(result.text)['result']['txid'])