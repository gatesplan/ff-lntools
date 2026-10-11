use crate::l0::Money;

#[derive(Debug, thiserror::Error)]
pub enum KitError {
    #[error("음수 금액: {0}")]
    Negative(Money),
    #[error("빈 입력")]
    Empty,
}
