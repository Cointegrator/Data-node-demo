import { getCosmWasmClient, getSigningCosmWasmClient, restoreWallet} from "@sei-js/core";
import { GasPrice, calculateFee } from '@cosmjs/stargate'

const contract_address = 'sei1xrg7cgku9xmazcx2syrasf5eukjqx4r20wf6vfg9ulp3uahlvx9q9f4ltv'
const rpc_url = 'https://rpc.atlantic-2.seinetwork.io/'
const address = 'sei1sjhuh3ekhlx770280vhfkzt9pmpmpnzn26jhcm'
const SEED_PHRASE = 'attack update worth divide chronic tomato aware demise version glide myth explain'

export const query_data = async (token_address: string, indicator: string) => {
    const cosmWasmClient = await getCosmWasmClient(rpc_url);
    const query_msg = { query: {token: token_address, indicator: indicator }}
    return await cosmWasmClient.queryContractSmart(contract_address, query_msg)
}

export const upload_data = async (token_address: string, indicator: string, timestamp: number, data: string) => {
    const wallet = await restoreWallet(SEED_PHRASE)
    const fee = calculateFee(300000, '0.1usei');
    const signingCosmWasmClient = await getSigningCosmWasmClient(rpc_url, wallet);

    const msg = { push : {
            data: {
            token: token_address,
            indicator: indicator,
            timestamp: timestamp,
            data: data
        } 
    } };

    return await signingCosmWasmClient.execute(address, contract_address, msg, fee);
}