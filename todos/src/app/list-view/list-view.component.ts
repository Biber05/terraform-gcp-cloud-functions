import {Component, Input, OnInit} from '@angular/core';
import {Todo} from '../models/todo';

@Component({
  selector: 'app-list-view',
  templateUrl: './list-view.component.html',
  styleUrls: ['./list-view.component.scss']
})
export class ListViewComponent implements OnInit {
  @Input() data: Todo[];

  displayedColumns: string[] = ['Name', 'Datum', 'Uhrzeit', 'Status'];

  constructor() {
  }

  ngOnInit(): void {
  }

}
