keyname=test
home=/data-01/sei-data
password=123456789

seid=~/go/bin/seid
code=$(printf $password | $seid tx wasm store /data-01/data_oracle.wasm -y --home $home --node https://rpc.atlantic-2.seinetwork.io/ --from=$keyname --chain-id=atlantic-2 --gas=10000000 --fees=10000000usei --broadcast-mode=block | grep -A 1 "code_id" | sed -n 's/.*value: "//p' | sed -n 's/"//p')
printf "Code id is %s\n" $code
admin_addr=$(printf $password |$seid keys show $keyname --home $home | grep -A 1 "address" | sed -n 's/.*address: //p')
printf "Admin addr id is %s\n" $admin_addr
addr=$(printf $password |$seid tx wasm instantiate $code '{"count": 0}' --home $home --from $keyname --broadcast-mode=block --label "data-oracle" --node https://rpc.atlantic-2.seinetwork.io/ --chain-id atlantic-2 --gas=30000000 --fees=300000usei --admin=$admin_addr -y | grep -A 1 -m 1 "key: _contract_address" | sed -n 's/.*value: //p' | xargs)
printf "Deployed counter address is %s\n" $addr


seid tx wasm store /data-01/data_oracle.wasm -y --from=test --home /data-01/sei-data --chain-id=atlantic-2 --node https://rpc.atlantic-2.seinetwork.io/ --gas=10000000 --fees=100000usei --broadcast-mode=block

seid tx wasm instantiate 13 '{}' --home /data-01/sei-data --chain-id atlantic-2 --node https://rpc.atlantic-2.seinetwork.io/ --from test --gas=4000000 --fees=1000000usei --broadcast-mode=block --label data-oracle --no-admin