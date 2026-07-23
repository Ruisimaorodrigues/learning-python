def check_membership(member, status):
    if status == "cancelled":
        print(member + " has cancelled their membership")
    else:
        print(member + " is active")

check_membership("Alice", "active")
check_membership("Bob", "cancelled")
check_membership("Carlos", "active")