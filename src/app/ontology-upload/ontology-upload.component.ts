import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {FileUploader} from 'ng2-file-upload';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-ontology-upload',
  templateUrl: './ontology-upload.component.html',
  styleUrls: ['./ontology-upload.component.css']
})
export class OntologyUploadComponent implements OnInit {

  uploadForm: FormGroup;

  public uploader: FileUploader = new FileUploader({
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
          this.uploadOntology(data).subscribe(response => alert(response.message));
        }
        this.uploader.clearQueue();
  }

  uploadOntology(data: FormData): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:5000/multiple-ontology-upload', data);
  }

  ngOnInit() {
    this.uploadForm = this.fb.group({
      document: [null, null],
      type:  [null, Validators.compose([Validators.required])]
    });
  }

}


