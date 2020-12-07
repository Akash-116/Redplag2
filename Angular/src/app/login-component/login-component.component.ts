import { Component, OnInit } from '@angular/core';
import { FormGroup,FormControlName, FormControl } from '@angular/forms'
import { AuthService } from '../shared/services/auth.service';
@Component({
  selector: 'app-login-component',
  templateUrl: './login-component.component.html',
  styleUrls: ['./login-component.component.scss']
})
export class LoginComponentComponent implements OnInit {
  form:FormGroup;
  constructor(private authserv:AuthService) { }

  ngOnInit(): void {
    this.form = new FormGroup({
      email:new FormControl,
      password:new FormControl
    });
  }

  login():void{
    // console.log(this.form);
    this.authserv.login(this.form.value.email,this.form.value.password);
  }


}
