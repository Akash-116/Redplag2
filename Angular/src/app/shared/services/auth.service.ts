import { Injectable, NgZone } from '@angular/core';
import { User } from './user';
import { auth } from 'firebase/app';
import { AngularFireAuth } from '@angular/fire/auth';
import { AngularFirestore, AngularFirestoreDocument } from '@angular/fire/firestore'; 
import { Router } from '@angular/router';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  userData:any;
  constructor(
    private afs: AngularFirestore,
    private afAuth: AngularFireAuth,
    private router: Router,
    private ngZone: NgZone
    ){
      this.afAuth.authState.subscribe(
        user=>{
          if(user) {
            this.userData=user;
            localStorage.setItem('user',JSON.stringify(this.userData));
            JSON.parse(localStorage.getItem('user')); //see what this does
          }else{
            localStorage.setItem('user',null);
            JSON.parse(localStorage.getItem('user'));
          }
        }
      )
    }
  
  login(email:any,password:any){
    return this.afAuth.signInWithEmailAndPassword(email,password).then(
      (result)=>{
        this.ngZone.run(()=>this.router.navigate(['home']));
        this.SetUserData(result.user);
      }).catch((error)=>{window.alert(error.message)});
  }

  SetUserData(user) {
    const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${user.uid}`);
    const userData: User = {
      email:user.email,
      displayName:user.displayName,
      uid:user.uid,
      photoURL:user.photoURL,
      emailVerified:user.emailVerified

    }
    return userRef.set(userData,{merge:true});
  }

  register(userdetails):void{
    this.afAuth.createUserWithEmailAndPassword(userdetails.email,userdetails.password1).then(
      result=>{
        this.send_verification_email();
        this.SetUserData(result.user);
        // this.send_verification_email();
      }
      ).catch((error)=>window.alert(error.message));
    }
    
    send_verification_email():void{ 
      auth().currentUser.sendEmailVerification().then(
        ()=>this.router.navigate(['email-verification']))

  }
  
  get is_logged():boolean{
    const user=JSON.parse(localStorage.getItem('user'));
    if(user!==null && user.emailVerified===true){return true;}
    return false;
  }

  // get username():string{
  //   const user=JSON.parse(localStorage.getItem('user'));
  //   console.log(user);
  //   return "dummy";

  // }

  get user_not_null():boolean{
    const user=JSON.parse(localStorage.getItem('user'));
    return user===null;
  }

  // ProfileChangeRequest(displayname):void{
    
  // }


  logout():void{
    this.afAuth.signOut().then(()=>{
      localStorage.removeItem('user');
      this.router.navigate(['login']);
    })
  }

  forgotPassword(passwordemail){
    // const user=JSON.parse(localStorage.getItem('user'));
    // console.log(user) //to be removed
    this.afAuth.sendPasswordResetEmail(passwordemail).then(
      ()=>{
        window.alert('Password reset email sent to your registered email.Check your Inbox and spam folder as well');
        this.router.navigate(['/login']);
      }
    ).catch((error)=>window.alert(error));
  }
  
  
}
