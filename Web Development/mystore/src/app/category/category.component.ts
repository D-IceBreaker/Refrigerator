import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.css']
})
export class CategoryComponent implements OnInit {
  currCategory = "";

  public productCategories = [
    {
      name: "Data Storage"
    },
    {
      name: "Computer Components"
    },
    {
      name: "Networking & Wireless"
    },
    {
      name: "Monitors"
    }
  ];

  constructor() { }

  ngOnInit(): void {
  }

  setCategory(input: string) {
    this.currCategory = input;
  }

}
