
def test_load_prompt():
    from app.services.prompt_loader import load_prompt
    prompt = load_prompt("default", "infer")
    assert "recommendation" in prompt
