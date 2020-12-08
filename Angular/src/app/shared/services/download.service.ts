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
    if (file_name == "png") {
      return this.http.get<any>(`${this.DJANGO_SERVER}/download/${file_name}`, { observe: 'body', responseType: 'arraybuffer' as 'json' }).subscribe(
        response => this.downloadFile(response, "image/png", file_name),
        error => console.log(error)
      );
    }
    else if (file_name == "csv") {
      return this.http.get<any>(`${this.DJANGO_SERVER}/download/${file_name}`, { observe: 'body', responseType: 'arraybuffer' as 'json' }).subscribe(
        response => this.downloadFile(response, "text/csv", file_name),
        error => console.log(error)
      );
    }
    else if (file_name == "showImage") {
      return this.http.get<any>(`${this.DJANGO_SERVER}/download/png`, { observe: 'body', responseType: 'arraybuffer' as 'json' }).subscribe(
        response => this.downloadFile(response, "image/png", file_name),
        error => console.log(error)
      );
    }
  }

  downloadFile(data: any, type: string, fileextension: string) {
    let blob = new Blob([data], { type: type });
    if (fileextension != "showImage") {
      saveAs(blob, "redplag." + fileextension)
    }
    let url = window.URL.createObjectURL(blob);
    console.log(url);
    if (fileextension == "showImage") {
      let x = document.getElementById("heatmap");
      x.setAttribute('src', url);
      x.style.display = "block";
      document.getElementById("heatmap_msg").style.display = "none";
    }
    // let pwa=window.open(url);
    // if(!pwa || pwa.closed || typeof pwa.closed == 'undefined' ){
    //   alert('Please disable your Pop-up blocker and try again')
    // }
  }
}