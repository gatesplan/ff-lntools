use super::Parser;

#[test]
fn strict_rejects_negative() {
    assert!(Parser::strict().parse("1,-2").is_err());
    assert_eq!(Parser::default().parse("1, 2").unwrap().len(), 2);
    assert_eq!(Parser::evens(&[1, 2, 4]).count(), 2);
}
