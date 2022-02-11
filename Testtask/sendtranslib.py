from pycoin.networks.bitcoinish import create_bitcoinish_network
import json
import requests
from pycoin.coins.tx_utils import create_tx
from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.encoding.hexbytes import h2b





class User:

    def __init__(self):

        self.user_id = 0
        self.secret_key = 'L3CsPqiKfRiJw9R97pDYrdYUDXU6n4J8STDABSQfcLoEg9cou8FZ'
        self.sender = 'B96aBZv79fTHpS7yA6XD2P6Kb9uSEs14E2'

class Transaction():
    def __init__(self, User, amount):

        self.hex_definition = " "
        self.transaction_annotation = " "
        self.amount = int(amount)

def get_utxo(user):
    utxo = requests.get(f'https://bcschain.info/api/address/{user.sender}/utxo')
    utxo = json.loads(utxo.text)[0]
    return utxo

class Bcs_network:
    def __init__(self):

        self.network = create_bitcoinish_network(symbol = '', network_name = 'BCS Chain', subnet_name = '',
                                                 wif_prefix_hex="80", address_prefix_hex="19",
                                                 pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
                                                 bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc",
                                                 bip49_prv_prefix_hex="049d7878",
                                                 bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
                                                 bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3",
                                                 default_port=3666)



    def send_rpc(self, method: str):
        address_reciever = requests.post('http://bcs_tester:iLoveBCS@45.32.232.25:3669',json={'method': method})
        return address_reciever

    def create_tx(self, user, transaction, solver_f, generator):
        utxo = get_utxo(user)
        address_reciever = json.loads(self.send_rpc('getnewaddress').text)['result']


        self.spendables = Spendable(coin_value=int(utxo['value']), script=h2b(utxo['scriptPubKey']),
                                    tx_hash=byte_reverse(h2b(utxo['transactionId'])), tx_out_index=int(utxo['outputIndex']))

        value_temp_transaction = int(utxo['value'] - 1.1*transaction.amount)

        self.unsigned_tx = create_tx(
            network=self.network,
            spendables=[self.spendables],
            payables=[tuple([address_reciever, transaction.amount]), tuple([user.sender, value_temp_transaction])],
            version=1
        )

        self.unsigned_tx_hex = self.unsigned_tx.as_hex()
        key_wif = self.network.parse.wif(user.secret_key)
        exponent = key_wif.secret_exponent()
        solver = solver_f([exponent], [generator])

        self.signed_new_tx = self.unsigned_tx.sign(solver)
        self.signed_new_tx_hex = self.signed_new_tx.as_hex()



def byte_reverse(byte):

    byte_list = bytearray(byte)
    byte_list.reverse()
    byte = bytes(byte_list)

    return byte