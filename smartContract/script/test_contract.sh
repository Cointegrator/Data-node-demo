seid=~/go/bin/seid
contract='sei1zllzycrxwr5ts0yyrtnzakweyt2veeat837vfm4szxugsjv80nyqj7ejyr' # Fill in contract address from deployment step, ex. sei14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9sh9m79m

seid tx wasm execute sei1xrg7cgku9xmazcx2syrasf5eukjqx4r20wf6vfg9ulp3uahlvx9q9f4ltv '{"push":{"data": {"token": "testtoken123456", "indicator": "price", "timestamp": 1, "data": "100"}}}' --home /data-01/sei-data --from test --broadcast-mode=block  --chain-id=atlantic-2 --node https://rpc.atlantic-2.seinetwork.io/ --gas=10000000 --fees=3000000usei -y

seid q wasm contract-state smart sei1zllzycrxwr5ts0yyrtnzakweyt2veeat837vfm4szxugsjv80nyqj7ejyr '{"query":{"token": "testtoken123456", "indicator": "price"}}' --home /data-01/sei-data --chain-id=atlantic-2 --node https://rpc.atlantic-2.seinetwork.io/
