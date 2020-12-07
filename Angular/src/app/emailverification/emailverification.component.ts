import { Component, OnInit } from '@angular/core';
import { AuthService } from '../shared/services/auth.service';

@Component({
  selector: 'app-emailverification',
  templateUrl: './emailverification.component.html',
  styleUrls: ['./emailverification.component.scss']
})
export class EmailverificationComponent implements OnInit {
  email:string;
  constructor(private authserve:AuthService) { }

  ngOnInit(): void {
    this.email=JSON.parse(localStorage.getItem('user')).email;
  }

}
