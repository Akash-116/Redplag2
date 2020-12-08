import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { saveAs } from "file-saver";
@Injectable({
  providedIn: 'root'
})
export class DownloadService {

  DJANGO_SERVER: string = "http://127.0.0.1:8000";
  constructor(private http: HttpClient) { }

  download(file_name: string): any {
    console.log('fle name in service is', file_name);
    return this.http.get<any>(`${this.DJANGO_SERVER}/download/${file_name}`, { observe: 'body', responseType: 'arraybuffer' as 'json' }).subscribe(
      response => this.downloadFile(response, "image/png"),
      error => console.log(error)
    );
  }

  downloadFile(data: any, type: string) {
    let blob = new Blob([data], { type: type });
    let url = window.URL.createObjectURL(blob);
    saveAs(blob, "RedPlag Analysis.png")
    // let pwa=window.open(url);
    // if(!pwa || pwa.closed || typeof pwa.closed == 'undefined' ){
    //   alert('Please disable your Pop-up blocker and try again')
    // }
  }
}