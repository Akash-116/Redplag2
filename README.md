# Project RedPlag

# Meet our Team
| Name | Roll Number | Contribution |
| :----: | :-----------: | -------------|
| **A**kash Reddy | 190050038 | WebPage Styling, Integrating part-1 logic in backend, Upload and Download implementation for Frontend and Backend. API endpoints documentation |
| **C**handrasekhar | 190050031 | Setting up REST-API framework for Django Backend, Firebase framework for Angular Frontend, Implemented login page (both frontend and backend), Implemented all the Guards and Serivces in Angular Frontend |
| **V**ishwanth | 190050131 | Visualisation for results. Implemented the stub-code feature |
| **K**arthikeya | 190050026 | Plagiarism core-logic implementation and documentation using doxygen |

# What we have implemented so far :

* Signup and Login Pages
* User Authentication and strictly no access for unauthorized user
* User Home page
* Change Password option in Home page and Forgot Password option in Login page
* Gave user options to select which type of files he wants to upload
* Option to upload Stub code is also given to the user
* Upload files and Download results facility is provided
* Core Logic (Similarity between files) 
  * Made some improvements on bag of words strategy for C++ files (Language Specific functionality)
  * If a stub code file is provided by user then the influence of stub code has been removed from the files
  
# Implementation details (Needs to be updated)

* We have used **Angular** for the frontend.
* For the authentication part we used **Firebase** and were successful in
  * Restricting access for non-authenticated users.
  * Sending Email verifications to activate account and also in case of change-password request.
  * Storing the user data in our google-firebase account.
  * The token details are stored in the local storage of the browser, rather than the frontend, maintaing privacy of the user.  
* For **Upload** and **Download** functionality, we've used **Django REST-API** framework and **Python** as backend and
  * When a zip-file is uploaded, it's constituents are stored in the **unzipped** folder. Instead, if a stub-code file is uploaded, it is placed in the **stubcode** directory.
  * The processing of the files, begin as soon as the zip-file is uploaded (The user is given choice (on the website) as to how to process the files, whether text or cpp, whether with stub or without). The results of the Plagiarism checking, are then stored in the **rpoutput** directory.
  * A visualisation image is sent to the front end, which displays it on the website, as soon as the user uploads the zip-file.
  * A download button is enabled, which then downloads the appropriate file (either a .png or a .csv file) from the backend. 
* For Core part we have used **Bag of Words** strategy to get the signature vector for each file and used the **Normalized distance** as the metric to compute the similarity between two vectors. For more details look at the Documentation.

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

* **Options**
  * Choose which type of file you want to upload (For now the options given are C++ and text, so select text if you want to select any language other than C++).
  * Choose the approppriate option if you want to upload stub code.
* **Upload**
  * If you have selected stub code option, only then you will be given an option to upload stub code file.
  * Upload a **zip** of all the files you want to check for plagiarism. Please ensure that this zip file does not have any directory inside it.
  * If the uploading of zip was successful then you can see the results of our plagiarism checker.
* **Download**
  * Download the results of our plagiarism checker.
  * Seperate options have been given to download the image or the CSV file. The CSV file contains a table of file names and Plagiarism percentage.
* **Reset**
  * After you have downloaded results, click on reset to upload new set of files.
* Click on the **Logout** button once you are done.
* Click on **Change Password** to change your password.

# Improvements that can be done
* **Part-1**
  * Improve our core logic by handling macros and some other ways of plagiarism in C++.
  * Implement language specific functionality for other common languages like Python, Java etc.
  * Use a better metric to find similarity between files using the signature vectors.
  * Read about other strategies to detect plagiarism and try to improve our core logic.
* **Part-2**
  * Add a new feature to create an organization and use organization code to login or signup.
  * Make some changes in styling to make it more attractive. 
