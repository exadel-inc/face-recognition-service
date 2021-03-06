package com.exadel.frs.core.trainservice.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiParam;
import lombok.Builder;
import lombok.Data;
import org.springframework.web.bind.annotation.RequestParam;

import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;

import static com.exadel.frs.core.trainservice.system.global.Constants.*;

@Data
@Builder
public class VerifyRequest {
    @JsonProperty("file")
    @NotNull
    @ApiParam(value = IMAGE_WITH_ONE_FACE_DESC, required = true)
    private String imageAsBase64;

    @Min(value = 0, message = LIMIT_MIN_DESC)
    @ApiParam(value = LIMIT_DESC)
    private Integer limit;

    @JsonProperty(DET_PROB_THRESHOLD)
    @ApiParam(value = DET_PROB_THRESHOLD_DESC)
    private Double detProbThreshold;

    @JsonProperty(FACE_PLUGINS)
    @ApiParam(value = FACE_PLUGINS_DESC)
    private String facePlugins;

    @JsonProperty(STATUS)
    @ApiParam(value = STATUS_DESC)
    private Boolean status;

    public Integer getLimit() {
        return limit == null ? 0 : limit;
    }
}
