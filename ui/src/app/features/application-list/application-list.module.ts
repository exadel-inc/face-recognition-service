/*
 * Copyright (c) 2020 the original author or authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { MatCardModule, MatIconModule } from '@angular/material';
import { MatButtonModule } from '@angular/material/button';
import { SnackBarModule } from 'src/app/features/snackbar/snackbar.module';
import { SpinnerModule } from 'src/app/features/spinner/spinner.module';

import { TableModule } from '../table/table.module';
import { ApplicationListContainerComponent } from './application-list-container.component';
import { ApplicationListFacade } from './application-list-facade';
import { ApplicationListComponent } from './application-list/application-list.component';

@NgModule({
  declarations: [ApplicationListContainerComponent, ApplicationListComponent],
  exports: [ApplicationListContainerComponent],
  providers: [ApplicationListFacade],
  imports: [
    CommonModule,
    TableModule,
    SpinnerModule,
    MatButtonModule,
    SnackBarModule,
    MatCardModule,
    MatIconModule,
  ]
})
export class ApplicationListModule {}