import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { Albums } from '../albums';
import { AlbumsService } from '../albums.service';

@Component({
  selector: 'app-albums',
  templateUrl: './albums.component.html',
  styleUrls: ['./albums.component.css']
})
export class AlbumsComponent implements OnInit {
  albums: Albums[] = [];

  // albums$: Observable<Albums>;
  // currId: number;

  constructor(private route: ActivatedRoute, private albumsService: AlbumsService) { }

  ngOnInit(): void {
    this.getAlbums();
  //   this.albums$ = this.route.paramMap.pipe(
  //     switchMap(params => {
  //       this.currId = Number(params.get('id'));
  //       return this.albumsService.getAlbums();
  //     })
  //   );
  }

  getAlbums(): void {
    this.albumsService.getAlbums()
      .subscribe(albums => this.albums = albums)
  }

  add(title: string): void {
    title = title.trim();
    if (!title) { return; }
    this.albumsService.addAlbum({ title } as Albums)
      .subscribe(album => {
        this.albums.push(album);
      });
  }

  delete(album: Albums): void {
    this.albums = this.albums.filter(a => a !== album);
    this.albumsService.deleteAlbum(album).subscribe();
  }
  
}
