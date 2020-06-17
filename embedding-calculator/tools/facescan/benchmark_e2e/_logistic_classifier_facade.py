#  Copyright (c) 2020 the original author or authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

import logging
from collections import defaultdict, Counter
from typing import Set, Union

from src.exceptions import NoFaceFoundError, MoreThanOneFaceFoundError
from src.services.classifier.logistic_classifier import LogisticClassifier, LogisticClassifierMock
from src.services.facescan.scanner.facescanner import FaceScanner
from tools.facescan.benchmark_e2e._dataset import Image
from tools.facescan.benchmark_e2e.constants import ENV

logger = logging.getLogger(__name__)


class LogisticClassifierFacade:
    def __init__(self, scanner: FaceScanner):
        self._scanner = scanner
        self._classifier: Union[LogisticClassifier, None] = None
        self._counts = defaultdict(Counter)
        self._given_train_names = set()
        self._trained_names = list()

    def _scan(self, array):
        return self._scanner.scan_one(array).embedding

    def train(self, images: Set[Image]) -> None:
        assert self._classifier is None

        embeddings = []
        train_counts = self._counts['Training']
        for img in images:
            self._given_train_names.add(img.name)
            try:
                embedding = img.embedding(scanner=self._scanner)
                embeddings.append(embedding)
                self._trained_names.append(img.name)
            except (NoFaceFoundError, MoreThanOneFaceFoundError) as e:
                train_counts[e.__class__.__name__] += 1
        train_counts['ImagesTotal'] += len(images)
        train_counts['ImagesTrained'] += len(self._trained_names)
        train_counts['NamesTrained'] += len(set(self._trained_names))
        logger.debug(f'Started training with {len(self._trained_names)} images')
        self._classifier = LogisticClassifier.train(embeddings, self._trained_names, self._scanner.ID) \
            if not ENV.DRY_RUN else LogisticClassifierMock()
        logger.debug('Training complete')

    def test_recognition(self, images: Set[Image]) -> dict:
        assert self._classifier is not None
        predict_counts = self._counts['Prediction']
        for img in images:
            if img.name not in self._given_train_names:
                predict_counts['NotInGivenTrainNamesError'] += 1
                continue
            if img.name not in self._trained_names:
                predict_counts['NotInTrainedNamesError'] += 1
                continue
            try:
                embedding = img.embedding(scanner=self._scanner)
            except (NoFaceFoundError, MoreThanOneFaceFoundError) as e:
                predict_counts[e.__class__.__name__] += 1
                continue
            predicted_name = self._classifier.predict(embedding, self._scanner.ID).face_name
            count_name = 'ImagesGuessedCorrectly' if img.name == predicted_name else 'ImagesGuessedIncorrectly'
            predict_counts[count_name] += 1
        predict_counts['ImagesTotal'] += len(images)
        return self._counts