/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


resource "google_bigquery_table" "imdb_reviews" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "reviews"
  description = "Large Movie Review Dataset v1.0\n\nOverview\n\nThis dataset contains movie reviews along with their associated binary\nsentiment polarity labels. It is intended to serve as a benchmark for\nsentiment classification. This document outlines how the dataset was\ngathered, and how to use the files provided.\n\nDataset\n\nThe core dataset contains 50,000 reviews split evenly into 25k train\nand 25k test sets. The overall distribution of labels is balanced (25k\npos and 25k neg). We also include an additional 50,000 unlabeled\ndocuments for unsupervised learning.\n\nIn the entire collection, no more than 30 reviews are allowed for any\ngiven movie because reviews for the same movie tend to have correlated\nratings. Further, the train and test sets contain a disjoint set of\nmovies, so no significant performance is obtained by memorizing\nmovie-unique terms and their associated with observed labels.  In the\nlabeled train/test sets, a negative review has a score \u003c= 4 out of 10,\nand a positive review has a score \u003e= 7 out of 10. Thus reviews with\nmore neutral ratings are not included in the train/test sets. In the\nunsupervised set, reviews of any rating are included and there are an\neven number of reviews \u003e 5 and \u003c= 5.\n\nColumns\nsplit - it has test(25K) / train(75K) records.\nlabel - Negative(25K)     --\u003e test(12.5K) and train (12.5K)\n        Positive(25K)     --\u003e test(12.5K) and train (12.5K)\n        Unsupervised(50K) --\u003e train(50K)\n\nFor Unsupervised label, reviewer_rating is NaN.\n"
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_reviews-table_id" {
  value = google_bigquery_table.imdb_reviews.table_id
}

output "bigquery_table-imdb_reviews-id" {
  value = google_bigquery_table.imdb_reviews.id
}
