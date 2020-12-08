import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponentComponent } from './login-component/login-component.component';
import { RegisterComponentComponent } from './register-component/register-component.component';
import {HomeComponent} from './home/home.component';
import { AuthGuard } from './shared/guard/auth.guard';
import { EmailGuard } from './shared/guard/email.guard'
import { LogoutComponent } from './logout/logout.component';
import { EmailverificationComponent } from './emailverification/emailverification.component';
import { ForgotpasswordComponent } from './forgotpassword/forgotpassword.component';
import { LoginGuard } from './shared/guard/login.guard';

const routes: Routes = [
  {path:'',redirectTo:'login',pathMatch:"full"},
  { path: 'login', component: LoginComponentComponent, canActivate:[LoginGuard]},
  { path: 'register', component: RegisterComponentComponent, canActivate: [LoginGuard]},
  {path:'home',component:HomeComponent,canActivate:[AuthGuard]},
  {path:'logout',component:LogoutComponent,canActivate:[AuthGuard]},
  {path:'forgot',component:ForgotpasswordComponent},
  {path:'changepassword',component:ForgotpasswordComponent},
  {path:'email-verification',component:EmailverificationComponent,canActivate:[EmailGuard]},
  {path:'**',redirectTo:'login',pathMatch:"full"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
