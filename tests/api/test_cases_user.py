# ({payload}, "test id")
USERS_REGISTRATION = [
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Default valid user",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "`!@#$%^&*()_+'\"№;:?-=[]/\\あいうえお",
        },
        "Password with special characters",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1111111",
        },
        "Password with minimum length 7",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        },
        "Password with maximum length 100",
    ),
]

# ({payload}, "test id")
USERS_REGISTRATION_INVALID = [
    (
        {
            "firstName": "",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Empty firstName",
    ),
    (
        {
            "firstName": "John",
            "lastName": "",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Empty lastName",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "",
            "password": "1234567890",
        },
        "Empty email",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "",
        },
        "Empty password",
    ),
    (
        {
            "firstName": "",
            "lastName": "",
            "email": "",
            "password": "",
        },
        "Empty each field",
    ),
    (
        {
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Missing field firstName",
    ),
    (
        {
            "firstName": "John",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Missing field lastName",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "password": "1234567890",
        },
        "Missing field email",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
        },
        "Missing field password",
    ),
    (
        {

        },
        "No fields",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "111111",
        },
        "Password less than 7 characters (6 in test)",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        },
        "Password longer than 100 characters (101 in test)",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.greenmail.com",
            "password": "1234567890",
        },
        "Email without @",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "@mail.com",
            "password": "1234567890",
        },
        "Email without user",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@",
            "password": "1234567890",
        },
        "Email without domain",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john green@mail.com",
            "password": "1234567890",
        },
        "Email with space",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail",
            "password": "1234567890",
        },
        "Email with invalid domain",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "jo#n.green@mail.com",
            "password": "1234567890",
        },
        "Email with invalid characters",
    ),
    (
        {
            "_id": "111111111111111111111111",
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "User with custom _id field",
    ),
]

# ({payload}, {expected}, "test id")
USERS_PATCHED = [
    (
        {
            "firstName": "John_updated",
            "lastName": "Green_updated",
            "email": "john.green_updated@mail.com",
            "password": "1234567890_updated",
        },
        {
            "firstName": "John_updated",
            "lastName": "Green_updated",
            "email": "john.green_updated@mail.com",
            "password": "1234567890_updated",
        },
        "Each field updated",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "No fields updated",
    ),
    (
        {

        },
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Empty body",
    ),
]

# ({payload}, "test id")
USERS_PATCHED_INVALID = [
    (
        {
            "firstName": "",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Empty firstName",
    ),
    (
        {
            "firstName": "John",
            "lastName": "",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Empty lastName",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "",
            "password": "1234567890",
        },
        "Empty email",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "",
        },
        "Empty password",
    ),
    (
        {
            "firstName": "",
            "lastName": "",
            "email": "",
            "password": "",
        },
        "Empty each field",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "111111",
        },
        "Too short password (length = 6)",
    ),
    (
        {
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        },
        "Too long password",
    ),
    (
        {
            "_id": "111111111111111111111111",
            "firstName": "John",
            "lastName": "Green",
            "email": "john.green@mail.com",
            "password": "1234567890",
        },
        "Change _id",
    ),
]
