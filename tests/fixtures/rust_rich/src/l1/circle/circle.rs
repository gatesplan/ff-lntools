use crate::l0::shape::Shape;

#[derive(Debug, Clone, Copy)]
#[cfg_attr(feature = "serde", derive(serde::Serialize))]
pub struct Circle {
    pub r: f64,
}

impl Shape for Circle {
    type Unit = f64;
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.r * self.r
    }
}
