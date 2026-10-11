use shop::App;

#[test]
fn momentum_follows_closes() {
    assert_eq!(App::run(&[1, 2, 3, 2]), 1);
}
