import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';

import {AppModule} from './app/app.module';

// src/main.ts  (Angular v15+ standalone or classic)
import '@iframe-resizer/child'


platformBrowserDynamic().bootstrapModule(AppModule)
    .catch(err => console.error(err));
