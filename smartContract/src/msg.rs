use cosmwasm_schema::{cw_serde, QueryResponses};

use crate::state::Indicator;

#[cw_serde]
pub struct InstantiateMsg {}

#[cw_serde]
pub enum ExecuteMsg {
    Push {data: Indicator}
}

#[cw_serde]
#[derive(QueryResponses)]
pub enum QueryMsg {
    #[returns(QueryDataResponse)]
    Query {token: String, indicator: String},
}

#[cw_serde]
pub struct QueryDataResponse {
    pub data: Vec<Indicator>,
}