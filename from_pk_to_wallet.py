from eth_account import Account

with open('privateKey.txt', 'r') as infile, open('wallets.txt', 'w') as outfile:
    for line in infile:
        privkey = line.strip()
        if privkey:
            try:
                acct = Account.from_key(privkey)
                outfile.write(acct.address + '\n')
            except Exception as e:
                print(f"Ошибка для ключа {privkey}: {e}")