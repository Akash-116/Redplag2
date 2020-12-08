import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, } from '@angular/forms';
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
  selectedfile: File = null;
  stubfile: File = null;
  user_code: number = 1;

  choices = new FormGroup({
    fileType: new FormControl('cpp'),
    stubCode: new FormControl('no'),
  });

  setUserCode() {
    if (this.choices.value.fileType == "cpp") { this.user_code = 1; }
    else { this.user_code = 0; }
    if (this.choices.value.stubCode == "yes") {
      this.user_code += 2;
    }
    if (this.user_code === 0) { //c++ false, stub false
      this.disableStubButtons(true);
      this.disableZipButtons(false);
      this.disableDownloadButtons(true);
    }
    else if (this.user_code === 1) { //c++ true, stub false
      this.disableStubButtons(true);
      this.disableZipButtons(false);
      this.disableDownloadButtons(true);
    }
    else if (this.user_code === 2) { // c++ false, stub true
      this.disableStubButtons(false);
      this.disableZipButtons(true);
      this.disableDownloadButtons(true);
    }
    else if (this.user_code === 3) {// c++ true, stub true
      this.disableStubButtons(false);
      this.disableZipButtons(true);
      this.disableDownloadButtons(true);
    }

  }
  resetFlow() {
    this.setUserCode();
    (<HTMLInputElement>document.getElementById("zChooseBtn")).value = "";
    this.selectedfile = null;
    (<HTMLInputElement>document.getElementById("sChooseBtn")).value = "";
    this.stubfile = null;
    document.getElementById("heatmap").style.display = "none";

  }

  disableStubButtons(disabled) {
    (<HTMLInputElement>document.getElementById("sChooseBtn")).disabled = disabled;
    (<HTMLInputElement>document.getElementById("sUploadBtn")).disabled = disabled;
    // document.getElementById("sChooseBtn").setAttribute('disabled', disabled) ;
    // document.getElementById("sUploadBtn").setAttribute('disabled', disabled) ;
  }
  disableZipButtons(disabled: boolean) {
    (<HTMLInputElement>document.getElementById("zChooseBtn")).disabled = disabled;
    (<HTMLInputElement>document.getElementById("zUploadBtn")).disabled = disabled;
    // document.getElementById("zChooseBtn").setAttribute('disabled', disabled) ;
    // document.getElementById("zUploadBtn").setAttribute('disabled', disabled) ;
  }
  disableDownloadButtons(disabled: boolean) {
    (<HTMLInputElement>document.getElementById("dImageBtn")).disabled = disabled;
    (<HTMLInputElement>document.getElementById("dCsvBtn")).disabled = disabled;
    // (<HTMLInputElement> document.getElementById("dDisplayBtn")).disabled = disabled ;
  }

  constructor(
    private authserv: AuthService,
    private router: Router,
    private uploadserv: UploadService,
    private downloadserv: DownloadService
  ) { }

  ngOnInit(): void {
    this.setUserCode();
    // this.disableDownloadButtons(true)
    // this.disableStubButtons(true)
    // this.disableZipButtons(true)
  }


  onSelect(event): void {
    this.selectedfile = event.target.files[0];
    // const file=event.target.files[0];
    // this.form.get('inputfile').setValue(file);
    // console.log(event);
  }

  onSelect2(event): void {
    this.stubfile = event.target.files[0];
    // const file=event.target.files[0];
    // this.form.get('inputfile').setValue(file);
    // console.log(event);
  }

  onSubmit(): void {
    if (this.selectedfile === null) {
      window.alert("Please choose a file first.");
      return
    }
    const formdata = new FormData();
    formdata.append('file', this.selectedfile, this.selectedfile.name);
    // console.log(formdata);
    this.uploadserv.upload(formdata, this.user_code).subscribe(
      res => {
        console.log(res);
        this.disableDownloadButtons(false);
        (<HTMLInputElement>document.getElementById("zChooseBtn")).value = "";
        this.selectedfile = null;
        this.download("showImage");
        alert("uploading Zip successful.");
      },
      err => {
        console.log(err);
        alert("upload failed.")
      }
    )
  }

  onSubmit2(): void {
    if (this.stubfile === null) {
      window.alert("Please choose a file first.");
      return
    }
    const formdata = new FormData();
    formdata.append('file', this.stubfile, this.stubfile.name);
    // console.log(formdata);
    this.uploadserv.upload(formdata, 5).subscribe(
      res => {
        console.log(res);
        this.disableZipButtons(false);
        (<HTMLInputElement>document.getElementById("sChooseBtn")).value = "";
        this.stubfile = null;
        alert("uploading Stub successful.");
      },
      err => {
        console.log(err);
        alert("upload failed.")
      }
    )
  }

  download(file_type: string): void {
    // console.log('download called');
    this.downloadserv.download(file_type);
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
  spamFunc() {
    console.log("Spam log. Please ignore.");
  }

}
