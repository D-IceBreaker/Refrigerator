import { Component, Input } from '@angular/core';

import { products } from "../products";

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent {
  @Input() currCategory!: string;
  productItems = products;

  share() {
    window.alert("The product has been shared!");
  }

  like() {
    window.alert("The product has been liked!");
  }

  onNotify() {
    window.alert("You will be notified when the product goes on sale");
  }
}
