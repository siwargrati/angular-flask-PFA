import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {FileUploader} from 'ng2-file-upload';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent implements OnInit {

  uploadForm: FormGroup;

  public uploader: FileUploader = new FileUploader({
    isHTML5: true
  });

    public uploader1: FileUploader = new FileUploader({
    isHTML5: true
  });

  title = 'Angular File Upload';
  constructor(private fb: FormBuilder, private http: HttpClient ) { }

  uploadSubmit() {
        for (let i = 0; i < this.uploader.queue.length; i++) {
          const fileItem = this.uploader.queue[i]._file;
          if (fileItem.size > 10000000) {
            alert('Each File should be less than 10 MB of size.');
            return;
          }
        }
        for (let j = 0; j < this.uploader.queue.length; j++) {
          const data = new FormData();
          const fileItem = this.uploader.queue[j]._file;
          console.log(fileItem.name);
          data.append('file', fileItem);
          data.append('fileSeq', 'seq' + j);
          data.append( 'dataType', this.uploadForm.controls.type.value);
          this.uploadFile(data).subscribe(response => alert(response.message));
        }
        this.uploader.clearQueue();

        for (let k = 0; k < this.uploader1.queue.length; k++) {
          const fileItem = this.uploader1.queue[k]._file;
          if (fileItem.size > 10000000) {
            alert('Each File should be less than 10 MB of size.');
            return;
          }
        }
        for (let l = 0; l < this.uploader1.queue.length; l++) {
          const data = new FormData();
          const fileItem = this.uploader1.queue[l]._file;
          console.log(fileItem.name);
          data.append('file', fileItem);
          data.append('fileSeq', 'seq' + l);
          data.append( 'dataType', this.uploadForm.controls.type.value);
          this.uploadFile(data).subscribe(response => alert(response.message));
        }
        this.uploader1.clearQueue();
  }

  uploadSubmit1() {

  }

  uploadFile(data: FormData): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:5000/multiple-files-upload', data);
  }

  ngOnInit() {
    this.uploadForm = this.fb.group({
      document: [null, null],
      type:  [null, Validators.compose([Validators.required])]
    });
  }

}


