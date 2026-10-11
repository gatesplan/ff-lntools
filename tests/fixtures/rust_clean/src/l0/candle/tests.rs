use super::Candle;

#[test]
fn keeps_close() {
    assert_eq!(Candle::new(3).close, 3);
}
