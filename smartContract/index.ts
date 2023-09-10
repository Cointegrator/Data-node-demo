import 'node-self'
import { query_data, upload_data } from "./contract"

const test = async () => {

    const token_address = 'testtoken123456'
    const indicator = 'price'

    const timestamp = Math.floor(Date.now() / 1000)
    const data = '100'

    const result = await query_data(token_address, indicator)
    console.log(result)

    const result2 = await upload_data(token_address, indicator, timestamp, data)
    console.log(result2)
}

test().catch(console.error)