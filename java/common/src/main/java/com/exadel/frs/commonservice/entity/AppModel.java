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

package com.exadel.frs.commonservice.entity;

import com.exadel.frs.commonservice.enums.AppModelAccess;
import com.exadel.frs.commonservice.helpers.ModelAccessTypeConverter;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Entity
@Table(name = "app_model", schema = "public")
@Data
@NoArgsConstructor
@EqualsAndHashCode(of = {"app", "model"})
public class AppModel {

    public AppModel(AppModel appModel){
        this.id = appModel.id;
        this.app = appModel.app;
        this.model = appModel.model;
        this.accessType = appModel.accessType;
    }

    @EmbeddedId
    private AppModelId id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @MapsId("appId")
    private App app;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @MapsId("modelId")
    private Model model;

    @Convert(converter = ModelAccessTypeConverter.class)
    @Column(name = "access_type")
    private AppModelAccess accessType;

    public AppModel(App app, Model model, AppModelAccess accessType) {
        this.app = app;
        this.model = model;
        this.accessType = accessType;
        this.id = new AppModelId(app.getId(), model.getId());
    }
}
