import { TestBed } from '@angular/core/testing';

import { AffordabilityApiService } from './affordability-api.service';

describe('AffordabilityApiService', () => {
  let service: AffordabilityApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AffordabilityApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
