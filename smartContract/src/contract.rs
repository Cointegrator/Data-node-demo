#[cfg(not(feature = "library"))]
use cosmwasm_std::entry_point;
use cosmwasm_std::{to_binary, Binary, Deps, DepsMut, Env, MessageInfo, Response, StdResult};
use cw2::set_contract_version;

use crate::error::ContractError;
use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg, QueryDataResponse};
use crate::state::{indicators, Indicator};

// version info for migration info
const CONTRACT_NAME: &str = "crates.io:data-oracle";
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    _: InstantiateMsg,
) -> Result<Response, ContractError> {
    set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;

    Ok(Response::new()
        .add_attribute("method", "instantiate")
        .add_attribute("owner", info.sender)
    )
}

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    _: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response, ContractError> {
    match msg { 
        ExecuteMsg::Push {data} => execute::push(deps, data),
    }
}

pub mod execute {
    use super::*;

    pub fn push(deps: DepsMut, data: Indicator) -> Result<Response, ContractError> {
        indicators().save(deps.storage, &(data.token.clone(), data.indicator.clone(), data.timestamp), &data)?;
        Ok(Response::new())
    }
}

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    match msg {
        QueryMsg::Query {token, indicator} => to_binary(&query::query(deps, token, indicator)?),
    }
}

pub mod query {
    use cosmwasm_std::Order;

    use super::*;

    pub fn query(deps: Deps, token: String, indicator: String) -> StdResult<QueryDataResponse> {
        let res: Vec<_> = indicators()
        .idx
        .token
        .prefix((token, indicator))
        .range(deps.storage, None, None, Order::Ascending)
        .map(|item: Result<((String, String, u64), Indicator), cosmwasm_std::StdError>| {
            let (_, data) = item.unwrap();
            return data;
        })
        .collect();
        Ok(QueryDataResponse { data: res })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use cosmwasm_std::testing::{mock_dependencies, mock_env, mock_info};
    use cosmwasm_std::{coins, from_binary};

    #[test]
    fn proper_initialization() {
        let mut deps = mock_dependencies();

        let msg = InstantiateMsg {};
        let info: MessageInfo = mock_info("creator", &coins(1000, "earth"));

        // we can just call .unwrap() to assert this was a success
        let res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();
        assert_eq!(0, res.messages.len());

        // it worked, let's query the state
        let res = query(deps.as_ref(), mock_env(), QueryMsg::Query { token: String::from("sender0001"), indicator: "volume".to_string() }).unwrap();
        let value: QueryDataResponse = from_binary(&res).unwrap();
        assert_eq!(0, value.data.len());
    }

    #[test]
    fn increment() {
        let mut deps = mock_dependencies();

        let msg = InstantiateMsg {};
        let info = mock_info("creator", &coins(2, "token"));
        let _res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();

        // beneficiary can release it
        let info = mock_info("anyone", &coins(2, "token"));
        let msg = ExecuteMsg::Push { data: Indicator {
            token: String::from("sender0001"), indicator: "volume".to_string(), timestamp: 1, data: String::from("100")
        } };
        let _res = execute(deps.as_mut(), mock_env(), info, msg).unwrap();

        // beneficiary can release it
        let info = mock_info("anyone", &coins(2, "token"));
        let msg = ExecuteMsg::Push { data: Indicator {
            token: String::from("sender0001"), indicator: "price".to_string(), timestamp: 1, data: String::from("100")
        } };
        let _res = execute(deps.as_mut(), mock_env(), info, msg).unwrap();
        
        // beneficiary can release it
        let info = mock_info("anyone", &coins(2, "token"));
        let msg = ExecuteMsg::Push { data: Indicator {
            token: String::from("sender0001"), indicator: "price".to_string(), timestamp: 2, data: String::from("200")
        } };
        let _res = execute(deps.as_mut(), mock_env(), info, msg).unwrap();

        // should increase counter by 1
        let res = query(deps.as_ref(), mock_env(), QueryMsg::Query { token: String::from("sender0001"), indicator: "price".to_string() }).unwrap();
        let value: QueryDataResponse = from_binary(&res).unwrap();
        assert_eq!(2, value.data.len());

        let data = value.data.get(1).unwrap();
        assert_eq!("200", data.data);
    }
}
