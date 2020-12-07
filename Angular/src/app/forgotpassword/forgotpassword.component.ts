import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { AuthService } from '../shared/services/auth.service';

@Component({
  selector: 'app-forgotpassword',
  templateUrl: './forgotpassword.component.html',
  styleUrls: ['./forgotpassword.component.scss']
})
export class ForgotpasswordComponent implements OnInit {

  form:FormGroup;

  constructor(private authserv:AuthService) { }

  ngOnInit(): void {
    this.form=new FormGroup({
      email:new FormControl
    });
  }

  forgotPassword():void{
    this.authserv.forgotPassword(this.form.value.email);
  }

}
