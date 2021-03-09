import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { Location } from '@angular/common';
import { Observable } from 'rxjs';
import { Albums } from '../albums';
import { AlbumsService } from '../albums.service';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.css']
})
export class AlbumDetailComponent implements OnInit {
  album: Albums;
  album$: Observable<Albums>;

  constructor(private route: ActivatedRoute, private router: Router, private albumsService: AlbumsService, private location: Location) { }

  ngOnInit(): void {
    // const albumId = this.route.snapshot.paramMap.get('id');
    // this.album$ = this.albumsService.getAlbum(Number(albumId)); 
    this.getAlbum();
  }

  getAlbum(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.albumsService.getAlbum(id)
      .subscribe(album => this.album = album);
  }

  goBack(): void {
    this.location.back();
  }

  save(): void {
    this.albumsService.updateAlbum(this.album)
      .subscribe(() => this.goBack());
  }

  // gotoItems(album: Albums) {
  //   const albumId = album ? album.id : null;
  //   this.router.navigate(['/albums', { id: albumId }]);
  // }

}
