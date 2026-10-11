/// 넓이를 가진 것
pub trait Shape: std::fmt::Debug {
    type Unit;
    fn area(&self) -> Self::Unit;
    fn scaled<K: Into<f64>>(&self, k: K) -> f64
    where
        Self: Sized,
        Self::Unit: Into<f64> + Copy,
    {
        self.area().into() * k.into()
    }
}
