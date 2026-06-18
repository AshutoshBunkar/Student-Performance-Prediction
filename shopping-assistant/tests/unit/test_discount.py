from app.agent import redeem_discount, DISCOUNT_STORE

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
