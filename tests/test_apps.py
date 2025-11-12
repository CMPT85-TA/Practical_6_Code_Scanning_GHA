import pytest
import vuln_app
import secure_app


def test_use_insecure_hash():
    assert vuln_app.use_insecure_hash("a") == "0cc175b9c0f1b6a831c399e269772661"


def test_use_secure_hash():
    assert secure_app.use_secure_hash("a") == "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"


def test_safe_eval_ok():
    assert secure_app.safe_eval("[1, 2, 3]") == [1, 2, 3]


def test_safe_eval_bad():
    with pytest.raises(ValueError):
        secure_app.safe_eval("__import__('os').system('echo hi')")
