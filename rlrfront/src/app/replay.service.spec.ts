import {inject, TestBed} from '@angular/core/testing';

import {ReplayService} from './replay.service';

describe('ReplayService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ReplayService]
    });
  });

  it('should be created', inject([ReplayService], (service: ReplayService) => {
    expect(service).toBeTruthy();
  }));
});
