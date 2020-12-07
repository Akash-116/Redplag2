# RedPlagProject

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 10.1.3.

# What we have implemented so far

* Signup and Login Pages
* User Authentication and strictly no access for unauthorized user
* User Home page
* Change Password (in Home Page) and Forgot password (in Login Page) options
* Upload and Download options

# Implementation details

* We have used **Angular** for the frontend.
* For the authentication part we used **Firebase** and were successful in
  * Restricting access for non-authenticated users.
  * Sending Email verifications to activate account and link to change password.
  * Storing all the user data in our firebase account.
* For **Upload** and **Download** we have used **Django REST API** framework and **Python** as backend and
  * When a zip file is uploaded, it is stored in the **media** folder. Now the zip file is unzipped and sent to the **unzipped** folder in the same directory.
  * For now we are just giving out the same zip file uploaded when the download button is clicked, we will change this later when our part-1 implementation is also done.

# Instructions for the User (How to use)

## Login Page

* This is the first page which appears on running the App.
* If you already have an account, you can login using your EmailID and password
  * If the EmailID or password doesn't match with that in the database you get an **error** with approppriate message.
  * If the login credentials are correct you will be redirected to the **Home Page**.
  * You can click on **forgot password** if you don't remember your password, this will take you to the **Forgot page** where you can type your EmailId and a link to change your password will be sent to that EmailId. Click on the link and change your password.
* If you don't have an account and want to create one, click on **Don't have an account?**. This will take you to the **Register Page**.

## Register Page

* Fill in all the details.
* The EmailID should be of the form aaa@aaa.aaa, and the password must be atleast 6 characters. Click on **Register** button once you are done.
* An **activation mail** will be sent to that EmailId, click on the activation link to activate your account. Please note that you cannot login without activating your account.

## Home Page

* **Upload**
  * Upload a zip of all the files you want to check for plagiarism.
* **Download**
  * Download the results of our plagiarism checker.
* Click on the **Logout** button once you are done.
* Click on **Change Password** to change your password.

# Yet to be done
* **Part-2**
  * Upgrade Authentication part implementing Django RESTapi, as we have observed that firebase is taking more time for the login part.
  * Add a new feature to create an organization and use organization code to login or signup.
  * Make some minor changes in the upload and download part to make it more user-friendly.
* **Part-3**
  * Implement part-1 on the zip-file uploaded by the user, and provide download access to the final output of part-1. (Currently, the same zip file is returned for downloading)
   * Implement a new app to authorize user login/signup requests from the frontend. (Google Firebase is our current choice)
