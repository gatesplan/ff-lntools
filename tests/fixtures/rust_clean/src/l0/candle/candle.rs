pub struct Candle {
    pub close: u32,
}

impl Candle {
    pub fn new(close: u32) -> Self {
        Self { close }
    }
}
