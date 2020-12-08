# Project RedPlag

# Meet the Team :
| Name | Roll Number | Contribution |
| :----: | :-----------: | -------------|
| **A**kash Reddy G. | 190050038 | Webpage styling (SCSS), integrating core-logic into backend, upload and download implementations (both frontend and backend). API-endpoint documentation. |
| **C**handrasekhara S.S.H.H. | 190050031 | Setting up REST-API framework for django-backend, google firebase framework for angular-frontend, implemented login page(both frontend and backend), implemented **all** the components, guards and serivces in angular-frontend. |
| **V**ishwanth K. | 190050131 | Visualisation for results obtained from processing the files, implemented the stub-code feature. |
| **K**arthikeya B. | 190050026 | Implemented plagiarism core-logic, documented the core-logic using doxygen |

  
# Implementation details :

* We've used **Angular** for the frontend, implementing:
  * Components like login-component, register-component, home, logout, emailverification etc.
  * Guards such as AuthGuard, EmailGuard, LoginGuard.
  * Services such as DownloadService, UploadService, AuthService.
  * Options for user to register an account, change password, recover password, logout.
  * Options to select the input nature, upload files, download results and more. 
  
* For the authentication part **Google Firebase** is used and we've successfully implemented:
  * Restricting access for non-authenticated users.
  * Sending email verifications to activate account and also in case of change-password/ forgot-password requests.
  * Storing the JWtokens in the local storage of the browser.  
  
* For **Upload** and **Download** functionality, we've used **REST-API framework** from django as backend. Also:
  * When a zip-file is uploaded, it's constituents are stored in the **unzipped** folder. Instead, if a stub-code file is uploaded, it is placed in the **stubcode** directory.
  * The processing of the files, begin as soon as the zip-file is uploaded (The user is given choice (on the website) as to how to process the files, whether text or cpp, whether with stub or without). The results of the Plagiarism checking, are then stored in the **rpoutput** directory.
  * A visualisation image is sent to the frontend, which displays it on the website, as soon as the user uploads the zip-file.
  * A download button is enabled, which then downloads the appropriate file (either a .png or a .csv file) from the backend.
  * API-endpoints documentation is avaliable at Documentation/API_Endpoints/ directory.
  
* For **core-logic** we've taken inspiration from **Bag of Words** strategy to obtain the signature vector for each file, and used the **Normalized distance** as a metric to compute the similarity between two such vectors. 
  * Made some improvements on bag of words strategy for C++ files (Language Specific functionality)
  * If a stub code file is provided by user, then the influence of stub code has been removed from the files.
  * Refer to Documentation/CorePart/html/index.html for more details regarding implementation.

# How to Use :

### Login Page

* This is the first page which appears on running the app.
* New users can use the **Don't have an account?** option to register their account.
* Users can login using thier emailid and password :
  * If the login credentials are correct, user will be redirected to the **Home Page**.
  * If the emailid or the password doesn't match with that in records, he/she'll get an **error alert**  with an approppriate message.
  * User can use the **forgot password** option, if he/she don't remember their password. This will take them to the **Forgot page** page, where he/she can give their emailid to recieve a link to change their password, via email.

### Register Page

* Fill in the required details.
* The EmailID should be of the form aaa@aaa.aaa, and the password must be atleast 6 characters. Click on **Register** button once you are done.
* An **Confirm-Activation mail** will be sent via email; click on the link to confirm activation. Note that one cannot login without confirming activation of their account.

### Home Page

* **Options**
  * Choose which type of file you plan to upload (For now, the options avaliable are C++ and text, so select text if you want to select any language other than C++).
  * Again, choose the approppriate option - whether you have a stub-code or not.
* **Upload**
  * If you've selected stub code option, only then will you be able to upload the stub code file.
  * Upload a **zip** of all the files you want to check for plagiarism. Please ensure that this zip file **does not have any directory** inside it. (i.e. the zip should have the files, immediately inside it.)
  * If the uploading of zip was successful, then you can immediately see the results of the plagiarism checker.
* **Download**
  * Download the results of the plagiarism checker using the buttons provided (these are disabled initially, but are enabled once you've successfully uploaded a zip file).
  * Seperate options have been given to download the image or the CSV file. The CSV file contains a table of file names and Plagiarism percentage.
* **Reset**
  * Use this option, if at any point of uploading the files, you need to reset the process.
* Click on the **Logout** button once you are done.
* Click on **Change Password** to change your password.

# Possible Improvements :
* **Part-1**
  * Improve core-logic for C++ file handling, by handling macros and other such ways of plagiarism specific to C++.
  * Implement language specific functionality for other common languages like Python, Java etc.
  * Implement an even better metric to compute similarity between files using the signature vectors.
  * Implement even better strategies to compute plagiarism, taking the position of words into account, etc.
* **Part-2,3**
  * Add a feature to create an organization and use organization code to login or signup.
  * Improve the styling of the webpage, introduce animations and stronger css concepts. 
