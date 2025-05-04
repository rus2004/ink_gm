from web3 import Web3
import time

def send_tokens_to_multiple_recipients(recipient_addresses):
    ink_rpc_url = "https://ink.drpc.org"
    web3_eth = Web3(Web3.HTTPProvider(ink_rpc_url))

    sender_address = ""
    private_key = ""
    amount_eth = 0.0000055555

    nonce = web3_eth.eth.get_transaction_count(sender_address)

    for recipient_address in recipient_addresses:
        checksum_address = Web3.to_checksum_address(recipient_address)

        tx = {
            'nonce': nonce,
            'to': checksum_address,
            'value': web3_eth.to_wei(amount_eth, 'ether'),
            'gas': 21000,
            'gasPrice': int(web3_eth.eth.gas_price * 1.1),
            'chainId': 57073,
        }

        signed_tx = web3_eth.eth.account.sign_transaction(tx, private_key=private_key)

        tx_hash = web3_eth.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Транзакция отправлена на адрес {recipient_address}. Хэш транзакции: {tx_hash.hex()}")

        nonce += 1
        time.sleep(10)

wallets = []
with open('wallets.txt', 'r', encoding='utf-8') as file:
    for line in file:
        wallets.append(line.strip())

send_tokens_to_multiple_recipients(wallets)