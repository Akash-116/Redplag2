import { Component, OnInit } from '@angular/core';
import { FormGroup,FormControl, } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import * as filesaver from 'file-saver';
import { Router } from '@angular/router';
import { AuthService } from '../shared/services/auth.service';
import { UploadService } from '../shared/services/upload.service';
import { DownloadService } from '../shared/services/download.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {
  // form:FormGroup;
  selectedfile:File=null;
  file_name:string=null;
  user_code:number = 1;
  
  constructor(
    private authserv:AuthService,
    private router:Router,
    private uploadserv:UploadService,
    private downloadserv:DownloadService
    ) { }

  ngOnInit(): void { }


  onSelect(event):void{
    this.selectedfile=event.target.files[0];
    // const file=event.target.files[0];
    // this.form.get('inputfile').setValue(file);
    // console.log(event);
  }
  onSubmit():void{
    const formdata= new FormData();
    this.file_name=this.selectedfile.name;
    formdata.append('file',this.selectedfile,this.selectedfile.name);
    // console.log(formdata);
    this.uploadserv.upload(formdata, this.user_code).subscribe(
      res=>{console.log(res);alert("upload successful.")},
      err=>{console.log(err);alert("upload failed.")}
    )
  }

  download():void{
    // console.log('download called');
    // console.log('file_name is ', this.file_name)
    this.downloadserv.download(this.file_name);
  }
  // getusername():void{
  //   console.log(this.authserv.username)
  // }

  // onupload():void{
  //   this.download();
  //   return;
  // }

  // download():void{
  //   fetch('login').then(response => console.log(response.url))
  //   // this.filedownloadserv.downloadFile("http://localhost:4200/login").subscribe(
  //   //   response=> {
  //   //     let blob:any =new Blob([response]);
  //   //     const url=window.URL.createObjectURL(blob);
  //   //     filesaver.saveAs(blob,'result');  
  //   //   }
  //   // ),error=>console.log('error has occurred while downloading'),
  //   // ()=> console.info('File Downloaded succesfully')
  // }

  
}
