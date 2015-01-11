```* here means login required```

#### User_Handler

    Create a new user or update a user info

```
All fields no longer than 30 characters except email is 50.

Model Fields:

    UserID         = str        Indexed
    FirstName      = str
    LastName       = str
    Birthday       = str    =>  unix timestamp
    Email          = str        Indexed
    Password       = str
    Phone          = str
    School         = str        Indexed
    Major          = str        Indexed
    Gender         = str   male/female  Indexed
    Signature      = str
    Driver         = str   yes/no    Indexed
    EmailActive    = bool
    PhoneActive    = bool
    AccountActive  = bool
    DriverLicense  = str   
    CarID          = str        None
    PhotoID        = str        None

```

> post : /api/v1/user/create

```
    PAYLOAD:

        {
            "email"     : "address must end with .edu",
            "firstname" : "first name",
            "lastname"  : "last name",
            "password"  : "a serious password"
        }

```

> put* : /api/v1/user/update

```
    PAYLOAD:
        
        {
            "firstname" : "first name",
            "lastname"  : "last name",
            "gender"    : "man/woman",
            "college"   : "school name",
            "major"     : "a serious major",
            "birthday"  : "an unix timestamp",
            "password"  : "a new password",
            "phone"     : "a XXX-XXX-XXXX style phone number",
            "signature" : "about user himself",
            "driver"    : "yes/no",
            "license"   : "last 4 digits of driver license"
        }

```

> get* : /api/v1/user/get   - get current user info

> get* : /api/v1/user/get/'a serious user id'   - get some user info

```
    Output Fields:
            FirstName,
            LastName,
            Birthday,
            Email,
            Phone,
            School,
            Major,
            Gender,
            Signature,
            Driver,
            DriverLicense,
            CarID,
            PhotoID
```





