import {Time} from '@angular/common';

export interface Todo {
  name: string;
  date: Date;
  time: Time;
  assignedTo: string;
}
