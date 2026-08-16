from library_system.member import Member


def test_member_attributes():
    member = Member("M001", "John Doe", "john@example.com")
    assert member.member_id == "M001"
    assert member.name == "John Doe"
    assert member.email == "john@example.com"
