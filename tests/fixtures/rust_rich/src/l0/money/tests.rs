use super::Money;

#[test]
fn adds() {
    assert_eq!(Money::won(1) + Money::won(2), Money(3));
    assert_eq!(Money::from((5_i32,)).to_string(), "5원");
}
