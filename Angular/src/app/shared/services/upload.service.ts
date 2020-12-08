import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  DJANGO_SERVER: string = "http://127.0.0.1:8000";

  constructor(private http: HttpClient) { }

  upload(formdata, user_code): any {
    // const requestOptions = {
    //   headers: new HttpHeaders(this.authserv.headerDict),
    // };
    let x = document.getElementById("heatmap");
    // x.setAttribute('src', url);
    x.style.display = "none"
    document.getElementById("heatmap_msg").style.display="block";


    return this.http.post<any>(`${this.DJANGO_SERVER}/upload/${user_code}`, formdata)
  }
}
