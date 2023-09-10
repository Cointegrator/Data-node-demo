use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use cw_storage_plus::{UniqueIndex, IndexList, Index, IndexedMap, MultiIndex};

const INDICATOR_NAMESPACE: &str = "indicators";

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, Eq, JsonSchema)]
pub struct Indicator {
    pub token: String,
    pub indicator: String,
    pub timestamp: u64,
    pub data: String,
}

pub struct IndicatorIndexes<'a> {
    pub indicator: UniqueIndex<'a, (String, String, u64), Indicator>,
    pub token: MultiIndex<'a, (String, String), Indicator, (String, String, u64)>,
}
  
impl<'a> IndexList<Indicator> for IndicatorIndexes<'a> {
    fn get_indexes(&'_ self) -> Box<dyn Iterator<Item = &'_ dyn Index<Indicator>> + '_> {
      let v: Vec<&dyn Index<Indicator>> = vec![&self.indicator, &self.token];
      Box::new(v.into_iter())
    }
}
  
pub fn indicators<'a>() -> IndexedMap<'a, &'a (String, String, u64), Indicator, IndicatorIndexes<'a>> {
    let indexes = IndicatorIndexes {
        indicator: UniqueIndex::new(
            |d: &Indicator| (d.token.clone(), d.indicator.clone(), d.timestamp),
            INDICATOR_NAMESPACE,
        ),
        token: MultiIndex::new(
            |_, d: &Indicator| (d.token.clone(), d.indicator.clone()),
            INDICATOR_NAMESPACE,
            "indicators_by_token"
        ),
    };
    IndexedMap::new(INDICATOR_NAMESPACE, indexes)
}