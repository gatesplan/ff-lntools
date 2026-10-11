use crate::l0::money::Money;
use crate::l1::kit_error::KitError;

/// 쉼표로 나눈 금액 목록을 읽는다
#[derive(Debug, Default)]
pub struct Parser {
    strict: bool,
}

impl Parser {
    pub fn strict() -> Self {
        Self { strict: true }
    }

    pub fn parse(&self, text: &str) -> Result<Vec<Money>, KitError> {
        let Some(first) = text.split(',').next() else {
            return Err(KitError::Empty);
        };
        if first.trim().is_empty() {
            return Err(KitError::Empty);
        }
        let out: Vec<Money> = text
            .split(',')
            .filter_map(|s| s.trim().parse::<i64>().ok())
            .map(Money::won)
            .collect();
        if self.strict
            && let Some(bad) = out.iter().find(|m| m.0 < 0)
        {
            return Err(KitError::Negative(*bad));
        }
        Ok(out)
    }

    pub fn evens(values: &[i64]) -> impl Iterator<Item = i64> + '_ {
        values.iter().copied().filter(|v| matches!(v % 2, 0))
    }

    pub async fn parse_later(&self, text: String) -> Result<Vec<Money>, KitError> {
        self.parse(&text)
    }
}
