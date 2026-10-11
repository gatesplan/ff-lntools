use kit_core::App;

#[test]
fn runs() {
    let out = App::run("1, 2").unwrap();
    assert!(out.contains("money: 3원"), "{out}");
    assert!(App::run("-1").is_err());
}
