collector_address = ""

ink_rpc_url = "https://ink.drpc.org"
web3 = Web3(Web3.HTTPProvider(ink_rpc_url))

private_keys = []
with open('privateKey.txt', 'r', encoding='utf-8') as file:
    for line in file:
        key = line.strip()
        if key:
            private_keys.append(key)

gas_limit = 21000

for private_key in private_keys:
    account = web3.eth.account.from_key(private_key)
    address = account.address

    try:
        balance = web3.eth.get_balance(address)
        if balance == 0:
            print(f"Баланс {address} = 0, пропускаем.")
            continue

        gas_price = int(web3.eth.gas_price * 1.1)

        fee = gas_price * gas_limit
        amount = balance - fee

        if amount <= 0:
            print(f"На {address} недостаточно средств для оплаты комиссии. Пропускаем.")
            continue

        nonce = web3.eth.get_transaction_count(address)

        tx = {
            'nonce': nonce,
            'to': Web3.to_checksum_address(collector_address),
            'value': amount,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': 57073,
        }

        signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Собрано {web3.from_wei(amount, 'ether')} ETH с {address}. Тx: {tx_hash.hex()}")

    except Exception as e:
        print(f"Ошибка с кошельком {address}: {e}")