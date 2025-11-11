*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Register Username  matt
    Set Register Password  password1
    Set Register Password Confirmation  password1
    Click Button  Register
    Registration Should Succeed

Register With Too Short Username And Valid Password
    Set Register Username  ma
    Set Register Password  password1
    Set Register Password Confirmation  password1
    Click Button  Register
    Registration Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Register Username  matt
    Set Register Password  pass
    Set Register Password Confirmation  pass
    Click Button  Register
    Registration Should Fail With Message  Password must be at least 8 characters long

Register With Valid Username And Invalid Password
    Set Register Username  matt
    Set Register Password  password
    Set Register Password Confirmation  password
    Click Button  Register
    Registration Should Fail With Message  Password must contain characters other than letters

Register With Nonmatching Password And Password Confirmation
    Set Register Username  matt
    Set Register Password  password1
    Set Register Password Confirmation  password2
    Click Button  Register
    Registration Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Create User  kalle  kalle123
    Set Register Username  kalle
    Set Register Password  kalle123
    Set Register Password Confirmation  kalle123
    Click Button  Register
    Registration Should Fail With Message  Username already exists

*** Keywords ***

Registration Should Succeed
    Page Should Contain  Welcome

Registration Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Register Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Register Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Register Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Reset Application And Go To Register Page
    Reset Application
    Go To  ${REGISTER_URL}
