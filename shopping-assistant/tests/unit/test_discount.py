from app.agent import DISCOUNT_STORE, redeem_discount, update_discount_status


def test_redeem_discount_success():
    # Reset DISCOUNT_STORE state for the test
    DISCOUNT_STORE["WELCOME50"] = False

    # Registered user account, valid not-redeemed code
    result = redeem_discount("WELCOME50", "user_123")
    assert "Success" in result
    assert DISCOUNT_STORE["WELCOME50"] is True


def test_redeem_discount_already_redeemed():
    # Set to already redeemed
    DISCOUNT_STORE["WELCOME50"] = True

    result = redeem_discount("WELCOME50", "user_123")
    assert "already been redeemed" in result


def test_redeem_discount_guest_user():
    # Reset DISCOUNT_STORE state for the test
    DISCOUNT_STORE["WELCOME50"] = False

    # guest_ prefixed user_id is blocked
    result = redeem_discount("WELCOME50", "guest_123")
    assert "Registered user account required" in result


def test_redeem_discount_empty_user():
    # Reset DISCOUNT_STORE state for the test
    DISCOUNT_STORE["WELCOME50"] = False

    result = redeem_discount("WELCOME50", "")
    assert "Registered user account required" in result


def test_redeem_discount_invalid_code():
    result = redeem_discount("INVALID99", "user_123")
    assert "Invalid discount code" in result


def test_update_discount_status_activate():
    # Set to already redeemed (meaning active=False, i.e. True in DISCOUNT_STORE)
    DISCOUNT_STORE["WELCOME50"] = True

    result = update_discount_status("WELCOME50", active=True, admin_id="admin_123")
    assert "activated" in result
    assert DISCOUNT_STORE["WELCOME50"] is False


def test_update_discount_status_deactivate():
    # Set to active (meaning active=True, i.e. False in DISCOUNT_STORE)
    DISCOUNT_STORE["WELCOME50"] = False

    result = update_discount_status("WELCOME50", active=False, admin_id="admin_123")
    assert "deactivated" in result
    assert DISCOUNT_STORE["WELCOME50"] is True


def test_update_discount_status_invalid_code():
    result = update_discount_status("INVALID99", active=True, admin_id="admin_123")
    assert "Invalid discount code" in result


def test_update_discount_status_unauthorized_guest():
    result = update_discount_status("WELCOME50", active=True, admin_id="guest_admin")
    assert "Administrator account required" in result


def test_update_discount_status_unauthorized_user():
    result = update_discount_status("WELCOME50", active=True, admin_id="user_123")
    assert "Administrator account required" in result
