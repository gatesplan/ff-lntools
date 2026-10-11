use std::fmt;
use std::ops::Add;

/// 금액. 정수 원 단위
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Money(pub i64);

impl Money {
    pub const ZERO: Money = Money(0);

    #[must_use]
    pub fn won(v: i64) -> Self {
        Self(v)
    }
}

impl Add for Money {
    type Output = Money;
    fn add(self, rhs: Money) -> Money {
        Money(self.0 + rhs.0)
    }
}

impl fmt::Display for Money {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}원", self.0)
    }
}

impl<T: Into<i64>> From<(T,)> for Money {
    fn from(v: (T,)) -> Self {
        Money(v.0.into())
    }
}
