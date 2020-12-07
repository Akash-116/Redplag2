import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, FormControlName } from '@angular/forms';
import { AuthService } from '../shared/services/auth.service';
@Component({
  selector: 'app-register-component',
  templateUrl: './register-component.component.html',
  styleUrls: ['./register-component.component.scss']
})
export class RegisterComponentComponent implements OnInit {

  form:FormGroup;  

  constructor(private authserv:AuthService) { }

  ngOnInit(): void {
    this.form=new FormGroup({
      firstname:new FormControl,
      lastname:new FormControl,
      email:new FormControl,
      phone:new FormControl,
      password1:new FormControl,
      password2:new FormControl
    });
  }

  register():void {
    if(this.form.value.password1!==this.form.value.password2){
      window.alert("Password doesn't match");
      return;
    }
    this.authserv.register(this.form.value);
  }


}
